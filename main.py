import streamlit as st
from vanna_connector import VannaConnector
from utils import prepend_schema
import logging
from logging_config import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize Vanna with your database configuration
        vc = VannaConnector()
        df_information_schema = vc.get_information_schema()
        
        # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
        plan = vc.get_training_plan(df_information_schema)
        vc.train(plan=plan)  # Using the updated train method with plan

        my_question = st.session_state.get("my_question", default=None)
        if my_question is None:
            my_question = st.text_input("Ask me a question that I can turn into SQL", key="my_question")
        else:
            st.title(my_question)
            try:
                sql = vc.generate_sql(my_question)
                if sql:
                    sql = prepend_schema(sql)
                    st.code(sql, language='sql')
                    df = vc.run_sql(sql)  
                    if df is not None:
                        st.dataframe(df, use_container_width=True)
                        plotly_code = vc.generate_plotly_code(question=my_question, sql=sql, df=df)
                        if plotly_code:
                            fig = vc.get_plotly_figure(plotly_code=plotly_code, df=df)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Failed to retrieve data. Please check the SQL query or database connection.")
                else:
                    st.error("No SQL generated. Please refine your question.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                st.error(f"An error occurred: {e}")
            st.button("Ask another question", on_click=lambda: st.session_state.clear())
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        st.error("A critical error occurred. Please check the logs for more details.")

if __name__ == "__main__":
    main()