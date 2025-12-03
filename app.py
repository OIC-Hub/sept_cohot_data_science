#import libraries
import pandas as pd
import plotly.express as px
import streamlit as st

def streamlit_app():
  #Page config
  st.set_page_config(
    page_title="Bank Churn Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
  )

  #load dataset
  df = pd.read_csv("cleaned_bank_customer_churn.csv")

  #header
  st.title("📈 Business Churn Customer Dashboard")
  st.caption("A strategic overview churn pattern customer segment, demographic and Finance.")
  st.markdown("---")

  #sidebar filter
  st.sidebar.header("Dashboard Filters")

  geo_filter = st.sidebar.multiselect(
    label="Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
  )

  gender_filter = st.sidebar.multiselect(
    label="Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
  )

  #apply filter
  filtered_df = df[
    (df["Geography"].isin(geo_filter)) &
    (df["Gender"].isin(gender_filter))
  ]

  #KPIs Summary
  total_count = len(filtered_df)
  churn_customer = filtered_df["Exited"].sum()
  churn_rate = round(churn_customer / total_count * 100, 2)

  avg_credit_score = round(filtered_df["CreditScore"].mean(), 1)
  avg_salary = round(filtered_df["EstimatedSalary"].mean(), 1)

  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("Total Customer", total_count)
  col2.metric("Churn Customer", churn_customer)
  col3.metric("Churn Rate", f"{churn_rate}%")
  col4.metric("Avg Credit Score", avg_credit_score)
  col5.metric("Avg Estimated Salary", f"${avg_salary:,.0f}")





streamlit_app()
