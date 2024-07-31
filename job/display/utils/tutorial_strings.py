t0 = """Benvenuto nel tutorial.

Questo tutorial ti spiegherà come utilizzare l'applicazione. 

Premi "Start" per iniziare, oppure premi il tasto "Exit" per uscire dal tutorial.
"""

tutstring0 = {
    "top": {"pos": (0, 0.7), "size": (1, 0.3)},
    "mid": {"pos": (0, 0.4), "size": (1, 0.3)},
    "bottom": {"pos": (0, 0), "size": (1, 0.4)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.9)},
    "text": t0,
}

t1 = """La barra gialla in alto presenta tre bottoni:
- Help: apre il tutorial
- About: spiega brevemente il progetto
- Quit: chiude l'applicazione

Scorri a destra per continuare
"""

tutstring1 = {
    "top": {"pos": (0, 0), "size": (0, 0)},
    "mid": {"pos": (0, 0.4), "size": (1, 0.5)},
    "bottom": {"pos": (0, 0), "size": (1, 0.4)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.85)},
    "text": t1,
}

t2 = """L'applicazione mostra i dati di una partita alla volta. 
In alto trovi la partita corrente che si sta visualizzando.

L'applicazione si compone di due viste principali:
1. Probabilità: mostra le probabilità che un determinato esito sportivo accada
2. Momento di forma: mostra lo stato di forma delle squadre

E' possibile navigare fra le pagine:
- cliccando sulle frecce: per navigare fra le partite
- cliccando sui nomi delle pagine: per spostarsi da una vista all'altra 

In alternativa, è possibile anche scrollare verticalmente (per spostarsi fra le partite) oppure orizzontalmente (per spostarsi fra le viste)

Ora approfondiamo la vista 'Probabilità'.
Scorri a destra per continuare oppure scorri a sinistra per tornare indietro.
"""

tutstring2 = {
    "top": {"pos": (0, 0.9), "size": (1, 0.1)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.8)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.76)},
    "text": t2,
}

t3 = """La vista 'Probabilità' mostra le probabilità che un determinato esito sportivo accada. 

Il primo riquadro indica la probabilità che una determinata squadra segni da 0 a 4 gol
"""

tutstring3 = {
    "top": {"pos": (0, 0.77), "size": (1, 0.23)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.52)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.99)},
    "text": t3,
}

t4 = """
Il secondo riquadro indica la probabilità che la partita abbia esito: 
- 1 (vittoria squadra casa), 
- X (pareggio), 
- 2 (vittoria squadra traserta)
"""

tutstring4 = {
    "top": {"pos": (0, 0.52), "size": (1, 0.48)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.36)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.73)},
    "text": t4,
}

t5 = """
Il terzo riquadro indica la probabilità che: 
- entrambe le squadre segnino (GG) 
- oppure che almeno una squadra non faccia gol (NG)
"""

tutstring5 = {
    "top": {"pos": (0, 0.36), "size": (1, 0.64)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.18)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.56)},
    "text": t5,
}

t6 = """
Il quarto riquadro indica la probabilità che: 
- la partita termini con 3 gol o più (Over) 
- oppure 2 gol o meno (Under)

Ora approfondiamo la vista 'Momento di forma'.
Scorri a destra per continuare oppure scorri a sinistra per tornare indietro.
"""

tutstring6 = {
    "top": {"pos": (0, 0.19), "size": (1, 0.81)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.032)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.42)},
    "text": t6,
}

t7 = """La vista 'Momento di forma' mostra lo stato di forma delle squadre. 

Il primo riquadro mostra i precedenti scontri diretti fra le squadre.
"""

tutstring7 = {
    "top": {"pos": (0, 0.8), "size": (1, 0.2)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.56)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.98)},
    "text": t7,
}

t8 = """
Il secondo riquadro mostra i risultati dei precedenti 5 incontri di campionato per entrambe le squadre:
- W: vittoria
- D: pareggio
- L: sconfitta
"""

tutstring8 = {
    "top": {"pos": (0, 0.56), "size": (1, 0.44)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.34)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.86)},
    "text": t8,
}

t9 = """
Il terzo riquadro mostra la classifica del campionato (posizione, punti, gol fatti e gol subiti).
Scrolla su e giù per scorrere fra le squadre.

Scorri a destra per continuare oppure scorri a sinistra per tornare indietro
"""

tutstring9 = {
    "top": {"pos": (0, 0.34), "size": (1, 0.66)},
    "mid": {"pos": (0, 0), "size": (0, 0)},
    "bottom": {"pos": (0, 0), "size": (1, 0.03)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.51)},
    "text": t9,
}

t10 = """
Il tutorial è terminato!
"""

tutstring10 = {
    "top": {"pos": (0, 0.7), "size": (1, 0.3)},
    "mid": {"pos": (0, 0.4), "size": (1, 0.3)},
    "bottom": {"pos": (0, 0), "size": (1, 0.4)},
    "label": {"pos_hint": {"x": 0.05, "y": 0}, "size_hint": (0.8, 0.65)},
    "text": t10,
}

strings = [
    tutstring0,
    tutstring1,
    tutstring2,
    tutstring3,
    tutstring4,
    tutstring5,
    tutstring6,
    tutstring7,
    tutstring8,
    tutstring9,
    tutstring10,
]
