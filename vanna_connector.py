from vanna.remote import VannaDefault
import pandas as pd
from config import VANNA_MODEL, VANNA_API_KEY, POSTGRES_CONFIG
import logging

logger = logging.getLogger(__name__)

class VannaConnector:
    def __init__(self):
        self.vn = VannaDefault(model=VANNA_MODEL, api_key=VANNA_API_KEY)
        self.connection = self.connect_to_postgres()

    def connect_to_postgres(self):
        logger.info("Connecting to PostgreSQL database")
        return self.vn.connect_to_postgres(**POSTGRES_CONFIG)

    def get_information_schema(self):
        query = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_schema = 'DATAWAREHOUSE' and table_name = 'FACTURACION'"
        return self.run_sql(query)

    def run_sql(self, query):
        try:
            logger.debug(f"Running SQL query: {query}")
            return self.vn.run_sql(query)
        except Exception as e:
            logger.error(f"SQL query failed: {e}")
            return None

    def get_training_plan(self, df):
        return self.vn.get_training_plan_generic(df)

    def generate_sql(self, question):
        try:
            logger.info(f"Generating SQL for question: {question}")
            return self.vn.generate_sql(question)
        except Exception as e:
            logger.error(f"Failed to generate SQL: {e}")
            return None

    def generate_plotly_code(self, question, sql, df):
        try:
            return self.vn.generate_plotly_code(question=question, sql=sql, df=df)
        except Exception as e:
            logger.error(f"Failed to generate plotly code: {e}")
            return None

    def get_plotly_figure(self, plotly_code, df):
        try:
            return self.vn.get_plotly_figure(plotly_code=plotly_code, df=df)
        except Exception as e:
            logger.error(f"Failed to generate plotly figure: {e}")
            return None

    def train(self, plan):
        try:
            logger.info("Training model with plan")
            self.vn.train(plan=plan)
            logger.info("Model training completed successfully")
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return None