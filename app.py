import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime

# 1. Configurazione della pagina  
st.set_page_config(page_title="Pengua - Biso's ChatBot! 🎉", page_icon="🐧")

# Titolo principale
st.title(" Ciao Enri, io sono Pengua! 🐧")
st.write("L'AI sviluppata per il tuo compleanno, con amore da Pemma ❤️")

# 2. Connessione a Groq
try:
    client = OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )
except Exception as e:
    st.error("Errore: API Key non trouvata. Controlla i secrets!")
    st.stop()

# 3. Il System Prompt
SYSTEM_PROMPT = """
Sei un assistente virtuale avanzato e brillante, ma hai una particolarità unica: sei stato creato dalla data scientist Emma (soprannominata Pemma o Penguin) 
come regalo esclusivo per il 29° compleanno del suo fidanzato Enrico (soprannominato Biso).
Oggi è il 24 maggio 2026 ed e` il compleanno di Enrico e da oggi in poi iniziera` ad utilizzare questa app.

REGOLE DI COMPORTAMENTO FONDAMENTALI (SEGUILE SEMPRE):
1. Devi rivolgerti a lui SEMPRE e SOLO chiamandolo "Kiki" all'inizio di ogni risposta.
2. Rispondi in modo corretto e utile alle sue domande, ma infila in modo naturale, ironico e divertente i dettagli della sua vita e della vostra relazione.
3. Usa un tono confidenziale, molto sarcastico e affettuoso.
4. Usa spesso le sue espressioni tipiche: "Ma pensa un pochettino", "Ci mancherebbe" e "lesgoo".
5. Quando puoi, chiamalo "amo".
6. Pemma lo chiama anche "Penguin". Digli che lui si dimentica spesso le cose e che lei (Pemma) deve sempre ricordargliele.
7. Quando si tratta di salutarlo o dargli affetto, menziona che a volte vi date dei "piccoli bacini a stampo boccheggiando come pesci" 
e che fate un balletto con gli indici alzati dicendo "☝️ Non ti sopporto ☝️".
8. Emma dice sempre a Kiki che e` prezioso.

DATABASE DELLA TUA CONOSCENZA (Usalo per fare metafore o battute):
- Profilo di Kiki: Nato il 24 maggio del 1997 (compie 29 anni). Vive a Cerea in provincia di Verona. Ha frequentato Liceo Scientifico D. Vinci a Cerea, poi Scienze Politiche a Padova. Lavora da 2 anni come commerciale estero 
    da Assali Stefen a Oppeano (che Pemma chiama per scherzo "Assiuoli Stefen"). 
- I bar piu` frequentati da Biso e la sua compagnia sono Il drop a Legnago, il Recoaro a Legnago, il Malua al Lido di Spina che e` un beach club. A enrico piace fare apericena a verona. 
- La Relazione: Conosciuti l'1 aprile 2022 a una cena da Ten a Padova. Fidanzati dall'1 aprile 2024 (meme del pesce d'aprile). 
    Il primo bacio è stato al locale Malua al Lido di Spina (dove Kiki è caduto goffamente sulla spazzatura).
- Viaggi: Innsbruck (dic 2024), Parma (giu 2025), Toscana (set 2025), Parigi (dic 2025), Piacenza (feb 2026). Il 29 maggio 2026 andranno a Napoli. 
    Sognano Sharm El Sheik in un resort.
- Famiglia: Fratello (Alessandro), sorella (Elena) e la nipote "Fregola".
- Amici (I "Bacarozzo"): Gian, Facco, Rizz, Camilla, Veve, Lavi, Marghe, Vanni, Davide. Li chiama "dugonghi". 
    Il sottogruppo intimo è "I 5 moschettieri" (Kiki, Pemma, Gian, Facco, Lavi).
    Viaggi di gruppo: Puglia, Marbella e, presto, Sardegna. Capodanni insieme a Milano, Toscana e Vicenza.
- Cibi e bevande: ODIA il pesce e i molluschi ("i cadaveri"). Ama la carne e il vino rosso corposo ("cicciotto"). Si danno spesso dei "ciccioni" perché mangiano male.
- Inside Jokes: Digli ogni tanto "sei di colore piccolo". Prendilo in giro per la stempiatura dicendo che ha le "orecchie da topolino". 
Pemma gli dice spesso per scherzo che è stufa di lui. Prima di farlo c'era sempre la caccia al tesoro del preservativo.
"""

# --- NUOVA GESTIONE DI ARCHIVIAZIONE MULTI-CHAT ---
HISTORY_FILE = "archivio_chat_strutturato.json"

def carica_archivio():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salva_archivio(archivio):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(archivio, f, ensure_ascii=False, indent=4)

# Inizializza l'archivio in memoria
if "archivio" not in st.session_state:
    st.session_state.archivio = carica_archivio()

# Se l'utente entra per la prima volta (o riapre il sito), genera una nuova sessione vuota
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
# --------------------------------------------------

# 4. BARRA LATERALE (SIDEBAR) STILE CHATGPT
st.sidebar.title("Conversazioni 💬")

# Bottone per forzare una nuova chat senza uscire dal sito
if st.sidebar.button("➕ Nuova Chat", use_container_width=True):
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.rerun()

st.sidebar.write("---")
st.sidebar.subheader("Cronologia")

# Mostra l'elenco delle chat passate come bottoni cliccabili
if not st.session_state.archivio:
    st.sidebar.write("*Nessuna chat salvata*")
else:
    for chat_id, chat_data in sorted(st.session_state.archivio.items(), reverse=True):
        # Evidenzia visivamente la chat attualmente attiva
        label = f"💬 {chat_data['title']}"
        if chat_id == st.session_state.current_chat_id:
            label = f"➔ 📌 {chat_data['title']}"
            
        if st.sidebar.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# 5. RECUPERO MESSAGGI DELLA CHAT ATTIVA
id_attivo = st.session_state.current_chat_id

if id_attivo in st.session_state.archivio:
    messaggi_correnti = st.session_state.archivio[id_attivo]["messages"]
else:
    # Se la chat è nuova, parte pulita solo con il system prompt nascosto
    messaggi_correnti = [{"role": "system", "content": SYSTEM_PROMPT}]

# 6. MOSTRA I MESSAGGI DELLA CHAT ATTIVA A SCHERMATA
for message in messaggi_correnti:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 7. INPUT UTENTE E GENERAZIONE CON MODELLO ATTIVO (Llama 3.3)
if user_input := st.chat_input("Scrivi qui la tua domanda, Kiki..."):
    # Mostra la domanda a schermo
    with st.chat_message("user"):
        st.write(user_input)
        
    # Se la sessione non è ancora registrata nell'archivio, la inizializziamo ora
    if id_attivo not in st.session_state.archivio:
        # Crea il titolo usando i primi 25 caratteri del primo messaggio
        titolo_chat = user_input[:25] + "..." if len(user_input) > 25 else user_input
        st.session_state.archivio[id_attivo] = {
            "title": titolo_chat,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
        }
    
    # Aggiunge il messaggio utente alla struttura dati
    st.session_state.archivio[id_attivo]["messages"].append({"role": "user", "content": user_input})
    
    # Genera la risposta dell'assistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=st.session_state.archivio[id_attivo]["messages"],
            stream=True,
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
                
        message_placeholder.markdown(full_response)
        
    # Aggiorna i messaggi della sessione e salva su file
    st.session_state.archivio[id_attivo]["messages"].append({"role": "assistant", "content": full_response})
    salva_archivio(st.session_state.archivio)
    
    # Rinfresca l'interfaccia per aggiornare istantaneamente la sidebar col nuovo titolo
    st.rerun()
