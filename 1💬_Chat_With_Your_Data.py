import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# streamlit run "1💬_Chat_With_Your_Data.py"

from src.logger.base import BaseLogger
from src.models.llms import load_llm
from src.utils import execute_plt_code


#load enviroment varibles
load_dotenv()
loggger = BaseLogger()
# gemini-2.5-flash or gemini-2.5-pro
MODEL_NAME = "gemini-2.5-flash"

# _exract_action(response)
def _exract_action(response):
    steps = response.get("intermediate_steps") or []
    if not steps:
        return None
    
    last = steps[-1][0] #
    tool_input = getattr(last,"tool_input",None)

    if isinstance(tool_input,dict):
        return tool_input.get("query") or tool_input.get("code") or str(tool_input)
    if tool_input is None:
        return None
    return str(tool_input)
#process_query
def process_query(da_angent, query):
    response = da_angent(query)

    action = _exract_action(response)
    output_text = str(response.get("output", ""))

    st.write(output_text)

    # luôn có giá trị mặc định
    to_display_string = output_text

    if action:
        # chạy plot nếu có
        if "plt" in action:
            fig = execute_plt_code(action, df=st.session_state.df)
            if fig:
                st.pyplot(fig)

        # luôn hiển thị code action
        st.code(action)

        # lưu lịch sử: output + code
        to_display_string = output_text + "\n" + f"```python\n{action}\n```"

    st.session_state.history.append((query, to_display_string))


# Story chat
def display_chat_history():
    st.markdown('## Chat History')
    for i,(q,r) in enumerate(st.session_state.history):
        st.markdown(f"**Query: {i+1}:** {q}")
        st.markdown(f"**Response: {i+1}:** {r}")
        st.markdown(f"---")

def main():
    #1.Set up streamlit interface
    st.header("💬CHAT WITH YOUR DATA")
    st.write("Welcome to our data analysis tool. This tool can assist your daily data analysis tasks")
    st.set_page_config(page_title="Data Analysis Tool",page_icon="📈",layout="centered")

    #2. load llms models
    llm = load_llm(model_name = MODEL_NAME)
    loggger.info(f"### Successfully loaded {MODEL_NAME} !###")

    #3. Upload csv 
    with st.sidebar:
        up_load_csv = st.file_uploader("Upload your csv file here",type="csv")

    #4. Initial chat history
    if "history" not in st.session_state:
        st.session_state.history = []
    
    #5. Read csv 
    if up_load_csv is not None:
        st.session_state.df = pd.read_csv(up_load_csv)
        st.write("## Your uploaded data: ",st.session_state.df.head())
    
        #6 Create DA angent to query with our data
        da_angent = create_pandas_dataframe_agent(
            llm= llm,
            df = st.session_state.df,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True,
        )
        loggger.info("### Successfully loaded data analysis agent !###")

        #7. Input query and process query
        query = st.text_input("Input your questions: ")
        if st.button("Run query"):
            with st.spinner("Processing..."):
                process_query(da_angent,query)

        #8. History chat
        st.divider()
        display_chat_history()
 

if __name__ == "__main__":
    main()