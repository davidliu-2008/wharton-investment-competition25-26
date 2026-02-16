import numpy as np
import pandas as pd


yrs = 10
n_sims = 5000 
init_inv = 500000
drawdown = 10000
start_yr = 3
def_total_port_pct = 0.60 

play_port_weights = {
    "ig_bonds": 0.15,
    "intl_esg": 0.14,
    "essential_svc": 0.145,
    "low_vol_equity": 0.165
}


assets_data = {
    "AGG":  {"m": 0.045, "v": 0.05, "p": "ig_bonds"},
    "BND":  {"m": 0.045, "v": 0.05, "p": "ig_bonds"},
    "VCIT": {"m": 0.050, "v": 0.07, "p": "ig_bonds"},
    "BNDX": {"m": 0.040, "v": 0.06, "p": "ig_bonds"},
    "ESGD": {"m": 0.070, "v": 0.15, "p": "intl_esg"},
    "ESGV": {"m": 0.080, "v": 0.16, "p": "intl_esg"},
    "VEA":  {"m": 0.070, "v": 0.15, "p": "intl_esg"},
    "VEU":  {"m": 0.070, "v": 0.15, "p": "intl_esg"},
    "XLU":  {"m": 0.065, "v": 0.13, "p": "essential_svc"},
    "XLP":  {"m": 0.060, "v": 0.12, "p": "essential_svc"},
    "PAVE": {"m": 0.085, "v": 0.18, "p": "essential_svc"},
    "SCHD": {"m": 0.090, "v": 0.13, "p": "low_vol_equity"},
    "VIG":  {"m": 0.085, "v": 0.12, "p": "low_vol_equity"},
    "VTV":  {"m": 0.080, "v": 0.13, "p": "low_vol_equity"},
    "JNJ":  {"m": 0.070, "v": 0.10, "p": "low_vol_equity"},
    "USMV": {"m": 0.075, "v": 0.11, "p": "low_vol_equity"},
    "QUAL": {"m": 0.090, "v": 0.14, "p": "low_vol_equity"}
}

tickers = list(assets_data.keys())
n_assets = len(tickers)

def run_mc_sim(weights):
    wins = 0
    for _ in range(n_sims):
        val = init_inv
        for y in range(yrs):
            ann_ret = 0
            for i, tkr in enumerate(tickers):
                sim_ret = np.random.normal(assets_data[tkr]["m"], assets_data[tkr]["v"])
                #weights here are relative to the 60% defensive sleeve
                ann_ret += weights[i] * sim_ret * def_total_port_pct 
            
            ann_ret += (0.40 * 0.12) 
        
            val *= (1 + ann_ret)
            if y >= start_yr: val -= drawdown
            if val <= 0: break
        if val >= 1000000: wins += 1 
    return wins / n_sims


base_w = np.array([1/n_assets]*n_assets)
base_p = run_mc_sim(base_w)
delta_p = []

for i, tkr in enumerate(tickers):
    tw = base_w.copy()
    tw[i] = 0
    tw = tw / np.sum(tw)
    delta_p.append(max(0.001, base_p - run_mc_sim(tw)))


df = pd.DataFrame({
    "ticker": tickers,
    "play": [assets_data[t]["p"] for t in tickers],
    "marginal_contrib": delta_p 
})

#divide marginal contribution by total play contribution (get share of play)
df['play_total_contrib'] = df.groupby('play')['marginal_contrib'].transform('sum')
df['share_of_play'] = df['marginal_contrib'] / df['play_total_contrib'] 


df['play_port_pct'] = df['play'].map(play_port_weights)
df['final_weight'] = df['share_of_play'] * df['play_port_pct'] 


df['dollar_allocation'] = df['final_weight'] * init_inv

print(df[['ticker', 'play', 'marginal_contrib', 'share_of_play', 'final_weight', 'dollar_allocation']])
