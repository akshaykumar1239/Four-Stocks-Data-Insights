#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# loading the exercise file

df = pd.read_excel('/Users/akshaykumar1239/Downloads/Excercise.xlsx')
df.head(10)


# In[3]:


# I can see some duplicates, so removing duplicates

df.drop_duplicates(inplace = True)
df.head(7)


# In[4]:


# to get data for ABC stocks, I can just pivot the table

df_ABC = df.pivot_table(index=['Date','Tick'], columns='XYZ', values='Value')
df_ABC


# In[5]:


# resetting the index

df_ABC.reset_index(inplace = True)
df_ABC


# In[6]:


# there's no data for B and C on 31st January

df_ABC.isnull().sum()


# In[7]:


df_ABC


# In[8]:


df_D = df.drop(['XYZ', "Value"], axis = 1)
df_D


# In[9]:


# removed all the duplicates and only kept positive values

df_D.drop_duplicates(inplace = True)
df_D = df_D[df_D['D'] != 0]
df_D


# In[10]:


df_D.isnull().sum()


# In[ ]:





# # My step-1 is complete here

# In[11]:


# so to not lose that data I used inner join
# A has 375 extra data points that can be useful so instead of losing that data
# I'm gonna use outer joint

df = df_ABC.merge(df_D, how = 'outer', on = ['Date', 'Tick'])
df


# In[12]:


# I need the last tick data 
# I just wanted to add a index column to later use in merging

last_tick = df[df['Tick'] == df['Tick'].max()]
last_tick.reset_index(inplace = True, drop = True)
last_tick.reset_index(inplace = True)
last_tick


# In[13]:


# all of the first tick data

first_tick = df[df['Tick'] == df['Tick'].min()]
first_tick.reset_index(inplace = True, drop = True)
first_tick.reset_index(inplace = True)
first_tick['index'] = first_tick['index'] + 1
first_tick


# In[14]:


data = first_tick.merge(last_tick, on = ('index'))
data


# In[15]:


# calculating daily pnl

data['A_pnl'] = data.apply(lambda row:row['A_y'] - row['A_x'], axis = 1)
data['B_pnl'] = data.apply(lambda row:row['B_y'] - row['B_x'], axis = 1)
data['C_pnl'] = data.apply(lambda row:row['C_y'] - row['C_x'], axis = 1)
data


# In[16]:


# extracting wanted columns

data = data[['index', 'A_pnl', 'B_pnl', 'C_pnl']]
data.rename({'index' : 'Day No.'}, axis = 1)


# In[17]:


# calculating total pnl

data['total_pnl_A'] = data['A_pnl'].cumsum()
data['total_pnl_B'] = data['B_pnl'].cumsum()
data['total_pnl_C'] = data['C_pnl'].cumsum()
data


# In[18]:


# Saving a copy of this data
df2 = data.drop(['index'], axis = 1)


# Note : there will be one extra data point in A because the 31st Jan dara is available for A and not fot B,C

# In[19]:


# importing library to plot data

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[20]:


plt.figure(figsize=(20, 10), dpi=150) 

data['A_pnl'].plot(label='A', color='blue') 
data['B_pnl'].plot(label='B', color='green') 
data['C_pnl'].plot(label='C', color='purple') 

plt.title("Daily PnL of A, B and C", fontsize = 30, color = 'red')
plt.savefig('graph.png')
plt.legend(fontsize = 20)


# In[21]:


data


# # Created a drawdown function(not in terms of percentage : as asked in exercise)

# In[22]:


# creating the drawdown calculator function

def calculate_drawdown(pnl_series):
    cumulative_pnl = pnl_series.cumsum()
    peak_value = cumulative_pnl.cummax()
    drawdown = (peak_value - cumulative_pnl)

    return drawdown.max()


# In[23]:


# calculating drawdpwn for ABC

drawdown_A = calculate_drawdown(data['A_pnl'])
drawdown_B = calculate_drawdown(data['B_pnl'])
drawdown_C = calculate_drawdown(data['C_pnl'])
drawdown_A, drawdown_B, drawdown_C


# In[24]:


# calculating standard deviation for A, B, C

std_A = data['A_pnl'].std()
std_B = data['B_pnl'].std()
std_C = data['C_pnl'].std()
std_A, std_B, std_C


# In[25]:


# creating a final_table dataframe

final_table = pd.DataFrame(columns = ['Type', 'No. of Pofitable trades', 
                                      'No. of loss making trades', 'Average PnL per trade', 
                                      'Drawdown', 'Sharpe'])
final_table


# In[26]:


# inserting the values

final_table.loc[len(final_table)] = {'Type':'A',
                                    'No. of Pofitable trades': (data['A_pnl'] > 0).sum(),
                                    'No. of loss making trades' : (data['A_pnl'] < 0).sum(),
                                    'Average PnL per trade' : data['A_pnl'].mean(),
                                    'Drawdown':drawdown_A,
                                    'Sharpe':(data.loc[19, 'total_pnl_A']/std_A)}
final_table.loc[len(final_table)] = {'Type':'B',
                                    'No. of Pofitable trades': (data['B_pnl'] > 0).sum(),
                                    'No. of loss making trades' : (data['B_pnl'] < 0).sum(),
                                    'Average PnL per trade' : data['B_pnl'].mean(),
                                    'Drawdown':drawdown_B,
                                    'Sharpe':(data.loc[18, 'total_pnl_B']/std_B)}
final_table.loc[len(final_table)] = {'Type':'C',
                                    'No. of Pofitable trades': (data['C_pnl'] > 0).sum(),
                                    'No. of loss making trades' : (data['C_pnl'] < 0).sum(),
                                    'Average PnL per trade' : data['C_pnl'].mean(),
                                    'Drawdown':drawdown_C,
                                    'Sharpe':(data.loc[18, 'total_pnl_C']/std_C)}


# # My step 2 is done here

# In[27]:


final_table


# In[28]:


# saving data

df3 = final_table


# In[29]:


# for the third step, I need data for second last tick

df1 = df[df['Tick'] != df['Tick'].max()]
second_last_tick = df1[df1['Tick'] == df1['Tick'].max()]
second_last_tick.reset_index(inplace = True, drop = True)
second_last_tick


# In[30]:


# relative value = B - C + D - A

second_last_tick['Relative Value'] = second_last_tick.apply(lambda i:i['B']-i['C']+i['D']-i['A'], axis = 1)
second_last_tick = second_last_tick[['Date','Relative Value']]
second_last_tick


# In[31]:


# adjusting the index column to merge first and last ticks
first_tick['index'] = first_tick['index'].apply(lambda i:i-2)
first_tick


# In[32]:


# merging first day's last tick and next day's first tick

data = last_tick.merge(first_tick, on = 'index')
data


# In[33]:


# mergining with relative values

data = data.merge(second_last_tick, left_on = 'Date_x', right_on = 'Date')
data


# In[34]:


# condiitonal data based on relative value

data_1 = data[data['Relative Value']<-2] 
data_2 = data[data['Relative Value']>1.5]


# In[35]:


data_1


# In[36]:


data_2


# In[37]:


# first condition applied for relative value < -2

data_1['Buy Value'] = -(data_1.apply(lambda x:-x['B_x'] + x['C_x'] + x['A_x'], axis = 1))

data_1['Sell Value'] = -(data_1.apply(lambda x:x['C_y'] + x['A_y'] - x['B_y'], axis = 1))

data_1['Pnl'] = data_1.apply(lambda x : x['Sell Value'] - x['Buy Value'], axis = 1)

data_1


# In[38]:


#second condiiton applied for relative value > 1.5

data_2['Buy Value'] = -(data_2.apply(lambda row : -row['A_x'] - row['C_x'] + row['B_x'], axis = 1))
data_2['Sell Value'] = -(data_2['B_y'] - data_2['A_y'] - data_2['C_y'])
data_2['Pnl'] = data_2['Sell Value'] - data_2['Buy Value']
data_2


# In[39]:


data = pd.concat([data_2, data_1])
data = data[['Buy Value', 'Sell Value', 'Pnl']]      # only wanted columns
data.reset_index(drop = True, inplace = True)        # removing the original index
data


# In[40]:


# calculating total pnl

data['Total PnL'] = data['Pnl'].cumsum()
data


# In[41]:


# Saving data
df4 = data.drop(['Buy Value', 'Sell Value'], axis = 1)


# In[42]:


plt.plot(data['Pnl'], color = 'blue')
plt.title('Day-wise Pnl for data', color = 'red', fontsize = 20)
plt.show()


# In[43]:


# plotting the Total PnL for data
plt.plot(data['Total PnL'], color = 'blue')
plt.title('Total Pnl for data', color = 'red', fontsize = 20)
plt.show()


# In[44]:


# calculating drawdown using the function we created earlier
drawdown = calculate_drawdown(data['Pnl'])
drawdown


# In[45]:


data


# In[46]:


#creating a dictionary to insert into final table

dict = {'Type':'Relative Value', 'No. of profitable trades':(data['Pnl'] > 0).sum(),
        'No. of loss making trades':(data['Pnl'] < 0).sum(), 'Average PnL per trade':(data['Pnl'].mean()),
        'Drawdown' : drawdown, 'Sharpe' : (data.loc[3, 'Total PnL']/data['Pnl'].std())}


# In[47]:


dict


# # Third step is complete here

# In[48]:


# final table

relative_value_table = pd.DataFrame(dict, index = [1])
relative_value_table


# In[49]:


# path to export data in excel sheet

path = '/Users/akshaykumar1239/Desktop/untitled folder/output.xlsx'


# # Exporting data in Excel

# In[50]:


writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
df.to_excel(writer, sheet_name='Polished Data', index = False)
df2.to_excel(writer, sheet_name='Pnl data for ABC', index = False)
df3.to_excel(writer, sheet_name='Final Table 1', index = False)
df4.to_excel(writer, sheet_name='Pnl for conditions')
relative_value_table.to_excel(writer, sheet_name = 'Final Table 2', index = False)
writer.close()


# In[51]:


df


# In[52]:


df = df[['A', 'B', 'C', 'D']]
df


# In[53]:


std = df.std()
std


# In[54]:


covariance = df.cov()
covariance


# In[55]:


correlation = df.corr()
correlation

