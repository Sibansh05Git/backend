import pandas as pd
import numpy as np

df = pd.read_csv("crop_recommendation.csv")
df_mean = df.groupby("label").mean()[["N", "P", "K"]]
df_std = df.groupby("label").std()[["N", "P", "K"]]
df_ll = df_mean - 0.3 * df_std
df_ul = df_mean + 0.3 * df_std


def check(n, p, k, label):
    stats = pd.concat([df_ll.loc[[label]].T.rename(columns={label: "lower_limit"}),
                       df_ul.loc[[label]].T.rename(columns={label: "upper_limit"})], axis=1)
    n_ll = stats["lower_limit"].loc["N"]
    p_ll = stats["lower_limit"].loc["P"]
    k_ll = stats["lower_limit"].loc["K"]
    n_ul = stats["upper_limit"].loc["N"]
    p_ul = stats["upper_limit"].loc["P"]
    k_ul = stats["upper_limit"].loc["K"]
    d = dict()
    if n_ll <= n <= n_ul:
        d["N"] = 0
    elif n < n_ll:
        d["N"] = n_ll - n
    else:
        d["N"] = n_ul - n
    if p_ll <= p <= p_ul:
        d["P"] = 0
    elif p < p_ll:
        d["P"] = p_ll - p
    else:
        d["P"] = p_ul - p
    if k_ll <= k <= k_ul:
        d["k"] = 0
    elif k < k_ll:
        d["K"] = k_ll - k
    else:
        d["K"] = k_ul - k
    return d


print(check(2, 3, 100, "rice"))
