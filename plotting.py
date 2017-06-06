import pandas as pd
from nba_py import team
import matplotlib.pyplot as plt
<<<<<<< HEAD
import matplotlib.dates as dates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,MaxNLocator
%matplotlib inline

detroit_id = 1610612765
=======

pistons = team.TeamPassTracking(1610612765)
pistons.passes_made().head(10)

detroit_last_game = team.TeamPassTracking(1610612765, last_n_games=1)
detroit_last_game.passes_made().head(10)

detroit_id = 1610612765
detroit_shots = team.TeamShotTracking(detroit_id, last_n_games=1)

# detroit_shots.closest_defender_shooting()

df_grouped = detroit_shots.closest_defender_shooting()

df_grouped['OPEN'] = df_grouped['CLOSE_DEF_DIST_RANGE'].map(lambda x: True if 'Open' in x else False)
# This creates a new column  OPEN,  mapped from the 'CLOSE_DEF_DIST_RANGE' column.
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.map.html


df_grouped

total_open_shots = df_grouped.loc[df_grouped['OPEN'] == True, 'FGA'].sum()
#print (total_open_shots)

# Mapping the formula above into a column:
open_efg = (df_grouped.loc[df_grouped['OPEN'] == True, 'FGM'].sum() + (.5 * df_grouped.loc[df_grouped['OPEN'] == True, 'FG3M'].sum())) / (df_grouped.loc[df_grouped['OPEN'] == True, 'FGA'].sum())
covered_efg = (df_grouped.loc[df_grouped['OPEN'] == False, 'FGM'].sum() + (.5 * df_grouped.loc[df_grouped['OPEN'] == False, 'FG3M'].sum())) / (df_grouped.loc[df_grouped['OPEN'] == False, 'FGA'].sum())

#print (open_efg)
#print (covered_efg)

detroit_log = team.TeamGameLogs(detroit_id)

#print (detroit_log.info())

df_game_log = detroit_log.info()
df_game_log['GAME_DATE'] = pd.to_datetime(df_game_log['GAME_DATE'])  # converting the columns datatype
df_game_log['DAYS_REST'] = df_game_log['GAME_DATE'] - df_game_log['GAME_DATE'].shift(-1)
df_game_log.head()

df_game_log['DAYS_REST'] = df_game_log['DAYS_REST'].astype('timedelta64[D]')

df_game_log.head()

# Get the dates from the game logs and pass them into the other functions:
dates = df_game_log['GAME_DATE']

# We have the first date, so now to get the relevant passing and shot info we need:
date = dates[2]  # picking a random date

game_info = team.TeamPassTracking(detroit_id, date_from=date, date_to=date).passes_made()
game_info['GAME_DATE'] = date
game_info

# Sum everything by GAME_DATE, similar to SQL-style aggregation/groupby:
df_sum = game_info.groupby(['GAME_DATE']).sum()
df_sum.reset_index(level=0, inplace=True)
df_sum

shot_info = team.TeamShotTracking(detroit_id, date_from=date, date_to=date).closest_defender_shooting()
shot_info

# From  earlier
shot_info['OPEN'] = shot_info['CLOSE_DEF_DIST_RANGE'].map(lambda x: True if 'Open' in x else False)
df_sum['OPEN_SHOTS'] = shot_info.loc[shot_info['OPEN'] == True, 'FGA'].sum()
df_sum['OPEN_EFG'] = (shot_info.loc[shot_info['OPEN'] == True, 'FGM'].sum() + (.5 * shot_info.loc[shot_info['OPEN'] == True, 'FG3M'].sum())) / (shot_info.loc[shot_info['OPEN'] == True, 'FGA'].sum())
df_sum['COVERED_EFG'] = (shot_info.loc[shot_info['OPEN'] == False, 'FGM'].sum() + (.5 * shot_info.loc[shot_info['OPEN'] == False, 'FG3M'].sum())) / (shot_info.loc[shot_info['OPEN'] == False, 'FGA'].sum())

df_sum

df_custom_boxscore = pd.merge(df_game_log, df_sum[['PASS', 'FG2M', 'OPEN_SHOTS', 'OPEN_EFG', 'COVERED_EFG']], how='left', left_on=df_game_log['GAME_DATE'], right_on=df_sum['GAME_DATE'])
df_custom_boxscore.head(10)

df_custom_boxscore['PASS_AST'] = df_custom_boxscore['PASS'] / df_custom_boxscore['AST']

# It's easier to work with dichotomos variables as binaries instead of letters
df_custom_boxscore['RESULT'] = df_custom_boxscore['WL'].map(lambda x: 1 if 'W' in x else 0)

>>>>>>> c68be799bee8b30675c0dad1bb61a618f4aa167a

def custom_boxscore(roster_id):

    game_logs = team.TeamGameLogs(roster_id)

    df_game_logs = game_logs.info()
    df_game_logs['GAME_DATE'] = pd.to_datetime(df_game_logs['GAME_DATE'])
    df_game_logs['DAYS_REST'] = df_game_logs['GAME_DATE'] - df_game_logs['GAME_DATE'].shift(-1)
    df_game_logs['DAYS_REST'] = df_game_logs['DAYS_REST'].astype('timedelta64[D]')

    # Just like before, that should get us the gamelogs we need and the rest days column

    # Now to loop through the list of dates for our other stats

    # This will build up a dataframe of the custom stats and join that to the gamelogs
    df_all = pd.DataFrame()  # blank dataframe

    dates = df_game_logs['GAME_DATE']

    for date in dates:

        game_info = team.TeamPassTracking(roster_id, date_from=date, date_to=date).passes_made()
        game_info['GAME_DATE'] = date  # We need to append the date to this so we can  join back

        temp_df = game_info.groupby(['GAME_DATE']).sum()
        temp_df.reset_index(level=0, inplace=True)

        # now to get the shot info. For the most part, we're just reusing code we've already written
        open_info = team.TeamShotTracking(roster_id, date_from=date, date_to=date).closest_defender_shooting()
        open_info['OPEN'] = open_info['CLOSE_DEF_DIST_RANGE'].map(lambda x: True if 'Open' in x else False)

        temp_df['OPEN_SHOTS'] = open_info.loc[open_info['OPEN'] == True, 'FGA'].sum()
        temp_df['OPEN_EFG'] = (open_info.loc[open_info['OPEN'] == True, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN'] == True, 'FG3M'].sum())) / (open_info.loc[open_info['OPEN'] == True, 'FGA'].sum())
        temp_df['COVERED_EFG'] = (open_info.loc[open_info['OPEN'] == False, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN'] == False, 'FG3M'].sum())) / (open_info.loc[open_info['OPEN'] == False, 'FGA'].sum())

        # append this to our bigger dataframe
        df_all = df_all.append(temp_df)

    df_boxscore = pd.merge(df_game_logs, df_all[['PASS', 'FG2M', 'FG2_PCT', 'OPEN_SHOTS', 'OPEN_EFG', 'COVERED_EFG']], how='left', left_on=df_game_logs['GAME_DATE'], right_on=df_all['GAME_DATE'])
    df_boxscore['PASS_AST'] = df_boxscore['PASS'] / df_boxscore['AST']
    df_boxscore['RESULT'] = df_boxscore['WL'].map(lambda x: 1 if 'W' in x else 0)

    return df_boxscore

df_detroit_box_scores = custom_boxscore(detroit_id)
<<<<<<< HEAD

print(df_detroit_box_scores.head(10))

# Save to local csv file
df_detroit_box_scores.to_csv('/home/rdacost_mda/nba_stats.csv')

fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, figsize=(8,8))


ax1.plot(df_detroit_box_scores['GAME_DATE'],df_detroit_box_scores['OPEN_EFG'], linewidth=1)
ax2.plot(df_detroit_box_scores['GAME_DATE'],df_detroit_box_scores['PTS'], linewidth=1)
=======
# print(df_detroit_box_scores.head())
#print (df_detroit_box_scores.columns)

fig, ax = plt.subplots()
ax.plot(df_detroit_box_scores['GAME_DATE'], df_detroit_box_scores['OPEN_EFG'])
#plt.plot(df_detroit_box_scores['GAME_DATE'], df_detroit_box_scores['OPEN_EFG'])
ax.set_title('NBA Stats')
ax.set_xlabel('Date')
ax.set_ylabel('EFG% (effective field goal percentage)')
>>>>>>> c68be799bee8b30675c0dad1bb61a618f4aa167a

ax1.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=(0), interval=1))
ax1.xaxis.set_major_formatter(dates.DateFormatter('%d/%m'))

<<<<<<< HEAD
ax1.tick_params(which='major', pad=10)
ax2.tick_params(which='major', pad=10)

for label in ax1.get_xminorticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment("right")

#ax1.set_title('Detroit Pistons 2016-17 Season', fontsize='15', fontweight='bold')
#ax1.set_xlabel('Date')
st = fig.suptitle("Detroit Pistons 2016-17 Season", fontsize='12')

ax1.set_ylabel('EFG% (effective field goal percentage)')

ax2.set_ylabel('PTS')

ax1.xaxis.set_major_locator(MaxNLocator(prune='lower'))

st.set_y(0.95)
plt.subplots_adjust(right=0.8, wspace = 0.5)

fig.autofmt_xdate()

plt.savefig('Detroit_Pistons.png', format='png')

=======
>>>>>>> c68be799bee8b30675c0dad1bb61a618f4aa167a
plt.show()
