import pandas as pd
import numpy as np
import numpy_financial as npf
from datetime import datetime
from dateutil.relativedelta import relativedelta

def bootstrap_yield_curve(bonds):
    spot_rates = np.zeros(len(bonds))

    for i, (price, coupon_rate, maturity) in enumerate(sorted(bonds, key=lambda x: x[2])):
        cash_flows = np.array([coupon_rate] * int(maturity - 1) + [100 + coupon_rate])
        time_periods = np.arange(1, maturity + 1)
        # Use previously calculated spot rates for discounted cash flows
        if i == 0:
            discounted_cash_flows = cash_flows / (1 + spot_rates[i])**time_periods
        else:
            discounted_cash_flows = [cf / (1 + spot_rates[j])**time_periods[j] for j, cf in enumerate(cash_flows)]
            discounted_cash_flows = np.sum(discounted_cash_flows)

        residual = price - discounted_cash_flows
        if residual <= 0:
            # Handle cases where residual is too low
            print(f"Warning: Residual for bond with maturity {maturity} is too low. Adjusting spot rate calculation.")
            spot_rate = spot_rates[i-1]  # Use previous spot rate as an approximation
        else:
            spot_rate = ((100 / residual)**(1 / maturity)) - 1
        spot_rates[i] = spot_rate

    return spot_rates


def calculate_spot_rate(df):
    # bonds = []
    # for i in range(len(df)):
    #     bond = (df.iloc[i]["DIRTY PRICE"], df.iloc[i]["COUPON"]/2, df.iloc[i]["NUMBER COUPONS"] + 1)
    #     bonds.append(bond)
    bonds = [
        (95, 1, 1),
        (190, 1.5, 2),
        (188, 2, 3)]
    spot_rates = bootstrap_yield_curve(bonds)
    return spot_rates
