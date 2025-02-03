
def bootstrap_yield_curve(bonds):
    spot_rates = []

    for bond in bonds:
        price = bond[0]
        coupon = bond[1]
        periods = bond[2]
        if periods == 1:
            spot_rate = ((100+coupon)/price)**(1/periods)-1
            spot_rates.append(spot_rate)
        else:
            disc_cf = 0
            for i in range(periods - 1):
                disc_cf = disc_cf + (coupon/((1 + spot_rates[i])**i))
            spot_rate = ((100+coupon)/(price-disc_cf))**(1/periods)-1
            spot_rates.append(spot_rate)

    spot_rates_annual = []
    for i in spot_rates:
        spot_rates_annual.append(i*2)

    return spot_rates_annual


def calculate_spot_rate(df):
    bonds = []
    for i in range(len(df)):
        bond = (df.iloc[i]["DIRTY PRICE"], df.iloc[i]["COUPON"]/2, df.iloc[i]["NUMBER COUPONS"] + 1)
        bonds.append(bond)
    spot_rates = bootstrap_yield_curve(bonds)
    df["SPOT RATES"] = spot_rates
    return df
