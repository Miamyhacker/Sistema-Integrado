import streamlit as st
import time
from streamlit_js_eval import streamlit_js_eval

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Segurança Ativa",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body, .main {
    background-color: #0b0f14;
    color: white;
}

.circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 4px solid #2ecc71;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    font-weight: bold;
    margin: auto;
    box-shadow: 0 0 40px rgba(46,204,113,.5);
}

.btn {
    width: 100%;
    padding: 16px;
    border-radius: 12px;
    background: #1f2937;
    color: white;
    font-size: 18px;
    border: none;
    cursor: pointer;
}

.alert {
    background: #1f2937;
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown("<h2 style='text-align:center'>Verificar segurança</h2>", unsafe_allow_html=True)

circle = st.empty()
circle.markdown("<div class='circle'>4%</div>", unsafe_allow_html=True)

st.markdown("""
✅ Ambiente de pagamentos  
✅ Privacidade e segurança  
✅ Vírus
""")

# ---------------- BUTTON ----------------
clicked = st.button("● ATIVAR PROTEÇÃO", use_container_width=True)

# ---------------- JS GEOLOCATION ----------------
if clicked:
    location = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            if (!navigator.geolocation) {
                resolve({error: "not_supported"});
            } else {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve({
                        ok: true,
                        lat: pos.coords.latitude,
                        lon: pos.coords.longitude
                    }),
                    (err) => resolve({error: err.code})
                );
            }
        })
        """,
        key="geo"
    )

    # ---------------- RESULT ----------------
    if location:
        if location.get("ok"):
            for i in range(4, 101, 6):
                circle.markdown(f"<div class='circle'>{i}%</div>", unsafe_allow_html=True)
                time.sleep(0.05)

            st.success("Proteção ativada com sucesso ✅")
            st.write("📍 Localização capturada com consentimento:")
            st.write(location)

        else:
            st.markdown("""
            <div class="alert">
            <h3>Para uma experiência melhor</h3>
            <p>O dispositivo precisa usar a <b>Precisão de Local</b>.</p>
            <ul>
                <li>Ative a localização do dispositivo</li>
                <li>Permita localização precisa no navegador</li>
            </ul>
            <small>Configurações → Localização → Precisão de Local</small>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#555;margin-top:40px'>Hospedado com Streamlit</p>", unsafe_allow_html=True)
