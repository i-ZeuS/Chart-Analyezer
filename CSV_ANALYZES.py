import pandas as pd
from mplfinance.original_flavor import candlestick2_ochl
import matplotlib.pyplot as plt
import numpy as np
import talib
import mplfinance as mpf
import mysql.connector

# Calculations of technical indicators
def calculate_technical_indicators(df):
    # Calculate RSI
    df['RSI'] = talib.RSI(np.asarray(df['close'].tolist()), timeperiod=14)

    # Calculate MACD
    macd, macdsignal, macdhist = talib.MACD(np.asarray(df['close'].tolist()), fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhistogram'] = macdhist

    # Calculate Bollinger Bands
    df['Close_mavg'] = talib.MA(np.asarray(df['close'].tolist()), timeperiod=20)
    df['Close_stddev'] = talib.STDDEV(np.asarray(df['close'].tolist()), 20)

    df['Upper_band'] = (df['Close_mavg'] + 2 * df['Close_stddev'])
    df['Lower_band'] = (df['Close_mavg'] - 2 * df['Close_stddev'])

    # Assuming you have a 'Volume' column in your DataFrame
    df['Volume'] = df['volume'].round().fillna(0).astype('int64')  # Using 'int64' to handle NaN/inf

    df['Upper_band'] = (df['Close_mavg'] + 2 * df['Close_stddev'])
    df['Lower_band'] = (df['Close_mavg'] - 2 * df['Close_stddev'])  # Adjust accordingly if your column is named differently

    return df

# Plotter of technical indicators
def plot_technical_indicators(df):
    fig, axs = plt.subplots(4, sharex=True, figsize=(10, 8))

    # Plot candlestick chart
    mpf.plot(df, type='candle', ax=axs[0], volume=axs[1], figscale=1.5, tight_layout=True)

    # Plot RSI
    axs_rsi = axs[2].twinx()
    axs_rsi.plot(df.index, df['RSI'], label='RSI', color='blue', linestyle='dashed')
    axs_rsi.set_ylabel('RSI')

    # Plot MACD
    axs[3].plot(df.index, df['macd'])
    axs[3].plot(df.index, df['macdsignal'])
    axs[3].plot(df.index, df['macdhistogram'], color='black', label='Histogram')
    axs[3].set_ylabel('MACD')

    # Plot Bollinger Bands
    axs[3].plot(df.index, df['close'])  # Use axs[3] instead of axs[4]
    axs[3].plot(df.index, df['Upper_band'])
    axs[3].plot(df.index, df['Lower_band'])
    axs[3].set_ylabel('Price')
    axs[3].set_xlabel('Timestamp')

    # Format x-axis to display in days
    axs[3].xaxis.set_major_locator(plt.MaxNLocator(6))  # Adjust the number of ticks as needed

    # Set title and labels
    plt.suptitle("Technical Indicators")
    plt.tight_layout()

    axs_rsi.legend(loc='upper left')

    plt.show()

#The main Program
def main():
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host='<HOST_IP>',
        user='<USERNAME>',
        password='<PASSWORD>',
        database='<DATABASE_NAME>'
    )

    # SQL query to retrieve data
    query = "SELECT * FROM <table_name>;"

    # Read timedata from MySQL into a DataFrame
    df = pd.read_sql(query, connection, index_col='timestamp', parse_dates=True)

    # Close the database connection
    connection.close()

    # Ensure that the index is a DatetimeIndex
    df.index = pd.to_datetime(df.index)

    df = calculate_technical_indicators(df)

    # Plot the technical indicators
    plot_technical_indicators(df)

if __name__ == "__main__":
    main()
