import pandas as pd
from download import download
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt


url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target = "La myriade de Totems de Montpellier - SaisiesFormulaire.csv"
download(url, path_target, replace=False)  # Import the data from url
df = pd.read_csv(path_target)  # Read the data imported

df_bike = df.copy()  # Copy the datataframe (dataset's size isn't too large)

# Drop columns not useful for analysis
df_bike = df_bike.drop(columns=['Vélos depuis le 1er janvier / Grand total', 'Unnamed: 4', 'Remarque'])

df_bike = df_bike.dropna(axis=0)  # remove missing values

df_bike.index = [i for i in range(df_bike.shape[0])]  # Re-index the dataframe

for i in range(df_bike.shape[0]):
    df_bike.iloc[i, 1] = str(df_bike.iloc[i, 1]).replace(":", "")


# Tranforme 'Heure/tile' Series to numeric format
df_bike['Heure / Time'] = pd.to_numeric(df_bike['Heure / Time'], errors='coerce')


l = list()
for i in df_bike.index:

    if int(str(df_bike.iloc[i, 1])[0:1]) not in [1, 2, 3, 4, 5, 6, 7] and int(str(df_bike.iloc[i, 1])[0:2]) not in [95]:
        l.append(i)


df_bike = df_bike.loc[l, :]  # keep only bike passages recorded around 9 a.m.
df_bike.index = [i for i in range(df_bike.shape[0])]


# Remove the duplicates dates keeping only the max of each date
df_bike = df_bike.sort_values('Heure / Time', ascending=False).drop_duplicates('Date').sort_index().reset_index(drop=True)


df_bike = df_bike.drop('Heure / Time', axis=1)
df_bike = df_bike.rename(columns={"Vélos ce jour / Today's total": "bikes_before_9am"})


df_bike = df_bike.drop(np.arange(28), axis=0)
df_bike.index = [i for i in range(df_bike.shape[0])]  # remove dates during first containment
df_bike = df_bike.drop(np.arange(74, 83), axis=0)      # remove dates during second containment
df_bike.index = [i for i in range(df_bike.shape[0])]


df_bike['Date'] = pd.to_datetime(df_bike['Date'], format='%d/%m/%Y')
df_bike = df_bike.set_index('Date')  # Re-index dataframe with the date


l_day = []

# Transform dates into a number of the associated day (0: Monday, 6:Sunday)
for i in range(df_bike.shape[0]):

    s = pd.to_datetime(df_bike.index[i]).weekday()
    l_day.append(s)

df_bike['Day'] = l_day   # Create a new Series named 'Day'



df_bike = df_bike[df_bike['Day']!=5]  # delete saturday
df_bike = df_bike[df_bike['Day']!=6]  # delete sunday



# Distribution of number of bikes from Monday to Friday

plt.figure(figsize=(6, 7))
ax = sns.kdeplot(df_bike['bikes_before_9am'], shade=True, cut=0, bw_method=0.1, color='#984ea3', alpha=0.4)
plt.title('Estimated distribution of the number of bicycles before 9 a.m. (Monday to Friday)', fontsize='xx-small')
plt.xlabel('Number of bikes')
# plt.show()


# Passages from Monday to Friday

plt.figure(figsize=(10, 6))
plt.subplot(1,2,1)
plt.plot(df_bike.index, df_bike['bikes_before_9am'], label='Number of bikes at 9 a.m.', color='#e41a1c')
plt.title('Cyclist flow at 9 a.m.', fontsize='x-small')
plt.xlabel('Dates', fontsize=6)
plt.ylabel('Number of bikes')
plt.legend(loc='best', fontsize='x-small')
plt.xticks(df_bike.index[::6], rotation=45, fontsize=5)
plt.subplot(1,2,2)
ax = sns.kdeplot(df_bike['bikes_before_9am'], shade=True, cut=0, bw_method=0.1, color='#984ea3', alpha=0.4)
plt.title('Estimated distribution of the number of bicycles at 9 a.m. (Monday to Friday)', fontsize='xx-small')
plt.xlabel('Number of bikes')
plt.savefig('./hist.pdf')
# plt.show()



RMSE = []
test = df_bike.loc[:, ['bikes_before_9am']]  # Create a test set from df_bike
train = df_bike.loc[:, ['bikes_before_9am']]  # Create a train set from df_bike
test = test.iloc[df_bike.shape[0]-30:df_bike.shape[0], :]
train = train.iloc[0:df_bike.shape[0]-30, :]
y_hat_avg = test.copy()



for n in range(1, train.shape[0]+1):

    y_hat_avg['moving_avg_forecast'] = train['bikes_before_9am'].rolling(window=n).mean().iloc[-1]
    RMSE.append(sqrt(mean_squared_error(test.bikes_before_9am, y_hat_avg.moving_avg_forecast)))



y_hat_avg['moving_avg_forecast'] = train['bikes_before_9am'].rolling(RMSE.index(min(RMSE))+1).mean().iloc[-1]

plt.figure(figsize=(10, 4))
plt.plot(train['bikes_before_9am'], label='Train', color='#e41a1c')
plt.plot(test['bikes_before_9am'], label='Test', color='purple')
plt.plot(y_hat_avg['moving_avg_forecast'], label='Moving Average Forecast', color='black')
plt.xlabel('Date', fontsize=7)
plt.ylabel('Number of bikes')
plt.xticks(df_bike.index[::4], rotation=45, fontsize=5)
plt.legend(loc='best', fontsize=11)
plt.savefig('./test.pdf')
# plt.show()


# My prediction
print('My prediction is', round(y_hat_avg.iloc[0, 1]), 'bikes before 9 a.m')

rm = sqrt(mean_squared_error(test.bikes_before_9am,
y_hat_avg.moving_avg_forecast))   # Calculate RMSE

# print('The RMSE of prediction is:', rm)
