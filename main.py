import streamlit as st
import pandas as pd
import plotly.express as px


# Page Config

st.set_page_config(
    page_title="Business Churn Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load Data

df = pd.read_csv("cleaned_bank_customer_churn.csv")


# Header

st.title("Business Customer Churn Dashboard")
st.caption("A strategic overview of churn patterns across customer segments, demographics, and financial behavior.")

st.markdown("---")


# Sidebar Filters

st.sidebar.header("Dashboard Filters")

geo_filter = st.sidebar.multiselect(
    "Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Apply filters
filtered_df = df[
    (df["Geography"].isin(geo_filter)) &
    (df["Gender"].isin(gender_filter))
]


# Business KPIs Overview

st.subheader("Executive Summary")

total_customers = len(filtered_df)
churned = filtered_df["Exited"].sum()
churn_rate = round((churned / total_customers) * 100, 2)

avg_credit = round(filtered_df["CreditScore"].mean(), 1)
avg_salary = round(filtered_df["EstimatedSalary"].mean(), 1)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Churn Rate", f"{churn_rate}%")
col4.metric("Avg Credit Score", avg_credit)
col5.metric("Avg Estimated Salary", f"${avg_salary:,.0f}")

st.markdown("---")


# Row 1 — Geography & Gender

left, right = st.columns(2)

with left:
    st.subheader("Churn Distribution by Geography")
    fig_geo = px.histogram(
        filtered_df,
        x="Geography",
        color="Exited",
        barmode="group",
        title="Churn Rate Across Countries",
    )
    st.plotly_chart(fig_geo, use_container_width=True)

with right:
    st.subheader("Gender Distribution Among Customers")
    fig_gender = px.histogram(
        filtered_df,
        x="Gender",
        color="Exited",
        barmode="group",
        title="Gender-Based Churn Split",
    )
    st.plotly_chart(fig_gender, use_container_width=True)


# Row 2 — Age & Credit Score

left, right = st.columns(2)

with left:
    st.subheader("Age: Churn vs Non-Churn")
    fig_age = px.box(
        filtered_df,
        x="Exited",
        y="Age",
        color="Exited",
        points="all",
        title="Age Distribution by Churn Status",
    )
    st.plotly_chart(fig_age, use_container_width=True)

with right:
  st.subheader("Credit Score Distribution")
  fig_credit = px.histogram(
      filtered_df,
      x="CreditScore",
      color="Exited",
      barmode="group",
      title="Customer Credit Score Patterns",
  )
  st.plotly_chart(fig_credit, use_container_width=True)


# Row 3 — Number of Products & Balance

left, right = st.columns(2)

with left:
  st.subheader("Number of Products vs Churn")
  fig_products = px.histogram(
    filtered_df,
    x="NumOfProducts",
    color="Exited",
    barmode="group",
    title="How Product Usage Influences Churn",
  )
  st.plotly_chart(fig_products, use_container_width=True)

with right:
  st.subheader("Tenure: Customer Loyalty Indicator")
  fig_tenure = px.histogram(
    filtered_df,
    x="Tenure",
    color="Exited",
    nbins=11,
    title="Tenure Comparison Between Churned & Active Customers",
  )
  st.plotly_chart(fig_tenure, use_container_width=True)


# Data Preview

st.markdown("---")
st.subheader("Data Preview")
st.dataframe(filtered_df.head(20))
