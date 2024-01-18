from set_up import league_season, league_data
from etl import update
from transform import merge, creation
#from predict import prediction, reportage

import logging
logging.basicConfig(filename='codeflow.log', encoding='utf-8', level=logging.DEBUG)  

lat_day = league_data.latest_matchday()
logging.info(f'Next day | {current}')

update.update_df()

list_ls = []
for y, s in league_data.seasons.items():
    list_ls.append(league_season.LeagueSeason(year=y, ongoing=s))

df = merge.merge_df(list_ls)
Xnot = creation.create_matchday_df(list_ls[-1], lat_day)
logging.info(f'Targets | {Xnot}')

predictions = [prediction.predict_scores(df, target, Xnot)
               for target in league_data.targets]

reportage.save_report(predictions)
reportage.display_report(predictions)