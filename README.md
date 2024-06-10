# Progetto-Schedina
The aim of the project is to predict the results of football matches in the Italian Serie A championship.
Therefore I built a statistical model that allows you to calculate the probabilities that a certain event occurs.

In total there are 5 events:
- **Goals scored**: probability that the home team scores from 0 to 4 goals.
- **Goals received**: probability that the home team concedes from 0 to 4 goals.
- **1X2**: probability that the match ends in victory (W), draw (N) or defeat (P) for the home team.
- **GG_NG**: probability that both teams score (GG) or that at least one of the two does not score (NG)
- **OU 2.5**: probability that the total goals of the match are greater (Over) or less (Under) than 2.5

The dataframe consists of the results of all Serie A matches played from 2019 to the current ones. For each meeting the following variables were created:
1. the goals scored by the home team in the match, the goals conceded by the home team in the match
2. the 5 previous results of the home team, the 5 previous results of the away team.
3. the goals scored by the home team in the previous 5 matchdays, the goals conceded by the home team in the previous 5 matchdays, the goals scored by the away team in the previous 5 matchdays, the goals conceded by the away team in the previous 5 matchdays.
4. the ranking position of the home team, the ranking position of the away team.
5. the average goals scored and the average goals conceded of the home team, the average goals scored and the average goals conceded of the away team, the standard deviation of goals scored and the standard deviation of goals conceded of the home team, the deviation standard of goals scored and the standard deviation of goals conceded of the home team

Point 1. represents the target variable (y) of the statistical model. Points 2-5 represent the explanatory variables (X) of the model.
Depending on the forecasting objective, either a Logistic Regression or a NaiveBayes model was used
