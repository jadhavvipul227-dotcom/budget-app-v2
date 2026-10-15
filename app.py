import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Personal Budget Management System",
    page_icon="💰",
    layout="wide"
)

# 2. Excel File Name
EXCEL_FILE = "Budget_Management_System_Enhanced.xlsx"

# 3. Load Data from Excel
@st.cache_data
def load_data():
    excel = pd.ExcelFile(EXCEL_FILE)
    df_tx = pd.read_excel(excel, sheet_name="Transactions")
    df_summary = pd.read_excel(excel, sheet_name="Monthly Summary")
    df_savings = pd.read_excel(excel, sheet_name="Saving Tracker")
    df_chart = pd.read_excel(excel, sheet_name="Chart Data")
    df_budget = pd.read_excel(excel, sheet_name="Budget Plan")
    return df_tx, df_summary, df_savings, df_chart, df_budget

try:
    df_tx, df_summary, df_savings, df_chart, df_budget = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# 4. Main App Title
st.title("💰 Personal Budget Dashboard")
st.markdown("---")

# 5. Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Select Page", ["Dashboard", "Monthly Summary Sheet", "Transactions Log", "Savings Tracker"])

# Key Metrics Calculation
total_income = df_tx[df_tx["Type"] == "Income"]["Amount"].sum()
total_expense = df_tx[df_tx["Type"] == "Expense"]["Amount"].sum()
net_savings = total_income - total_expense
savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0

# Dashboard Page (All 6 Charts)
if menu == "Dashboard":
    # Key Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Net Savings", f"₹{net_savings:,.2f}")
    col4.metric("Savings Rate", f"{savings_rate:.1f}%")

    st.markdown("---")

    # Row 1: Chart 1 & Chart 2
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Monthly Income vs Expenses")
        if not df_summary.empty:
            fig1 = px.bar(
                df_summary,
                x="Month",
                y=["Income", "Expense"],
                barmode="group",
                color_discrete_map={"Income": "#2ecc71", "Expense": "#e74c3c"}
            )
            st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        st.subheader("2. Expense Distribution by Category")
        df_expenses = df_tx[df_tx["Type"] == "Expense"]
        if not df_expenses.empty:
            df_cat = df_expenses.groupby("Category")["Amount"].sum().reset_index()
            fig2 = px.pie(
                df_cat,
                names="Category",
                values="Amount",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Row 2: Chart 3 & Chart 4
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("3. Monthly Savings Trend")
        if not df_savings.empty:
            fig3 = px.line(
                df_savings,
                x="Month",
                y="Actual Savings",
                markers=True,
                line_shape="linear",
                color_discrete_sequence=["#27ae60"]
            )
            st.plotly_chart(fig3, use_container_width=True)

    with row2_col2:
        st.subheader("4. Budget vs Actual Expenses")
        if not df_budget.empty:
            fig4 = px.bar(
                df_budget,
                y="Category",
                x=["Monthly Budget", "Actual Expenses"],
                barmode="group",
                orientation="h",
                color_discrete_map={"Monthly Budget": "#3498db", "Actual Expenses": "#e67e22"}
            )
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Row 3: Chart 5 & Chart 6
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        st.subheader("5. Income Sources Analysis")
        df_inc = df_tx[df_tx["Type"] == "Income"]
        if not df_inc.empty:
            df_source = df_inc.groupby("Category")["Amount"].sum().reset_index()
            fig5 = px.bar(
                df_source,
                y="Category",
                x="Amount",
                orientation="h",
                color_discrete_sequence=["#2980b9"]
            )
            st.plotly_chart(fig5, use_container_width=True)

    with row3_col2:
        st.subheader("6. Payment Mode Analysis")
        if "Payment Mode" in df_tx.columns:
            df_pay = df_tx.groupby("Payment Mode")["Amount"].sum().reset_index()
            fig6 = px.pie(
                df_pay,
                names="Payment Mode",
                values="Amount",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig6, use_container_width=True)

# Monthly Summary Sheet Page
elif menu == "Monthly Summary Sheet":
    st.subheader("📊 Monthly Summary Sheet")
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
    fig_sav = px.bar(
        df_savings,
        x="Month",
        y=["Goal", "Actual Savings"],
        barmode="group"
    )
    st.plotly_chart(fig_sav, use_container_width=True)