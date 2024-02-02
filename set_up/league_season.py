from set_up import league_data
from job.work.etl import scraping, extraction
import logging

class Stagione:

    def __init__(self, year, ongoing=False):
        self.year = year
        self.teams = league_data.teamlist[self.year]
        if ongoing:
            self.days = league_data.latest_matchday()
            self.leagues = scraping.scrape_sky(self.year)
            self.next = self.leagues[self.days]
        else:
            self.days = 38

    def process_data(self):
        self.rankings = extraction.ExtractorRanking(self).process()
        self.results = extraction.ExtractorResults(self).process()
        self.gsgr = extraction.ExtractorGoals(self).process()

    def export_csv(self, path):
        logging.info('Saving data')
        for i in range(self.days):
            self.leagues[i].to_csv(
                f'{path}/data/scores/{self.year}/{i}.csv'
                )
            self.rankings[i].to_csv(
                f'{path}/data/rankings/{self.year}/{i}.csv'
                )
            self.results[i].to_csv(
                f'{path}/data/results/{self.year}/{i}.csv'
                )
            self.gsgr[i].to_csv(
                f'{path}/data/scored_received/{self.year}/{i}.csv'
                )