import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import math


def database_connection(ticker) -> pd.DataFrame:
    """
    :ticker company ticker

    :returns DataFrame with company data
    """
    try:
        db = mysql.connector.connect(
            user="fellow",
            password="fellow2021",
            host="51.83.129.54",
            port=3306,
            database="fellowshippl"
        )

    except Error as e:
        print("Error while connecting to MySQL", e)

    curs = db.cursor()
    conditions = f"SELECT session_date ,close FROM olhc WHERE ticker = '{ticker.upper()}'"
    curs.execute(conditions)

    data = []
    for x in curs:
        data.append(x)

    df = pd.DataFrame(data, columns=['date', 'close'])
    return df


"""
jeżeli stracę więcej niż x złotych, to przerwij obliczenia


DRAWDOWN 
"""


def bollinger_bands(data):
    """
    :data DF containing company close price data

    :returns plot and calculate bollinger bands
    """
    moving_average = []
    bandwidth = []
    for x in data.index:
        index = x + 20
        if index <= data.index.max():
            avg = data['close'].rolling(window=20).mean().iloc[x:index]
            moving_average.append(avg.iloc[-1])
            std = np.std(data['close'].iloc[x:index])
            bandwidth.append(std)

    maximum = np.array(bandwidth) + np.array(moving_average)
    max_bandwidth = pd.DataFrame(maximum, columns=['max'])
    minimum = np.array(moving_average) - np.array(bandwidth)
    min_bandwidth = pd.DataFrame(minimum, columns=['min'])
    df_average = pd.DataFrame(moving_average, columns=['average'])
    # df_std = pd.DataFrame(bandwidth, columns=['std'])

    plt.plot(max_bandwidth, label='max')
    plt.plot(min_bandwidth, label='min')
    plt.plot(df_average, label='avg')
    plt.plot(data['close'], label='price')
    plt.legend(loc='upper left')
    plt.show()


def plot_sim(cash, r, ra, rb, pnl, q):
    """


    :param cash: price of stocks
    :param r: Reserve price
    :param ra: reserve price ask
    :param rb: reserve price bid
    :param pnl: Wealth
    :param q: inventory
    :return: plot result of simulation
    """
    f = plt.figure(figsize=(15, 4))
    f.add_subplot(1, 3, 1)
    plt.plot(cash, color='black', label='price')
    plt.plot(r, color='blue', label='Reservation price')
    plt.plot(ra, color='red', linestyle='', marker='.', label='price asked', markersize='4')
    plt.plot(rb, color='lime', linestyle='', marker='o', label='Price bid', markersize='2')
    plt.legend()

    f.add_subplot(1, 3, 2)
    plt.plot(pnl[:-1], color='black', label='PNL')
    plt.xlabel('Time')
    plt.ylabel('PnL [ZL]')
    plt.grid(True)
    plt.legend()

    f.add_subplot(1, 3, 3)
    plt.plot(q[:-1], color='black', label='stocks held')
    plt.xlabel('Time')
    plt.ylabel('Inventory')
    plt.grid(True)
    plt.legend()

    plt.show()
