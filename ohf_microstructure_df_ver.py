import random
import ohf_utilities as ohf
import numpy as np
import math
import pandas as pd

# ticker list
data_ticker = pd.read_csv('copartnership_data.csv', sep=';')
data = pd.read_csv('dane.csv', sep=';')
df = data[['Unnamed: 0', 'Data sesji', 'Close']]
b = df.copy()
b.loc[:, ('Close')] = df['Close'].transform(lambda x: x.replace(" ", "").replace(",", ".")).astype(float, errors='raise')
B = b[df["Unnamed: 0"].str.contains('11B', case=False)]

ticker = B['Close']
for i in range(1):
    # df = ohf.database_connection(i)
    df = ticker

    # choose parameters
    # Wealth
    pnl = [0]

    # cash
    c = [0]
    cash = df

    # market maker
    k = 1.5

    # reserve price
    r = []

    # inventory
    q = [0]

    # transactions
    t = 0

    # hold time of the same position
    hold_time = []

    # hold time of one postion
    p_time = 0

    # time of not being in a position
    n_p_time = []

    # position == 0
    n_p = 0

    max_q_held = 0
    min_q_held = 0

    # risk = 0 -> high risk; risk = 1 -> low risk
    risk_parameter = 0.001

    ra = []
    rb = []

    for n in cash.index:
        # Reserve price
        r.append(cash[n] - q[n] * risk_parameter)

        # Reserve spread
        r_spread = 2 / risk_parameter * math.log(1 + risk_parameter / k)

        # reserve price bid and ask
        r_ask = r[n] + r_spread / 2
        r_bid = r[n] - r_spread / 2
        ra.append(r_ask)
        rb.append(r_bid)

        # reserve delta
        delta_a = r_ask - cash[n]
        delta_b = cash[n] - r_bid

        # Intensities
        lambda_a = math.exp(-k*delta_a)
        lambda_b = math.exp(-k*delta_b)

        # order consumption
        ya = random.random()
        yb = random.random()

        dNa = 0
        dNb = 0

        prob_ask = 1 - math.exp(-lambda_a)
        prob_bid = 1 - math.exp(-lambda_b)

        if ya < prob_ask:
            dNa = 1
        if yb < prob_bid:
            dNb = 1

        # update variables
        q.append(q[n] - dNa + dNb)
        c.append(c[n] + r_ask * dNa - r_bid * dNb)
        pnl.append(c[n+1] + q[n+1] * cash[n])

        # count transactions
        if q[n-1] != q[n]:
            t += 1

        # count days not being in a position
        if q[n] == 0:
            n_p += 1
        elif q[n] != 0 and q[n-1] == 0:
            n_p_time.append(n_p)
            n_p = 0

        # how much time does it hold it's position
        if q[n-1] == q[n]:
            p_time += 1
        elif q[n-1] != q[n]:
            hold_time.append(p_time)
            p_time = 1

        # update min/max inventory
        if q[n+1] > max_q_held:
            max_q_held = q[n+1]
        if q[n+1] < min_q_held:
            min_q_held = q[n+1]

    print(f'Ticker: {i}')
    print("Final inventory hold: ", q[-1])
    print(f"Number of transactions: {t}")
    print(f"Average Time in one postion: {np.mean(hold_time)}")
    print(f'Cash: {c[-1]}')
    print(f'Final Wealth: {pnl[-1]}')
    print(f'Max q held: {max_q_held}')
    print(f'Min q held: {min_q_held}')
    print(f'Average Inventory: {np.mean(q)}')
    print(f'Average Wealth: {np.mean(pnl)}')
    print(f'Average days of not holding position: {int(np.mean(n_p_time))}\n')

ohf.plot_sim(cash, r, ra, rb, pnl, q)
