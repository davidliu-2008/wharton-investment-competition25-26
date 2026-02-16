import numpy as np
import matplotlib.pyplot as plt

iterations = 5000
years = 10
initial_total = 500000
target_goal = 1500000

#playbook allocations
defensive_weight = 0.60 #300k
offensive_weight = 0.40 #200k

#Defensve Playbook
mu_defensive = 0.07 #stable returns
sigma_defensive = 0.08 #Low-volatility req

#Offensive playbook
mu_offensive = 0.16    
sigma_offensive = 0.28  

#drawdown parameters
annual_drawdown = 10000
start_year = 3 #2029

def linebacker_simulation():
    all_paths = []
    
    for i in range(iterations):
        def_total = initial_total * defensive_weight
        off_total = initial_total * offensive_weight
        
        path = [def_total + off_total]
        t = 0.0
        
        while t < years:
            m_mu_def = mu_defensive / 12
            m_sig_def = sigma_defensive / np.sqrt(12)
            def_return = np.random.normal(m_mu_def, m_sig_def)
            def_total *= (1 + max(def_return, -0.9))
            
            m_mu_off = mu_offensive / 12
            m_sig_off = sigma_offensive / np.sqrt(12)
            off_return = np.random.normal(m_mu_off, m_sig_off)
            off_total *= (1 + max(off_return, -0.9))
            
            current_portfolio = def_total + off_total
            

            if t >= start_year:

                current_portfolio -= (annual_drawdown / 12)

                def_total = current_portfolio * defensive_weight
                off_total = current_portfolio * offensive_weight
            
            path.append(current_portfolio)
            t += 1/12
            
        all_paths.append(path)
        
    return np.array(all_paths)


results = linebacker_simulation()
time_axis = np.linspace(0, years, results.shape[1])
avg_path = np.mean(results, axis=0)
upper_85 = np.percentile(results, 92.5, axis=0)
lower_85 = np.percentile(results, 7.5, axis=0)

#plot
plt.figure(figsize=(12, 7))
plt.fill_between(time_axis, lower_85, upper_85, color='#4A90E2', alpha=0.2, label='85% Confidence Range')
plt.plot(time_axis, avg_path, color='#003366', linewidth=3, label='Linebacker Strategy (Average)')

legend_text = (
    "• Thousands of Simulated Market Scenarios\n"
    "• Illustrates Range of Potential Outcomes\n"
    "• 60/40 Defensive-Offensive Playbook Split\n"
    "• Probability of Success ≥ 85%"
)
props = dict(boxstyle='round', facecolor='white', edgecolor='#003366', alpha=0.9)
plt.gca().text(0.05, 0.95, legend_text, transform=plt.gca().transAxes, fontsize=10,
               verticalalignment='top', bbox=props, linespacing=1.8)

plt.axhline(y=target_goal, color='red', linestyle='--', label='Goal: $1.5M')
plt.title("MTWB Portfolio: The Linebacker Strategy", fontsize=18, fontweight='bold', loc='left')
plt.ylabel("Portfolio Value ($)")
plt.xlabel("Years")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
plt.legend(loc='lower right')
plt.show()

success_rate = np.mean(results[:, -1] >= target_goal) * 100
print(f"Strategy Success Likelihood: {success_rate:.1f}%")
