from set_up import league_season, league_data
from etl.update import Updater
from transform import merge, creation
from predict import prediction, reportage

import logging

logging.info("Import completed")

stagione = league_season.Stagione("2023", ongoing=True)

lat_day = league_data.latest_matchday()
logging.info(f"Next matchday: {lat_day + 1}")

Updater(stagione).check_aggiornamento()

list_ls = []
for y, s in league_data.seasons.items():
    list_ls.append(league_season.Stagione(year=y, ongoing=s))

df = merge.merge_df(list_ls)
Xnot = creation.create_matchday_df(list_ls[-1], lat_day)

predictions = [
    prediction.predict_scores(df, target, Xnot) for target in league_data.targets
]

reportage.save_report(predictions)
reportage.display_report(predictions)
