import streamlit as st
import pandas as pd

# Lista dei consiglieri
consiglieri = [
    "Leonardo Balzarini (Mag)", "Mario Boatto (Min)", "Giorgio Circosta (Mag)",
    "Marco Colombo (Min)", "Simone Danzo (Mag)", "Loredana D’Agaro (Mag)",
    "Edoardo Favaron (Min)", "Pietro Ferrario (Mag)", "Christian Gnodi (Mag)",
    "Betta Giordani (Mag)", "Sergio Gumier (Mag)", "Francesca Gualtieri (Mag)",
    "Marco Limbiati (Min)", "Barbara Mercalli (Mag)", "Michele Ponti (Mag)",
    "Jole Capriglia Sesia (Min)", "Floriana Tollini (Mag)"
]

# Separazione dei consiglieri per ruolo
maggioranza = [c for c in consiglieri if "(Mag)" in c and c != "Betta Giordani (Mag)"]
minoranza = [c for c in consiglieri if "(Min)" in c]
sindaco = "Betta Giordani (Mag)"

# Bonus e Malus con i relativi punteggi
bonus = {
    "Si prenota a parlare per primo": 2,
    "Cita sindaci precedenti al 1995": 2,
    "Parla più di 20 minuti per intervento": 4,
    "Sbaglia strumento di intervento": 10,
    "Si alza e sparisce dall’inquadratura della Civicam 5 o più volte": 9,
    "Cita una pagina social": 2,
    "Nomina una testata locale": 3,
    "Nomina il FantaConsiglio": 5,
    "Si inginocchia": 9,
    "Cita un’associazione onlus": 1,
    "Usa la parola 'élite'": 4,
    "Porta il discorso sulla Moschea": 9,
    "Intervento Mic Drop": 9
}

malus = {
    "Non si presenta": -4,
    "Non prende mai la parola": -2,
    "Parla al pubblico e non all’interlocutore": -4,
    "Guarda il cellulare mentre un interlocutore gli parla": -2,
    "Parla oltre il tempo concesso": -4,
    "Usa la parola PD": -4,
    "Definisce Sesto Calende come casa": -2,
    "Fa riferimento al proprio lavoro": -10,
    "Ride durante l’intervento di un altro consigliere": -2,
    "Getta i fogli sul banco in segno di stizza": -4
}

# Inizializzazione del punteggio e della cronologia delle azioni
if 'punteggi' not in st.session_state:
    st.session_state.punteggi = {consigliere: 0 for consigliere in consiglieri}

if 'cronologia' not in st.session_state:
    st.session_state.cronologia = []

# Titolo dell'app
st.title("Control Room FantaConsiglio")

# Layout con tre colonne: Maggioranza, Sindaco, Minoranza
col1, col2, col3 = st.columns([3, 1, 3])

# Maggioranza
with col1:
    st.subheader("Maggioranza")
    for consigliere in maggioranza:
        if st.button(consigliere, key=f"maggioranza_{consigliere}"):
            st.session_state.selezionato = consigliere

# Sindaco
with col2:
    st.subheader("Sindaco")
    if st.button(sindaco, key="sindaco"):
        st.session_state.selezionato = sindaco

# Minoranza
with col3:
    st.subheader("Minoranza")
    for consigliere in minoranza:
        if st.button(consigliere, key=f"minoranza_{consigliere}"):
            st.session_state.selezionato = consigliere

# Pulsante per cancellare l'ultima azione
if st.button("Cancella Ultimo") and st.session_state.cronologia:
    ultima_azione = st.session_state.cronologia.pop()
    st.session_state.punteggi[ultima_azione['consigliere']] -= ultima_azione['punteggio']
    st.warning(f"Annullata l'azione '{ultima_azione['azione']}' per {ultima_azione['consigliere']}.")

# Sezione Bonus
st.subheader("Bonus")
for azione, punteggio in bonus.items():
    if st.button(azione, key=f"bonus_{azione}"):
        if 'selezionato' in st.session_state:
            st.session_state.punteggi[st.session_state.selezionato] += punteggio
            st.session_state.cronologia.append({
                'consigliere': st.session_state.selezionato,
                'azione': azione,
                'punteggio': punteggio
            })
            st.success(f"Azione '{azione}' (+{punteggio}) assegnata a {st.session_state.selezionato}!")

# Sezione Malus
st.subheader("Malus")
for azione, punteggio in malus.items():
    if st.button(azione, key=f"malus_{azione}"):
        if 'selezionato' in st.session_state:
            st.session_state.punteggi[st.session_state.selezionato] += punteggio
            st.session_state.cronologia.append({
                'consigliere': st.session_state.selezionato,
                'azione': azione,
                'punteggio': punteggio
            })
            st.error(f"Azione '{azione}' ({punteggio}) assegnata a {st.session_state.selezionato}!")

# Dashboard dei punteggi
st.header("Dashboard Punteggi")
punteggi_df = pd.DataFrame(list(st.session_state.punteggi.items()), columns=['Consigliere', 'Punteggio'])
punteggi_df = punteggi_df.sort_values(by='Punteggio', ascending=False)

st.dataframe(punteggi_df, use_container_width=True)

# Reset dei punteggi
if st.button("Reset Punteggi"):
    st.session_state.punteggi = {consigliere: 0 for consigliere in consiglieri}
    st.session_state.cronologia = []
    st.success("Punteggi resettati!")
