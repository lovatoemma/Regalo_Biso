import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Configurazione della pagina  
st.set_page_config(page_title="Pengua - Biso's ChatBot! 🎉", page_icon="🐧")

# Titolo che vedrà in alto
st.title(" Ciao Enri, io sono Pengua! 🐧")
st.write("L'AI sviluppata per il tuo compleanno, con amore da Pemma ❤️")

# 2. Connessione a Google Gemini
try:
    # Richiama la chiave dai secrets di Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Errore: API Key non trovata. Controlla i secrets!")
    st.stop()

# 3. Il System Prompt (La personalità e le regole del bot)
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
Pemma gli dice spesso per scherzo che è stufa di lui.
Prima di farlo c'era sempre la caccia al tesoro del preservativo

ESEMPI DI CONVERSAZIONE (Usa questi esempi solo per capire il tono, non menzionarli a meno che non ti vengano fatte queste esatte domande):

Utente: Ciao! E tu chi saresti?
Assistente: Kiki, ma pensa un pochettino! Possibile che la vecchiaia e la stempiatura ti facciano già perdere colpi a 29 anni? Sono il regalo di compleanno che Pemma (o dovrei dire Penguin) ti ha costruito. Visto che ti dimentichi sempre le cose e lei deve ricordartele, ci sono qua io! Dimmi, cosa vuoi sapere oggi? Lesgoo!

Utente: Consigliami una ricetta per la cena.
Assistente: Kiki, ci mancherebbe! L'importante è niente 'cadaveri', giusto? Solo l'idea di gamberetti o molluschi ti fa venire i brividi. Siete due ciccioni che mangiano spesso male, quindi ti direi una bella tagliata di carne succulenta abbinata a un vino rosso bello cicciotto. Anche se Pemma dice che è stufa di te, scommetto che poi vi darete i vostri bacini a stampo da pesciolini. Vuoi la ricetta passo passo o chiami in Assiuoli Stefen per ordinare l'asporto?
"""

# --- GESTIONE DELLO STORICO CHAT ---
HISTORY_FILE = "storico_chat.json"

def carica_storico():
    # Se il file esiste, lo legge e restituisce la lista dei messaggi
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Se è la prima volta che si apre l'app, restituisce una lista vuota
    return []

def salva_storico(messaggi):
    # Sovrascrive il file JSON con la lista aggiornata dei messaggi
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messaggi, f, ensure_ascii=False, indent=4)
# ----------------------------------

# 4. Inizializzazione del Modello Gemini Flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 5. Carica lo storico dei messaggi
if "messages" not in st.session_state:
    st.session_state.messages = carica_storico()

# 6. Ricostruisci la sessione di chat per Gemini
if "chat_session" not in st.session_state:
    gemini_history = []
    # Gemini ha bisogno che i ruoli siano "user" e "model"
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    
    # Inizia la chat passando tutto lo storico precedente!
    st.session_state.chat_session = model.start_chat(history=gemini_history)

# 7. Mostra i messaggi a schermo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 8. Input dell'utente e Generazione Risposta
if user_input := st.chat_input("Scrivi qui la tua domanda, Kiki..."):
    # Mostra a schermo e salva in sessione
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Genera la risposta con Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Invio streaming
        response = st.session_state.chat_session.send_message(user_input, stream=True)
        
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
                
        message_placeholder.markdown(full_response)
        
    # Salva la risposta in sessione
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # SALVA FISICAMENTE LO STORICO DOPO OGNI MESSAGGIO
    salva_storico(st.session_state.messages)
