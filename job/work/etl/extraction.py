import pandas as pd
import numpy as np
from transform import computation
import logging

class Extractor():

    def __init__(self, ls):
        self.year = ls.year
        self.teams = ls.teams
        self.leagues = ls.leagues
        self.days = ls.days


class ExtractorRanking(Extractor):

    def process(self):
        logging.info(f'Computing ranking')
        
        # set up the dataframe
        df = pd.DataFrame(np.zeros((20, 8)))
        df.columns = [
            'squadra', 
            'gol_fatti', 
            'gol_subiti', 
            'punti', 
            'vittoria', 
            'pareggio', 
            'sconfitta', 
            'differenza_reti'
            ]
        df['squadra'] = self.teams
        df.set_index('squadra', inplace=True)

        # fill the dataframe
        classifica = []
        for giorno in range(self.days):

            goal_fatti = computation.count_goals(self, giorno)
            # debug check se non sono già a zero
            goal_fatti[['vittoria', 'pareggio', 'sconfitta', 'punti']] = 0

            for squadra in goal_fatti.index:
                if goal_fatti.loc[squadra, 'gol_fatti'] > goal_fatti.loc[squadra, 'gol_subiti']:
                    goal_fatti.loc[squadra, 'punti'] = 3
                    goal_fatti.loc[squadra, 'vittoria'] = 1

                elif goal_fatti.loc[squadra, 'gol_fatti'] == goal_fatti.loc[squadra, 'gol_subiti']:
                    goal_fatti.loc[squadra, 'punti'] = 1
                    goal_fatti.loc[squadra, 'pareggio'] = 1

                else:
                    goal_fatti.loc[squadra, 'sconfitta'] = 1

            goal_fatti['differenza_reti'] = goal_fatti['gol_fatti'] - goal_fatti['gol_subiti']
            df = goal_fatti + df
            df.sort_values(
                by=[
                    'punti', 
                    'differenza_reti', 
                    'gol_fatti',
                    ],
                ascending = [
                    False, 
                    False, 
                    False,
                    ],
                inplace=True
                )
            df['posizione'] = np.arange(1, 21)
            classifica.append(df)

        return classifica


class ExtractorResults(Extractor):

    def process(self):
        logging.info(f'Computing results')
        risultati = []
        for giorno in range(self.days):
            
            # load matchday scores
            # resdf.columns = ['squadra_casa', 'squadra_trasferta', 'risultato'] risultato = 'Goal-Goal'
            df = self.leagues[giorno]
            tabellino = pd.DataFrame(np.zeros((20, 2)))
            tabellino.columns = ['squadra', 'esito']

            for i in df.index:
                tabellino.loc[i, 'squadra'] = df.loc[i, 'squadra_casa']
                tabellino.loc[i + 10, 'squadra'] = df.loc[i, 'squadra_trasferta']
                
                risultato_casa, risultato_trasferta = df.loc[i, 'risultato'].split(' - ')
                if risultato_casa > risultato_trasferta:
                    tabellino.loc[i, 'esito'] = 'vittoria'
                    tabellino.loc[i + 10, 'esito'] = 'sconfitta'

                elif risultato_casa == risultato_trasferta:
                    tabellino.loc[i, 'esito'] = 'pareggio'
                    tabellino.loc[i + 10, 'esito'] = 'pareggio'

                else:
                    tabellino.loc[i, 'esito'] = 'sconfitta'
                    tabellino.loc[i + 10, 'esito'] = 'vittoria'

            risultati.append(tabellino)

        return risultati


class ExtractorGoals(Extractor):

    def process(self):
        logging.info(f'Computing goals')
        goal_segnati = pd.DataFrame(np.zeros((20,1)))
        goal_segnati.index = self.teams
        goal_subiti = goal_segnati.copy()

        for giorno in range(self.days):
            goal = computation.count_goals(self, giorno)
            goal_segnati = pd.concat(
                [goal_segnati, goal['gol_fatti']], 
                axis=1
                )
            goal_subiti = pd.concat(
                [goal_subiti, goal['gol_subiti']], 
                axis=1
                )

        # che è 0?
        goal_segnati.drop(
            0, 
            axis=1, 
            inplace=True
            )
        goal_segnati.columns = [i for i in range(1, self.days + 1)]

        goal_subiti.drop(
            0, 
            axis=1, 
            inplace=True
            )
        goal_subiti.columns = [i for i in range(1, self.days + 1)]

        goal_totali = []
        for giornata in range(self.days):
            goal = pd.DataFrame(np.zeros((20, 4)))
            goal.index = goal_segnati.index

            goal['media_gol_fatti'] = goal_segnati.loc[:, 1:giornata+1].mean(axis=1)
            goal['varianza_gol_fatti'] = goal_segnati.loc[:, 1:giornata+1].std(axis=1)
            goal['media_gol_subiti'] = goal_subiti.loc[:, 1:giornata+1].mean(axis=1)
            goal['varianza_gol_subiti'] = goal_subiti.loc[:, 1:giornata+1].std(axis=1)

            goal.fillna(0, inplace=True)
            goal_totali.append(goal)

        return goal_totali
