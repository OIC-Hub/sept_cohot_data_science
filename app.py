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

  # Row 1 - Geography & Gender
  left, right = st.columns(2)
  with left:
    st.subheader("Customer Churn Distribution by Geography")
    fig_geo = px.histogram(
      filtered_df,
      x="Geography",
      color="Exited",
      barmode="group",
      title="Churn rate accross countries"
    )
    st.plotly_chart(fig_geo, use_container_width=True)

  with right:
    st.subheader("Customer Churn Distribution by Gender")
    fig_gender = px.histogram(
      filtered_df,
      x="Gender",
      color="Exited",
      barmode="group",
      title="Churn rate by gender"
    )
    st.plotly_chart(fig_gender, use_container_width=True)
  
  #Row 2 - Age and CreditScore
  left, right = st.columns(2)
  with left:
    st.subheader("Age: Customer Churn vs Non-Churn")
    fig_age = px.box(
      filtered_df,
      x="Exited",
      y="Age",
      color="Exited",
      points="all",
      title="Age Distribution by Churn"
    )
    st.plotly_chart(fig_age, use_container_width=True)

  with right:
    st.subheader("Customer Churn Distribution by CreditScore")
    fig_credit_score = px.histogram(
      filtered_df,
      x="CreditScore",
      color="Exited",
      title="Churn rate by credit score"
    )
    st.plotly_chart(fig_credit_score, use_container_width=True)
  

  #Row 3 - NumOfProduct and Tenure
  left, right = st.columns(2)
  with left:
    st.subheader("Number Of Product: Customer Churn vs Non-Churn")
    fig_product = px.histogram(
      filtered_df,
      x="NumOfProducts",
      barmode="group",
      color="Exited",
      title="How product influences churn"
    )
    st.plotly_chart(fig_product, use_container_width=True)

  with right:
    st.subheader("Tenure: Customer Loyalty Indicator")
    fig_tenure = px.histogram(
      filtered_df,
      x="Tenure",
      color="Exited",
      title="Tenure Comparison Between Churn & Active Customer"
    )
    st.plotly_chart(fig_tenure, use_container_width=True)
  
  st.markdown("---")
  st.subheader("Data Preview")
  st.dataframe(filtered_df.head(20))

streamlit_app()
