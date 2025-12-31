# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:16:36 2024

@author: ASUS
"""
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import numpy as np
Discount=pd.read_csv("/Users/ASUS/Desktop/Project728/0203.csv")
Discount
DF=[Discount[Discount.Term==x].Discount.values[0] for x in ['12 MO', "2 YR"]]
DF
PV=1/2*DF[0]+1/2*DF[1]

df=pd.read_excel('/Users/ASUS/Desktop/Project728/Fixed to LIBOR Swap.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
start_date = '2020-02-01'
end_date = '2020-04-30'
df = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

df['Unhedged_PnL'] = df['Last Price'].diff()
df['Unhedged_Value'] = df['Unhedged_PnL'].cumsum()
df.loc[220,'Unhedged_Value']=0

S=[1.4835,1.5169,1.5339,1.3021,1.154,0.6226,0.7518,0.7129,0.7285]
K=[1.26,1.29,1.33,1.1,0.87,0.44,0.39,0.35,0.32]
sigma=list(np.array([61.79,58.19,65,79,64.88,71.1,60.36,50.5,48.85,50.81])/100)
start=['2020-02-03','2020-02-10','2020-02-17','2020-02-24','2020-03-02','2020-03-09','2020-03-16','2020-03-23','2020-03-30']

T=1
d1=[1/(norm.cdf((np.log(S/K)+0.5*sigma**2*T)/sigma/T**0.5) )for S,K,sigma in zip(S,K,sigma)]
quantity = [abs(d1[i] - d1[i - 1]) if i > 0 else d1[i] for i in range(len(d1))]

swaption_price=[-PV*(S*norm.cdf(-1*((np.log(S/K)+0.5*sigma**2*T)/sigma/T**0.5))-K*norm.cdf(-1*((np.log(S/K)+0.5*sigma**2*T)/sigma/T**0.5-sigma*T**0.5))) for S, K,sigma in zip(S,K,sigma)]

def hedge(quantity,K,start,sigma,swaption_price):
    new_df = pd.DataFrame({'Date': df.Date,'Value':0})
    S0=df[df['Date'] == start]["Last Price"].values[0]
    price0=S0*norm.cdf((np.log(S0/K)+0.5*sigma**2*T)/sigma/T**0.5)-K*norm.cdf((np.log(S0/K)+0.5*sigma**2*T)/sigma/T**0.5-sigma*T**0.5)
    new_df.loc[new_df['Date'] > start, 'Value'] = quantity*(price0-df[df['Date']>start].copy()['Last Price'].apply(lambda x:x*norm.cdf((np.log(x/K)+0.5*sigma**2*T)/sigma/T**0.5)-K*norm.cdf((np.log(x/K)+0.5*sigma**2*T)/sigma/T**0.5-sigma*T**0.5)  ) )    
    return new_df

hedge1=hedge(quantity[0],K[0],start[0],sigma[0],swaption_price[0])
hedge2=hedge(quantity[1],K[1],start[1],sigma[1],swaption_price[1])
hedge3=hedge(quantity[2],K[2],start[2],sigma[2],swaption_price[2])
hedge4=hedge(quantity[3],K[3],start[3],sigma[3],swaption_price[3])
hedge5=hedge(quantity[4],K[4],start[4],sigma[4],swaption_price[4])
hedge6=hedge(quantity[5],K[5],start[5],sigma[5],swaption_price[5])
hedge7=hedge(quantity[6],K[6],start[6],sigma[6],swaption_price[6])
hedge8=hedge(quantity[7],K[7],start[7],sigma[7],swaption_price[7])
hedge9=hedge(quantity[8],K[8],start[8],sigma[8],swaption_price[8])
# Hedge once
df['Hedged_Value']=df['Unhedged_Value']+hedge1['Value']#-quantity[0]*swaption_price[0]
df['Hedged_PnL']=df['Hedged_Value'].diff()

# Hedge every week
df['Weekly Hedge Value']=df['Unhedged_Value']+hedge1['Value']+hedge2['Value']+hedge3['Value']+hedge4['Value']+hedge5['Value']+hedge6['Value']+hedge7['Value']+hedge8['Value']+hedge9['Value']#-sum(np.array(swaption_price)*np.array(quantity))
df['Weekly hedge PnL']=df['Weekly Hedge Value'].diff()

# Hedge every month
q=d1[4]-d1[0]
hedge_m=hedge(q,K[4],start[4],sigma[4],swaption_price[4])
df['Monthly Hedged_Value']=df['Unhedged_Value']+hedge1['Value']+hedge_m['Value']#-quantity[0]*swaption_price[0]-quantity[4]*swaption_price[4]
df['Monthly Hedged_PnL']=df['Monthly Hedged_Value'].diff()

# Total Value Plot
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Unhedged_Value'], label='Unhedged Portfolio Value')
plt.plot(df['Date'], df['Hedged_Value'], label='Hedged Onced Portfolio value')
plt.plot(df['Date'], df['Monthly Hedged_Value'], label='Monthly Hedged Portfolio Value')
plt.plot(df['Date'], df['Weekly Hedge Value'], label='Weekly Hedged Portfolio Value')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Portfolio Value')
plt.legend()
plt.grid(True)
plt.show()

# Daily PnL plot
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Unhedged_PnL'], label='Unhedged PnL')
plt.plot(df['Date'], df['Hedged_PnL'], label='hedged PnL')
plt.plot(df['Date'], df['Monthly Hedged_PnL'], label='Monthly hedged PnL')
plt.plot(df['Date'], df['Weekly hedge PnL'], label='Weekly hedged PnL')
plt.xlabel('Date')
plt.ylabel('PnL')
plt.title('PnL')
plt.legend()
plt.grid(True)
plt.show()

# Density Plot
plt.figure(figsize=(10, 5))
df['Unhedged_PnL'].plot(kind='density', label='Unhedged PnL')
df['Hedged_PnL'].plot(kind='density', label='Hedged PnL')
df['Monthly Hedged_PnL'].plot(kind='density', label='Monthly Hedged PnL')
df['Weekly hedge PnL'].plot(kind='density', label='Weekly Hedged PnL')
plt.legend()
plt.title('Density Plot of PnL')
plt.xlabel('PnL')
plt.show()