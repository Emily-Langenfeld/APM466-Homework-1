import pandas as pd
import numpy as np
import numpy_financial as npf
from CalculateDirtyPrice import calculate_dirty_price
from CalculateYTM import calculate_ytm
from CalculateSpotRate import calculate_spot_rate
import matplotlib.pylab as plt


d = {}
spot_rates = []

for i in [6, 7, 8, 9, 10, 13, 14, 15, 16, 17]:
    bonds = pd.read_excel("/Users/emily/Desktop/10_Bonds.xlsx", sheet_name="{0}".format(i))
    bonds = calculate_dirty_price(bonds)
    bonds = calculate_ytm(bonds)
    # spot_rates.append(calculate_spot_rate(bonds))
    d["{0}".format(i)] = bonds[["DIRTY PRICE", "COUPON", "MATURITY DATE", "DATE", "YTM"]]
    lin_label = bonds.iloc[0]["DATE"].strftime('%Y-%m-%d')
    plt.plot(bonds["MATURITY DATE"].dt.strftime('%Y-%m'), bonds["YTM"], label=lin_label)

plt.xlabel("Maturity Dates")
plt.ylabel("YTM")
plt.title("YTM-curve")
plt.legend()
plt.show()

if __name__ == '__main__':
    print(bonds["MATURITY DATE"])

