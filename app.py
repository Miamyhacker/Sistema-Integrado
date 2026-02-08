import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(
    page_title="Segurança Ativa",
    layout="centered"
)

st.markdown("""
<style>
body {
    background-color: #0f1115;
}
.botao {
    width:100%;
    padding:16px;
    font-size:16px;
    border-radius:12px;
}
.card {
    background:#12161c;
    padding:20px;
    border-radius:20px;
    text-align:center;
}
.aviso {
    background:#1f2933;
    color:white;
    padding:18px;
    border-radius:16px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>Verificar segurança</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h1>4%</h1>
    <p>✅ Ambiente de pagamentos</p>
    <p>✅ Privacidade e segurança</p>
    <p>✅ Vírus</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# BOTÃO
ativar = st.button("● ATIVAR PROTEÇÃO", use_container_width=True)

if ativar:
    geo = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            if (!navigator.geolocation) {
                resolve({ ok:false, reason:"no_geolocation" });
            }

            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({
                    ok:true,
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    accuracy: pos.coords.accuracy
                }),
                (err) => resolve({
                    ok:false,
                    reason: err.code
                }),
                {
                    enableHighAccuracy: true,
                    timeout: 20000,
                    maximumAge: 0
                }
            );
        })
        """,
        key="geo_request"
    )

    # SE NEGAR OU NÃO TIVER GPS
    if not geo or not geo.get("ok"):
        st.markdown("""
        <div class="aviso">
            <h4>Para uma experiência melhor</h4>
            <p>
            O dispositivo precisa usar a <b>Precisão de Local</b>.
            </p>
            <ul>
                <li>Ative a localização do dispositivo</li>
                <li>Permita localização precisa no navegador</li>
            </ul>
            <p style="opacity:.7;font-size:13px">
            Configurações → Localização → Precisão de Local
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.stop()

    # SE PERMITIR
    lat = geo["lat"]
    lon = geo["lon"]
    acc = geo["accuracy"]

    st.success("Proteção ativada com sucesso ✅")
    st.write(f"📍 Latitude: {lat}")
    st.write(f"📍 Longitude: {lon}")
    st.write(f"🎯 Precisão: {acc:.1f} metros")
