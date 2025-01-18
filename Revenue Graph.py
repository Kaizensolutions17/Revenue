import streamlit as st
import pandas as pd
import plotly.express as px

# Load DataFrame (replace this with the path to your actual Excel file)
data = pd.read_excel(r"Revenue and Agency Performance.xlsx")
df = pd.DataFrame(data)

# Handle missing or null values
df["Product"] = df["Product"].fillna("Unknown")
df["Period"] = df["Period"].fillna("Unknown")

# Streamlit app
st.title("Business Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_product = st.sidebar.multiselect(
    "Select Product", options=df["Product"].unique(), default=df["Product"].unique()
)
selected_period = st.sidebar.multiselect(
    "Select Period", options=df["Period"].unique(), default=df["Period"].unique()
)

# Ensure selected filters are not empty
if not selected_product:
    selected_product = df["Product"].unique()
if not selected_period:
    selected_period = df["Period"].unique()

# Filter data based on selections
filtered_df = df[
    (df["Product"].isin(selected_product)) & 
    (df["Period"].isin(selected_period))
]

# Key metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Billing", f"₹{filtered_df['Billing'].sum():,.2f}")
with col2:
    st.metric("Total Profit", f"₹{filtered_df['Profit'].sum():,.2f}")
with col3:
    st.metric("Total Office Expenses", f"₹{filtered_df['Office Exp'].sum():,.2f}")

# Visualizations
st.header("Visualizations")

# Billing Trends
billing_fig = px.line(
    filtered_df, x="Period", y="Total Billing In Month", color="Product",
    title="Billing Trends by Product"
)
st.plotly_chart(billing_fig)

# Profit vs Salary
profit_salary_fig = px.bar(
    filtered_df, x="Period", y=["Profit", "Salary"],
    title="Profit vs Salary", barmode="group"
)
st.plotly_chart(profit_salary_fig)

# Productivity by Product
productivity_fig = px.bar(
    filtered_df, x="Product", y="Productivity", color="Product",
    title="Productivity by Product"
)
st.plotly_chart(productivity_fig)

# Profitability Heatmap
heatmap_fig = px.density_heatmap(
    filtered_df, x="Period", y="Product", z="Profit",
    title="Profitability Heatmap", nbinsx=4, nbinsy=4
)
st.plotly_chart(heatmap_fig)

# Additional Insights
st.header("Additional Insights")
# Productivity and Weightage Correlation
st.write("### Productivity and Weightage Correlation")
correlation = filtered_df["Productivity"].corr(filtered_df["Weightage"])
st.write(f"Correlation Coefficient: {correlation:.2f}")

# Download filtered data
st.header("Download Filtered Data")
st.download_button(
    label="Download Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
