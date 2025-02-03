import pandas as pd
import numpy as np
import numpy_financial as npf
from CalculateDirtyPrice import calculate_dirty_price
from CalculateYTM import calculate_ytm, calculate_number_of_coupon_payments
from CalculateSpotRate import calculate_spot_rate
from CalculateForwardRate import calculate_forward_rates
from CalculateCovarianceMatrix import calculate_cov_matrix
import matplotlib.pylab as plt
from numpy.linalg import eig

d = {}
forward_rates = {}

for i in [6, 7, 8, 9, 10, 13, 14, 15, 16, 17]:
    bonds = pd.read_excel("/Users/emily/Desktop/10_Bonds.xlsx", sheet_name="{0}".format(i))
    bonds['MATURITY DATE'] = pd.to_datetime(bonds['MATURITY DATE'], errors='coerce')
    bonds['DATE'] = pd.to_datetime(bonds['DATE'], errors='coerce')
    bonds = calculate_dirty_price(bonds)
    bonds = calculate_ytm(bonds)
    bonds = calculate_spot_rate(bonds)
    forward_rates[bonds.iloc[0]["DATE"]] = calculate_forward_rates(bonds)
    d["{0}".format(i)] = bonds[["DIRTY PRICE", "COUPON", "MATURITY DATE", "DATE", "YTM", "SPOT RATES"]]


def plot_ytm(d):
    for i in [6, 7, 8, 9, 10, 13, 14, 15, 16, 17]:
        bonds = d["{0}".format(i)]
        lin_label = bonds.iloc[0]["DATE"].strftime('%Y-%m-%d')
        plt.plot(bonds["MATURITY DATE"].dt.strftime('%Y-%m'), bonds["YTM"]*100, label=lin_label)
    plt.xlabel("Maturity Dates")
    plt.ylabel("YTM")
    plt.title("YTM-curve")
    plt.legend()
    plt.show()


def plot_spot_rates(d):
    for i in [6, 7, 8, 9, 10, 13, 14, 15, 16, 17]:
        bonds = d["{0}".format(i)]
        lin_label = bonds.iloc[0]["DATE"].strftime('%Y-%m-%d')
        plt.plot(bonds["MATURITY DATE"].dt.strftime('%Y-%m'), bonds["SPOT RATES"]*100, label=lin_label)
    plt.xlabel("Maturity Dates")
    plt.ylabel("Spot rates")
    plt.title("Spot-curve")
    plt.legend()
    plt.show()


def plot_forward_rates(fwr):
    for i in fwr:
        fwr_percent = []
        for j in fwr[i]:
            fwr_percent.append(j*100)
        lin_label = i.strftime("%Y-%m-%d")
        plt.plot(["1yr-1yr", "1yr-2yr", "1yr-3yr", "1yr-4yr"], fwr_percent, label=lin_label)
    plt.ylabel("Forward Rates")
    plt.title("1-year forward curve")
    plt.legend()
    plt.show()


def create_list_from_dic(d):
    lst = []
    for i in d:
        lst.append(d[i])
    return lst


yield_cov, forward_cov = calculate_cov_matrix(d, create_list_from_dic(forward_rates))
eigenval_yield, eigenvec_yield = eig(yield_cov)
eigenval_forward, eigenvec_forward = eig(forward_cov)


if __name__ == '__main__':
    plot_forward_rates(forward_rates)
    plot_spot_rates(d)
    plot_ytm(d)
    print(yield_cov)
    print(forward_cov)
    print(eigenval_yield)
    print(eigenvec_yield)
    print(eigenval_forward)
    print(eigenvec_forward)
