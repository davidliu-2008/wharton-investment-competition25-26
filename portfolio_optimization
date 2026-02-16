import numpy as np
import matplotlib.pyplot as plt

#config params
init_inv = 500000
goal = 1500000
yrs = 10
iters = 2000 
drawdown = 10000
start_yr = 3

#defensive playbook (agg, jnj)
mu_def = 0.07 
sig_def = 0.08 

#offensive playbook (nvda, s, fslr)
mu_off = 0.16
sig_off = 0.28

def run_split_sim(def_w):
    off_w = 1.0 - def_w
    wins = 0
    
    for _ in range(iters):
        val = init_inv
        t = 0
        while t < yrs:
            #get monthly returns
            r_d = np.random.normal(mu_def/12, sig_def/np.sqrt(12))
            r_o = np.random.normal(mu_off/12, sig_off/np.sqrt(12))
            
            #calc weighted portolio growth
            chg = (def_w * r_d) + (off_w * r_o)
            val *= (1 + chg)
            
            #apply community payout (>= 10k)
            if t >= start_yr:
                val -= (drawdown / 12)
            
            if val <= 0: break
            t += 1/12
            
        #check if met barwins goal
        if val >= goal:
            wins += 1
            
    return (wins / iters) * 100

#test range of weights for linebacker strategy
test_weights = np.linspace(0, 1, 11) 
results = []

for w in test_weights:
    pct = run_split_sim(w)
    results.append(pct)
    #log results for analysis
    print(f"def {int(w*100)}% / off {int((1-w)*100)}%: {pct:.1f}% success")

#plot results
plt.figure(figsize=(10, 6))
plt.plot(test_weights * 100, results, marker='o', color='#003366')

#mark the 60/40 linebacker split & 85% success line
plt.axvline(x=60, color='red', ls='--')
plt.axhline(y=85, color='green', ls=':')

plt.title("success prob vs defensive weight", fontweight='bold')
plt.xlabel("defensive playbook %")
plt.ylabel("success prob %")
plt.grid(alpha=0.3)
plt.show()
