import streamlit as st
from openai import OpenAI
import json
import os

# 1. Configurazione della pagina  
st.set_page_config(page_title="Pengua - Biso's ChatBot! 🎉", page_icon="🐧")

st.title(" Ciao Enri, io sono Pengua! 🐧")
st.write("L'AI sviluppata per il tuo compleanno, con amore da Pemma ❤️")

# 2. Connessione a Groq usando la libreria OpenAI
try:
    client = OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )
except Exception as e:
    st.error("Errore: API Key non trovata. Controlla i secrets!")
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

# --- GESTIONE DELLO STORICO CHAT ---
HISTORY_FILE = "storico_compleanno_biso.json"

def carica_storico():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salva_storico(messaggi):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messaggi, f, ensure_ascii=False, indent=4)
# ----------------------------------

# 4. Inizializzazione della cronologia
if "messages" not in st.session_state:
    storico_salvato = carica_storico()
    if not storico_salvato:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    else:
        st.session_state.messages = storico_salvato

# 5. Mostra i messaggi precedenti (nascondendo il system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 6. Input dell'utente
if user_input := st.chat_input("Scrivi qui la tua domanda, Kiki..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 7. Generazione della risposta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
# Chiamata al modello Llama 3.1 tramite Groq
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile", 
            messages=st.session_state.messages,
            stream=True,
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
                
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    salva_storico(st.session_state.messages)
