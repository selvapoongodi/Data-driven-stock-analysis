import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Database Connection
engine = create_engine("mysql+pymysql://selva:guru@127.0.0.1:3306/first_schema")

st.set_page_config(layout="wide", page_title="Nifty 50 Professional Dashboard")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM nifty50_stocks", engine)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['Ticker', 'date'])
    
    # Yearly Performance Logic
    perf = df.groupby('Ticker')['close'].agg(['first', 'last'])
    perf['yearly_return'] = ((perf['last'] - perf['first']) / perf['first']) * 100
    
    # Technical Metrics
    df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
    
    return df, perf

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📈 Stock Analytics")

# List 1: Key Metrics & Rankings
st.sidebar.subheader("📋 Key Metrics & Rankings")
list_1 = st.sidebar.radio(
    "Select Metric:",
    ["Market Summary", "Top 10 Green Stocks", "Top 10 Loss Stocks"],
    key="list1"
)

st.sidebar.divider()

# List 2: Advanced Technical Analysis
st.sidebar.subheader("🔬 Technical Analysis")
list_2 = st.sidebar.selectbox(
    "Select Analysis:",
    [
        "None",
        "1. Volatility Analysis", 
        "2. Cumulative Return", 
        "3. Sector-wise Performance", 
        "4. Stock Correlation", 
        "5. Monthly Gainers/Losers"
    ],
    key="list2"
)

# --- LOGIC TO RESET SELECTION ---
# If user picks from List 2, we prioritize that view.
if list_2 != "None":
    view = list_2
else:
    view = list_1

# --- MAIN RENDERER ---
try:
    df, perf = load_data()

    # --- LIST 1 VIEWS ---
    if view == "Market Summary":
        st.header("📊 Market Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Green vs Red", f"{len(perf[perf['yearly_return']>0])} / {len(perf[perf['yearly_return']<=0])}")
        m2.metric("Avg Price", f"₹{df['close'].mean():.2f}")
        m3.metric("Avg Volume", f"{df['volume'].mean():,.0f}")

    elif view == "Top 10 Green Stocks":
        st.header("🍏 Top 10 Green Stocks (Yearly)")
        st.table(perf.sort_values('yearly_return', ascending=False).head(10)[['yearly_return']])

    elif view == "Top 10 Loss Stocks":
        st.header("🍎 Top 10 Loss Stocks (Yearly)")
        st.table(perf.sort_values('yearly_return', ascending=True).head(10)[['yearly_return']])

    # --- LIST 2 VIEWS ---
    elif view == "1. Volatility Analysis":
        st.header("⚖️ Top 10 Most Volatile Stocks")
        vol = df.groupby('Ticker')['daily_return'].std().sort_values(ascending=False).head(10).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=vol, x='Ticker', y='daily_return', palette="magma", ax=ax)
        plt.xticks(rotation=45, ha='right') # Rotate labels 45 degrees
        plt.tight_layout()                  # Automatically adjust layout to prevent clipping
        st.pyplot(fig)

    elif view == "2. Cumulative Return":
        st.header("🚀 Cumulative Return (Top 5)")
        top_5 = perf.sort_values('yearly_return', ascending=False).head(5).index
        cdf = df[df['Ticker'].isin(top_5)].copy()
        cdf['cum_ret'] = cdf.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)
        st.line_chart(cdf.pivot(index='date', columns='Ticker', values='cum_ret'))

    elif view == "3. Sector-wise Performance":
        st.header("🏗️ Sector Performance")
        st.info("Upload/Load your Sector CSV to see this data.")
        # Example implementation assuming a 'sector_df' exists:
        # sector_perf = merged_df.groupby('Sector')['yearly_return'].mean()
        # st.bar_chart(sector_perf)

    elif view == "4. Stock Correlation":
        st.header("🌡️ Stock Correlation Heatmap")
        corr = df.pivot(index='date', columns='Ticker', values='close').pct_change().corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, cmap='RdYlGn', ax=ax)
        st.pyplot(fig)

    elif view == "5. Monthly Gainers/Losers":
        st.header("📅 Monthly Performance")
        df['month'] = df['date'].dt.to_period('M').astype(str)
        month = st.select_slider("Select Month", options=sorted(df['month'].unique()))
        mdf = df[df['month'] == month]
        m_perf = mdf.groupby('Ticker')['close'].agg(['first', 'last'])
        m_perf['ret'] = (m_perf['last'] - m_perf['first']) / m_perf['first']
        
        c1, c2 = st.columns(2)
        c1.subheader("Top 5 Gainers")
        c1.bar_chart(m_perf['ret'].sort_values(ascending=False).head(5))
        c2.subheader("Top 5 Losers")
        c2.bar_chart(m_perf['ret'].sort_values(ascending=True).head(5))

except Exception as e:
    st.error(f"Connection Error: {e}")