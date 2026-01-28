from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import streamlit as st
import pandas as pd
import os
import boto3
import json
import os
import pandas as pd
import numpy as np
import io
import psycopg2
from psycopg2.extras import execute_values
import warnings


DB_NAME = "postgres"
DB_USER = "group_B04"
DB_PASSWORD = "Surveyanalysis_b04"
DB_HOST = "careerspace.ctsoqg24oatl.ca-central-1.rds.amazonaws.com"
DB_PORT = "5432"
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    data = pd.read_sql_query("SELECT * FROM public.Survey_data_table_2025", conn)
    print(data.shape)
# Close the connection
    conn.close()
except:
    print("Unable to connect to the database")

context = """
You are a data analyst chatbot. The dataframe contains survey data.
- Column 'Question_id' maps to specific survey questions.
- Column 'Question' provides the specific question
- Column 'Survey_Number' is the column used to identify unique surveys. Used to get count of number of surveys.
- Column 'Response' contains textual customer answers.
- Columns 'Sentiment_score' and 'Emotion_score' are float scores derived from NLP models calculating score.
- `Start_Date` and `End_Date`: Timestamps indicating when the survey session started and ended.used for time range calculations.
-  Sentiment_score` and `Sentiment_class`: Numerical score and categorical label derived from sentiment analysis.
- `Emotion_score` and `Emotion_class`: Numerical score and categorical label for detected emotion.
- `LDA_Dominant_Topic`, `lda_Perc_Contribution`, `Topic_Keywords`, `Topic_name_LDA`: Results from topic modeling using Latent Dirichlet Allocation (LDA).
Always use distinct count of Survey_Number column to get number of surveys.
Some values such as sentiment and topic modeling fields may be missing (NaN) for non-text responses or if analysis was not applicable.

You are tasked with interpreting the survey results, summarizing trends, and answering questions based on this data.
"""

def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False

api_key=os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="Chatbot: Chat with Survey Data", page_icon="🦜")
st.title(" Chatbot: Chat with Survey Data")


df = data

openai_api_key = api_key
if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "system", "content": context},
                                    {"role": "assistant", "content": "How can I help you with the survey data?"}]

    #st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Ask a Question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True
    )
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
        allow_dangerous_code=True  # Ensure you understand the security implications
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
        
        
### Deploy code using below command
#  streamlit run Chatbot.py