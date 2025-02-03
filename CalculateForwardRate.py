def calculate_fraction_year(maturity, date):
    days_diff = (maturity - date).days
    return days_diff/365


def interpolate(days_diff1, days_diff2, spot1, spot2, x):
    diff = days_diff2 - days_diff1
    interpolated_rate = ((days_diff2 - x)/diff)*spot1 + ((x - days_diff1)/diff)*spot2
    return interpolated_rate


def calculate_forward_rates(df):
    interpolated_spot = []
    i = 1
    spot = 1
    while i < len(df):
        bond1 = [df.iloc[i]["MATURITY DATE"], df.iloc[i]["DATE"], df.iloc[i]["SPOT RATES"]]
        bond2 = [df.iloc[i + 1]["MATURITY DATE"], df.iloc[i + 1]["DATE"], df.iloc[i + 1]["SPOT RATES"]]
        days_diff_1 = calculate_fraction_year(bond1[0], bond1[1])
        days_diff_2 = calculate_fraction_year(bond2[0], bond2[1])
        interpolated_spot.append(interpolate(days_diff_1, days_diff_2, bond1[2], bond2[2], spot))
        spot = spot + 1
        i = i + 2

    forward_rates = []
    i = 1
    while i < len(interpolated_spot):
        forward_rate = ((1+interpolated_spot[i])**(2*i)/(1+interpolated_spot[0]))**(1/(2*i)) - 1
        forward_rates.append(forward_rate)
        i = i + 1

    return forward_rates
