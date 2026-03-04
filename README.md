# Data-Driven Stock Analysis: Nifty 50 Market Trends
## Overview
This project is a comprehensive end-to-end data analytics solution for the Nifty 50 stock market. It automates the extraction of raw monthly stock data from YAML files, processes it into a structured MySQL database, calculates advanced financial metrics, and visualizes trends through an interactive Streamlit dashboard.

## Features
ETL Pipeline: Python script to convert YAML files into structured SQL tables.

Statistical Analysis: Calculates Volatility, Cumulative Returns, and Correlation matrices.

Interactive UI: A custom Streamlit dashboard with real-time filtering.

## Tech Stack & Skills

Languages: Python

Libraries: Pandas, SQLAlchemy, PyYAML, Matplotlib, Seaborn

Database: MySQL

Visualization: Streamlit, Power BI

Domain: Finance / Data Engineering

## Implementation Steps
# 1. Data Extraction & ETL
The script parses multiple .yaml files from a nested directory structure (C:\Users\Administrator\Downloads\Data\extracted). It handles both list and dictionary formats to consolidate the data into a master DataFrame.

Key Action: Standardizes column names and converts dates to datetime objects.

Storage: Uploads the raw data to the nifty50_stocks table in the first_schema database.

# 2. Advanced Metrics Engine
A secondary processing layer calculates crucial financial indicators:

Volatility: Uses standard deviation of daily returns to measure risk.

Cumulative Returns: Calculates the growth of a ₹1 investment over time.

Correlation Matrix: Analyzes how different tickers move in relation to each other.

Monthly Performance: Groups data by month to identify granular trends.

# 3. Interactive Streamlit Dashboard
A professional-grade web interface that allows users to toggle between different market views:

Market Summary: High-level metrics (Green vs. Red stock count, Avg Price, Avg Volume).

Rankings: Top 10 Gainers and Top 10 Losers based on yearly performance.

Technical Deep-Dives: Visual charts for Volatility, Sector performance, and Heatmaps.

Monthly Snapshot: A month-slider to view top 5 gainers and losers for specific time periods.

# Business Use Cases
Risk Assessment: Identifying high-volatility stocks for aggressive or conservative portfolios.

Trend Identification: Spotting "Green Stocks" with consistent cumulative growth.

Diversification Support: Using the Correlation Heatmap to ensure a portfolio isn't overly exposed to a single market movement.

Performance Benchmarking: Comparing monthly momentum to identify seasonal trends.

