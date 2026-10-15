import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Personal Budget Management System",
    page_icon="💰",
    layout="wide"
)

# 2. Updated File Name
EXCEL_FILE = "Budget_Management_System_Enhanced.xlsx"

# 3. Load Data from Excel
@st.cache_data
def load_data():
    excel = pd.ExcelFile(EXCEL_FILE)
    df_tx = pd.read_excel(excel, sheet_name="Transactions")
    df_summary = pd.read_excel(excel, sheet_name="Monthly Summary")
    df_savings = pd.read_excel(excel, sheet_name="Saving Tracker")
    return df_tx, df_summary, df_savings

try:
    df_tx, df_summary, df_savings = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# 4. Main App Title
st.title("💰 Personal Budget Dashboard")
st.markdown("---")

# 5. Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Select Page", ["Dashboard", "Monthly Summary Sheet", "Transactions Log", "Savings Tracker"])

# Calculate Totals from Transactions
total_income = df_tx[df_tx["Type"] == "Income"]["Amount"].sum()
total_expense = df_tx[df_tx["Type"] == "Expense"]["Amount"].sum()
net_savings = total_income - total_expense
savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0

# Dashboard Page
if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Net Savings", f"₹{net_savings:,.2f}")
    col4.metric("Savings Rate", f"{savings_rate:.1f}%")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Expenses by Category")
        df_expenses = df_tx[df_tx["Type"] == "Expense"]
        if not df_expenses.empty:
            cat_fig = px.pie(
                df_expenses,
                names="Category",
                values="Amount",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(cat_fig, use_container_width=True)

    with col_chart2:
        st.subheader("Monthly Income vs Expense Trend")
        if not df_summary.empty:
            trend_fig = px.bar(
                df_summary,
                x="Month",
                y=["Income", "Expense"],
                barmode="group",
                color_discrete_map={"Income": "#2ecc71", "Expense": "#e74c3c"}
            )
            st.plotly_chart(trend_fig, use_container_width=True)

# Monthly Summary & Formulas Page
elif menu == "Monthly Summary Sheet":
    st.subheader("📊 Monthly Summary Sheet & Excel Formulas")
    
    summary_data = {
        "Metric": ["Income", "Expense", "Savings", "Savings %"],
        "Excel Formula": [
            "=SUM(Income!D:D)", 
            "=SUM(Expense!D:D)", 
            "=B2-C2", 
            "=D2/B2*100"
        ],
        "Calculated Value": [
            f"₹{total_income:,.2f}",
            f"₹{total_expense:,.2f}",
            f"₹{net_savings:,.2f}",
            f"{savings_rate:.2f}%"
        ]
    }
    
    df_formula_summary = pd.DataFrame(summary_data)
    st.table(df_formula_summary)
    
    st.markdown("---")
    st.subheader("Monthly Breakdown Data")
    st.dataframe(df_summary, use_container_width=True)

# Transactions Log Page
elif menu == "Transactions Log":
    st.subheader("All Transactions")
    type_filter = st.selectbox("Filter by Type", ["All", "Income", "Expense"])
    filtered_df = df_tx.copy()
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    st.dataframe(filtered_df, use_container_width=True)

# Savings Tracker Page
elif menu == "Savings Tracker":
    st.subheader("Monthly Savings Goals vs Actual Savings")
    st.dataframe(df_savings, use_container_width=True)
    goal_fig = px.bar(
        df_savings,
        x="Month",
        y=["Goal", "Actual Savings"],
        barmode="group",
        labels={"value": "Amount (₹)", "variable": "Type"}
    )
    st.plotly_chart(goal_fig, use_container_width=True)