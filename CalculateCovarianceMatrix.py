import numpy as np

# We choose the 5 bonds that mature in March.


def calculate_cov_matrix(d, fwr):
    list_of_ytm = []
    filtered_bonds = []
    for df in d:
        bonds = d[df]
        # filtered_bonds.append(bonds[bonds['MATURITY DATE'].dt.month != 9])
        filtered_bonds.append(bonds.iloc[0:5])

    for i in filtered_bonds:
        ytms = []
        i['YTM'].apply(lambda x: ytms.append(x))
        list_of_ytm.append(ytms)

    log_returns_y = []
    for ytms in list_of_ytm:
        log_return = []
        for i in range(len(ytms) - 1):
            log_return.append(np.log((ytms[i+1]-ytms[i])/ytms[i]))
        log_returns_y.append(log_return)

    log_returns_f = []
    for forwards in fwr:
        log_return = []
        for i in range(len(forwards)-1):
            log_return.append(np.log((forwards[i+1]-forwards[i])/forwards[i]))
        log_returns_f.append(log_return)

    log_returns_arr = np.array(log_returns_y).T
    forward_returns_arr = np.array(log_returns_f).T
    yield_cov = np.cov(log_returns_arr)
    forward_cov = np.cov(forward_returns_arr)

    return yield_cov, forward_cov
