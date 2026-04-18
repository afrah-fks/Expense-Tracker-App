import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.processor import clean_and_feature_engineer

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="FinTrack: Expense Analytics", layout="wide")

# --- 2. DATA LOADING LOGIC ---
@st.cache_data
def load_data():
    """Reads the CSV from the data folder and cleans it."""
    file_path = 'data/expenses.csv'
    if os.path.exists(file_path):
        raw_data = pd.read_csv(file_path)
        # Apply the cleaning logic from your src folder
        processed_data = clean_and_feature_engineer(raw_data)
        return processed_data
    else:
        return None

# --- 3. INITIALIZE DATA ---
df = load_data()

# --- 4. UI CHECK ---
if df is None:
    st.error("❌ 'expenses.csv' not found in the 'data/' folder!")
    st.info("Please run `python create_csv.py` first to generate your dataset.")
else:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Navigation & Filters")
    
    # Category Filter
    all_categories = df['Category'].unique().tolist()
    selected_cats = st.sidebar.multiselect("Select Categories", all_categories, default=all_categories)
    
    # Month Filter
    all_months = df['Month'].unique().tolist()
    selected_months = st.sidebar.multiselect("Select Months", all_months, default=all_months)

    # Apply Filters to DataFrame
    filtered_df = df[
        (df['Category'].isin(selected_cats)) & 
        (df['Month'].isin(selected_months))
    ]

    # --- MAIN DASHBOARD UI ---
    st.title("📊 FinTrack: Personal Finance Dashboard")
    st.markdown(f"**Analysis Period:** {min(df['Date'])} to {max(df['Date'])}")
    st.divider()

    # --- TOP METRICS (KPIs) ---
    total_spend = filtered_df['Amount'].sum()
    avg_trans = filtered_df['Amount'].mean()
    transaction_count = len(filtered_df)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Expenses", f"${total_spend:,.2f}")
    kpi2.metric("Avg. Transaction", f"${avg_trans:,.2f}")
    kpi3.metric("Transactions", transaction_count)

    st.divider()

    # --- VISUALIZATIONS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        fig_pie = px.pie(
            filtered_df, 
            values='Amount', 
            names='Category', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Monthly Spending Trends")
        # Ensure trends are sorted by the Month_Sort column we created in processor.py
        trend_data = filtered_df.groupby(['Month_Sort', 'Month'])['Amount'].sum().reset_index()
        fig_line = px.line(
            trend_data, 
            x='Month', 
            y='Amount', 
            markers=True,
            title="Total Spend per Month"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # --- AUTOMATED EXPORT LOGIC ---
    st.sidebar.divider()
    if st.sidebar.button("💾 Save Charts to 'outputs/'"):
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        
        # Save images using kaleido
        try:
            fig_pie.write_image("outputs/category_breakdown.png")
            fig_line.write_image("outputs/monthly_trend.png")
            st.sidebar.success("Images saved successfully!")
        except Exception as e:
            st.sidebar.error(f"Error saving: {e}")

    # --- DATA TABLE ---
    st.divider()
    with st.expander("🔍 View Filtered Transaction History"):
        # Drop the sorting helper column before displaying to user
        display_df = filtered_df.drop(columns=['Month_Sort'])
        st.dataframe(display_df, use_container_width=True)

    # --- FOOTER ---
    st.markdown("---")
    st.caption("Developed for Data Science Portfolio | Synthetic Data Simulation")