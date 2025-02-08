import yfinance as yf
import pandas as pd
import ta
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import streamlit as st

from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

def fetch_and_compute_data():
    # Fetch stock data for Apple Inc. (AAPL)
    data = yf.download("AAPL", period="1d", interval="1m")

    # Ensure 'Close' column is a 1D Series
    close_prices = data['Close'].squeeze()

    # Calculate RSI
    data['RSI'] = RSIIndicator(close=close_prices, window=14).rsi()

    # Calculate SMA
    data['SMA_50'] = SMAIndicator(close=close_prices, window=50).sma_indicator()

    return data


# Function to send email alerts
def send_email(subject, body, to_email):
    from_email = "kolanarjuna@gmail.com"  
    password = "flvwvyqduwjjgcbr"  

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check conditions and send alerts
def check_conditions_and_alert(data):
    print("Checking conditions...")

    if data['RSI'].iloc[-1] < 30:
        print(f"AAPL RSI is {data['RSI'].iloc[-1]}. Sending buy alert...")
        send_email(
            subject="Stock Alert: AAPL is Oversold",
            body=f"AAPL RSI is {data['RSI'].iloc[-1]}. Consider buying.",
            to_email="rithvikreddykolan2002@gmail.com"
        )
    elif data['RSI'].iloc[-1] > 70:
        print(f"AAPL RSI is {data['RSI'].iloc[-1]}. Sending sell alert...")
        send_email(
            subject="Stock Alert: AAPL is Overbought",
            body=f"AAPL RSI is {data['RSI'].iloc[-1]}. Consider selling.",
            to_email="tejenthakkar176@gmail.com"
        )
    else:
        print("No alerts triggered.")

# Function to update data periodically
def update_data():
    print("Fetching new data...")
    data = fetch_and_compute_data()
    check_conditions_and_alert(data)

# Streamlit Dashboard
def run_dashboard():
    st.title("Stock Analysis Dashboard")
    st.write("### Apple Inc. (AAPL)")
    data = fetch_and_compute_data()
    st.write("#### Closing Price")
    st.line_chart(data['Close'])
    st.write("#### RSI (Relative Strength Index)")
    st.line_chart(data['RSI'])
    st.write("#### 50-day Simple Moving Average (SMA)")
    st.line_chart(data['SMA_50'])

# Schedule updates every 10 minutes
schedule.every(10).minutes.do(update_data)

# Main function to run the bot
def main():
    # Run the Streamlit dashboard
    run_dashboard()

    # Run the scheduler in the background
    print("Starting the email alert bot...")

    while True:
        schedule.run_pending()
        print("Scheduler running...")
        time.sleep(1)

if __name__ == "__main__":
    main()
