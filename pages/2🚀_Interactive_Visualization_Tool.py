import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

def main():
    #1. Setup Streamlit interface
    st.set_page_config(
        page_title="🚀Interactive Visualization Tool",layout="wide"
    )

    st.header("2🚀Interactive Visualization Tool")
    st.write("### Welcome to Interactive Visualization Tool")

    #2. Render pywa;ker
    if st.session_state.get("df") is not None:
        pyg_app = StreamlitRenderer(st.session_state.df)
        pyg_app .explorer()
    else:
        st.info("Please upload a data set to begin using the interactive visualization tools")

if __name__ == "__main__":
    main()
