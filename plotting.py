import pandas as pd

df_list = pd.read_html('http://www.espn.com/nba/team/stats/_/name/det', header=0)
df_2017 = df_list[0]
df_2017.columns = df_2017.iloc[0]
df_2017 = df_2017.reindex(df_2017.index.drop(0))
df_2017.set_index(['PLAYER'], inplace=True)

# Create a new Panda series
df_2017_total = (df_2017.loc['Totals'])

# Drop the 'Totals' row
df_2017.drop('Totals', inplace=True)

# Set the mean values
avg_ppg = pd.to_numeric(df_2017['PPG']).mean()
avg_min = pd.to_numeric(df_2017['MIN']).mean()
avg_gp = pd.to_numeric(df_2017['GP']).mean()

print('Average Minutes:', avg_ppg)
print('Average Points per Game:', avg_min)
print('Games Played:', avg_gp)


print(df_2017)

#lst = []
# for i in range(2006, 2017):
#    df_list = pd.read_html('http://www.espn.com/nba/team/stats/_/name/det/year/i/seasontype/2', header=0)
#   df_i = df_list[0]
#   lst.append(df_i)
