import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os

def get_db_connection():
    db_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    return create_engine(db_url)

def main():
    st.title("Price Intelligence Dashboard")
    
    try:
        # Get latest data
        engine = get_db_connection()
        query = """
        SELECT product_id, competitor_id, platform, price, created_at
        FROM price_history 
        ORDER BY created_at DESC 
        LIMIT 1000
        """
        df = pd.read_sql(query, engine)
        
        # Price Trends
        st.subheader("Price Trends by Product")
        fig = px.line(df, x='created_at', y='price', 
                    color='product_id', title='Price Trends Over Time')
        st.plotly_chart(fig)
        
        # Competitor Analysis
        st.subheader("Competitor Price Comparison")
        competitor_df = df.groupby(['competitor_id'])['price'].agg(['mean', 'min', 'max']).reset_index()
        st.dataframe(competitor_df)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()

if __name__ == "__main__":
    main()