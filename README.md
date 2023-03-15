# Progetto-Schedina
Lo scopo del progetto è prevedere i risultati delle partite di calcio del campionato italiano Serie A. 
Pertanto ho costruito un modello statistico che permette di calcolare le probabilità che un certo evento avvenga.
Per ogni variabile che viene predetta esiste uno specifico notebook:
- Forecasting 1X2: probabilità che la partita finisca in vittoria, pareggio o sconfitta per la squadra di casa.
- Forecasting results: probabilità che la squadra di casa faccia da 0 a 8 gol e subisca da 0 a 8 gol.
- Forecasting GG NG: probabilità che entrambe le squadre segnino (GG) oppure che almeno una delle due non faccia gol (NG)
- Forecasting UO 1.5: probabilità che i gol totali della partita siano più di 2
- Forecasting UO 2.5: probabilità che i gol totali della partita siano più di 3
- Forecasting UO 3.5: probabilità che i gol totali della partita siano più di 4
- Forecasting UO 4.5: probabilità che i gol totali della partita siano più di 5

Il dataframe sul quale le analisi vengono svolte è salvato nell'apposito file Dataframe.csv. Esso si compone dei risultati di tutte le partite di Serie A giocate dal 2019 fino a quelle attuali. Per ogni incontro sono state create le seguenti vatriabili: 
1. i gol fatti dalla squadra di casa nella partita, i gol subiti dalla squadra di casa nella partita
2. i 5 precedenti risultati della squadra di casa, i 5 precedenti risultati della squadra in trasferta. 
3. i gol fatti dalla squadra di casa nelle precedenti 5 giornate, i gol subiti dalla squadra di casa nelle precedenti 5 giornate, i gol fatti dalla squadra in trasferta nelle precedenti 5 giornate, i gol subiti dalla squadra in trasferta nelle precedenti 5 giornate.
4. la posizione in classifica della squadra di casa, la posizione in classifica della squadra in trasferta.
5. la media gol fatti e la media gol subiti della squadra di casa, la media gol fatti e la media gol subiti della squadra in trasferta, la deviazione standard dei gol fatti e la deviazione standard dei gol subiti della squadra di casa, la deviazione standard dei gol fatti e la deviazione standard dei gol subiti della squadra di casa

Il punto 1. rappresenta la variabile target (y) del modello statistico. I punti 2-5 rappresentano le variabili esplicative (X) del modello. 
A seconda dell'obiettivo di pfrevisione è stato usato o una RegressioneLogistica, o un modello NaiveBayes

I file .ipynb che non servono a fare Forecasting (previsioni), servono per la raccolta e la manipolazione dei dati. Infine, i file excel servono come step intermedi per trasformare i dati nel dataframe finale
