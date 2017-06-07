
# coding: utf-8

# In[1]:

import pandas as pd
from nba_py import team
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,MaxNLocator
get_ipython().magic('matplotlib inline')

detroit_id = 1610612765

def custom_boxscore(roster_id):

    game_logs  = team.TeamGameLogs(roster_id)

    df_game_logs = game_logs.info()
    df_game_logs['GAME_DATE'] =  pd.to_datetime(df_game_logs['GAME_DATE'])
    df_game_logs['DAYS_REST'] =  df_game_logs['GAME_DATE'] - df_game_logs['GAME_DATE'].shift(-1)
    df_game_logs['DAYS_REST'] =  df_game_logs['DAYS_REST'].astype('timedelta64[D]')

    df_all =pd.DataFrame() ##blank dataframe

    dates = df_game_logs['GAME_DATE']

    for date in dates:

        game_info = team.TeamPassTracking(roster_id,  date_from=date, date_to=date).passes_made()
        game_info['GAME_DATE'] = date ## We need to append the date to this so we can  join back

        temp_df = game_info.groupby(['GAME_DATE']).sum()
        temp_df.reset_index(level =  0,  inplace =  True)

        ##now to get the shot info. For the most part, we're just reusing code we've already written
        open_info =  team.TeamShotTracking(roster_id,date_from =date,  date_to =  date).closest_defender_shooting()
        open_info['OPEN'] = open_info['CLOSE_DEF_DIST_RANGE'].map(lambda x: True if 'Open' in x else False)

        temp_df['OPEN_SHOTS'] = open_info.loc[open_info['OPEN'] == True, 'FGA'].sum()
        temp_df['OPEN_EFG']= (open_info.loc[open_info['OPEN']== True, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== True, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== True, 'FGA'].sum())
        temp_df['COVERED_EFG']= (open_info.loc[open_info['OPEN']== False, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== False, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== False, 'FGA'].sum())

        ##append this to our bigger dataframe
        df_all = df_all.append(temp_df)
        
    df_boxscore =  pd.merge(df_game_logs, df_all[['PASS', 'FG2M', 'FG2_PCT', 'OPEN_SHOTS', 'OPEN_EFG', 'COVERED_EFG']], how = 'left', left_on = df_game_logs['GAME_DATE'], right_on = df_all['GAME_DATE'])
    df_boxscore['PASS_AST'] = df_boxscore['PASS'] /  df_boxscore['AST']
    df_boxscore['RESULT'] = df_boxscore['WL'].map(lambda x: 1 if 'W' in x else 0 )

    return df_boxscore

df_detroit_box_scores = custom_boxscore(detroit_id)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8,8))

ax1.plot(df_detroit_box_scores['GAME_DATE'],df_detroit_box_scores['FGM'], linewidth=1, label='FGM per game')
ax1.plot(df_detroit_box_scores['GAME_DATE'],df_detroit_box_scores['FGA'], linewidth=1, label='FGA per game')
ax2.plot(df_detroit_box_scores['GAME_DATE'],df_detroit_box_scores['PTS'], linewidth=1, label='Points scored per game')

ax1.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=(0), interval=1))                             
ax1.xaxis.set_major_formatter(dates.DateFormatter('%d/%m'))

for label in ax1.get_xminorticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment("right")
    

ax1.set_ylabel('FGA (Field Goal Attempts) / FGM (Field Goals Made)')
ax2.set_ylabel('PTS')


plt.subplots_adjust(top = 0.85)

ax1.set_xlim(df_detroit_box_scores['GAME_DATE'].iloc[-1],  df_detroit_box_scores['GAME_DATE'].iloc[0])
ax2.set_xlim(df_detroit_box_scores['GAME_DATE'].iloc[-1],  df_detroit_box_scores['GAME_DATE'].iloc[0])

ax1.legend(loc="upper left", prop={'size':6})
ax2.legend(loc="upper left", prop={'size':6})

fig.autofmt_xdate()
fig.suptitle("Detroit Pistons 2016-17 Season", fontsize='12', fontweight='bold', verticalalignment = 'top')
plt.savefig('Detroit_Pistons_1.png', format='png')
plt.tight_layout()
plt.show()


# In[ ]:

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame()
df = df.from_csv('/home/rdacost_mda/nba_stats.csv')

print (df.head())

fig, ax = plt.subplots()
ax.plot(df['GAME_DATE'],df['OPEN_EFG'])
plt.show()


# In[ ]:



