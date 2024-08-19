import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="🎀 Il's Trading Assistant")

# List of popular stocks with cute emojis
popular_stocks = [
    "🍎 AAPL", "🪟 MSFT", "📦 AMZN", "🔍 GOOGL", "👥 FB", "🚗 TSLA", "🎮 NVDA"
]

def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker.split()[-1])  # Remove emoji
    data = stock.history(start=start_date, end=end_date)
    return data['Close']

def main():
    st.title("🎀 Il's Trading Assistant")
    st.markdown("---")

    # Sidebar for user inputs
    st.sidebar.header("📈 Pick your stocks")

    stock1 = st.sidebar.selectbox("First stock:", popular_stocks, index=0)
    stock2 = st.sidebar.selectbox("Second stock:", popular_stocks, index=1)

    # allow user to enter stocks manually
    if st.sidebar.checkbox("🔍 Search for your own stocks"):
        stock1 = st.sidebar.text_input("First stock:")
        stock2 = st.sidebar.text_input("Second stock:")
        stock1 = stock1.upper()
        stock2 = stock2.upper()

    st.sidebar.header("📅 When shall we look?")
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date:")
    end_date = col2.date_input("End date:")

    if st.sidebar.button("✨ Analyze", key="analyze"):
        if stock1 and stock2:
            # Fetch stock data
            with st.spinner(f"Fetching data for {stock1} and {stock2}..."):
                df1 = get_stock_data(stock1, start_date, end_date)
                df2 = get_stock_data(stock2, start_date, end_date)

            # Combine data
            df = pd.concat([df1, df2], axis=1)
            df.columns = [stock1.split()[-1], stock2.split()[-1]]  # Remove emoji

            # Calculate correlation
            correlation = df[df.columns[0]].corr(df[df.columns[1]])

            # Display correlation
            st.header(f"💕 Correlation between {stock1.split()[-1]} and {stock2.split()[-1]}")
            st.metric(label="Correlation coefficient", value=f"{correlation:.2f}")

            # Plot stock prices
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df[df.columns[0]], name=stock1.split()[-1], line=dict(color="#ff9999")))
            fig.add_trace(go.Scatter(x=df.index, y=df[df.columns[1]], name=stock2.split()[-1], line=dict(color="#66b3ff")))
            fig.update_layout(
                title=f"💰 {stock1.split()[-1]} vs {stock2.split()[-1]} Plot",
                xaxis_title="Date",
                yaxis_title="Price",
                legend_title="Stocks",
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Custom summary statistics
            summary_stats = {
                stock1.split()[-1]: {
                    "Mean": df[stock1.split()[-1]].mean(),
                    "Standard Deviation": df[stock1.split()[-1]].std(),
                    "Minimum": df[stock1.split()[-1]].min(),
                    "Maximum": df[stock1.split()[-1]].max()
                },
                stock2.split()[-1]: {
                    "Mean": df[stock2.split()[-1]].mean(),
                    "Standard Deviation": df[stock2.split()[-1]].std(),
                    "Minimum": df[stock2.split()[-1]].min(),
                    "Maximum": df[stock2.split()[-1]].max()
                }
            }

            # Display summary statistics
            st.header("📊 Summary Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(stock1)
                st.write(pd.DataFrame(summary_stats[stock1.split()[-1]], index=["Values"]))

            with col2:
                st.subheader(stock2)
                st.write(pd.DataFrame(summary_stats[stock2.split()[-1]], index=["Values"]))

if __name__ == "__main__":
    main()