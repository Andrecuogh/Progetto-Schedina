# Progetto-Schedina

L'obiettivo del progetto è prevedere i risultati delle partite di calcio del campionato italiano di Serie A. Pertanto, ho costruito un modello statistico che consente di calcolare le probabilità che si verifichi un determinato evento.

In totale ci sono 5 eventi:
- **Goal segnati**: probabilità che la squadra di casa segni da 0 a 4 goal.
- **Goal subiti**: probabilità che la squadra di casa subisca da 0 a 4 goal.
- **1X2**: probabilità che la partita finisca in vittoria (W), pareggio (N) o sconfitta (P) per la squadra di casa.
- **GG_NG**: probabilità che entrambe le squadre segnino (GG) o che almeno una delle due non segni (NG).
- **OU 2.5**: probabilità che i goal totali della partita siano superiori (Over) o inferiori (Under) a 2.5.

Il dataframe è composto dai risultati di tutte le partite di Serie A giocate dal 2019 a quelle attuali. Per ciascun incontro sono state create le seguenti variabili:
1. i goal segnati dalla squadra di casa nella partita, i goal segnati dalla squadra in trasferta nella partita.
2. i 5 risultati precedenti della squadra di casa, i 5 risultati precedenti della squadra in trasferta.
3. i goal segnati dalla squadra di casa nelle precedenti 5 giornate, i goal subiti dalla squadra di casa nelle precedenti 5 giornate, i goal segnati dalla squadra in trasferta nelle precedenti 5 giornate, i goal subiti dalla squadra in trasferta nelle precedenti 5 giornate.
4. la posizione in classifica della squadra di casa, la posizione in classifica della squadra in trasferta.
5. la media dei goal segnati e la media dei goal subiti della squadra di casa, la media dei goal segnati e la media dei goal subiti della squadra in trasferta, la deviazione standard dei goal segnati e la deviazione standard dei goal subiti della squadra di casa, la deviazione standard dei goal segnati e la deviazione standard dei goal subiti della squadra in trasferta.

Il punto 1 rappresenta la variabile target (y) del modello statistico. I punti 2-5 rappresentano le variabili esplicative (X) del modello. Il modello statistico utilizzato è un GradientBosstingClassifier.