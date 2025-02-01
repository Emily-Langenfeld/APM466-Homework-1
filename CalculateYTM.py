import pandas as pd
import numpy as np
import numpy_financial as npf
from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_number_of_coupon_payments(maturity_date, date):
    coupon_count = -1
    while maturity_date > date:
        coupon_count = coupon_count + 1
        maturity_date = maturity_date - relativedelta(months=6)

    return coupon_count


def calculate_ytm(df):
    df["NUMBER COUPONS"] = df.apply(lambda row: calculate_number_of_coupon_payments(row["MATURITY DATE"],
                                                                                    row["DATE"]), axis=1)
    df["YTM"] = None
    for i in range(len(df)):
        coupon_num = df.iloc[i]["NUMBER COUPONS"]
        coupon = (df.iloc[i]["COUPON"])/2
        cashflow = [-df.iloc[i]["DIRTY PRICE"]] + [coupon]*coupon_num
        cashflow.append(100+coupon)
        df.loc[i, "YTM"] = npf.irr(cashflow)
    return df

