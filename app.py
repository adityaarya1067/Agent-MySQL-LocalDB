import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

# Page Configuration
st.set_page_config(page_title="Langchain: Chat with SQL DB")
st.title("Langchain: Chat with SQL DB")

# Sidebar options for database selection
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
radio_opt = ["Use SQLite 3 Database-Student.db", "Connect to your SQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

# SQL Database configuration
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MYSQL User")
    mysql_password = st.sidebar.text_input("Please enter your password", type='password')
    mysql_db = st.sidebar.text_input("MYSQL database")
else:
    db_uri = LOCALDB

# Groq API Key input
api_key = st.sidebar.text_input(label="Groq API Key", type="password")

# Check for missing API Key or DB selection
if not db_uri:
    st.info("Please enter the database information and URI")

if not api_key:
    st.info("Please add the Groq API key")

# LLM Setup
llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192", streaming=True)

# Database configuration function
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MYSQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

# Setup the database connection
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# SQLDatabase Toolkit setup
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Agent setup
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Handle message history in session state
if "messages" not in st.session_state or st.sidebar.button("Clear message History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input for query
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        # Streamlit callback handler setup
        streamlit_callback = StreamlitCallbackHandler(st.container())

        # Run the agent with error handling
        try:
            response = agent.run(input=user_query, callbacks=[streamlit_callback], handle_parsing_errors=True)
            if "I'm ready to help!" in response:
                st.warning("It seems like the question was too vague or missing context. Please ask a more specific question.")
            else:
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred while processing your query: {str(e)}")
