
import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
from collections import Counter

st.title("🎯 Analisador de Roleta - por Imagem")

uploaded_file = st.file_uploader("Envie a imagem da roleta (estatísticas)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')

    numeros = [int(n) for n in text.split() if n.isdigit() and 0 <= int(n) <= 36]
    if not numeros:
        st.error("Nenhum número válido foi detectado na imagem.")
    else:
        st.success(f"🎲 {len(numeros)} números detectados com sucesso!")

        color_map = {
            0: "verde", 1: "vermelho", 2: "preto", 3: "vermelho", 4: "preto",
            5: "vermelho", 6: "preto", 7: "vermelho", 8: "preto", 9: "vermelho",
            10: "preto", 11: "preto", 12: "vermelho", 13: "preto", 14: "vermelho",
            15: "preto", 16: "vermelho", 17: "preto", 18: "vermelho", 19: "vermelho",
            20: "preto", 21: "vermelho", 22: "preto", 23: "vermelho", 24: "preto",
            25: "vermelho", 26: "preto", 27: "vermelho", 28: "preto", 29: "preto",
            30: "vermelho", 31: "preto", 32: "vermelho", 33: "preto", 34: "vermelho",
            35: "preto", 36: "vermelho"
        }

        def analisar(n):
            return {
                "cor": color_map.get(n, "desconhecida"),
                "par": "par" if n != 0 and n % 2 == 0 else "ímpar" if n != 0 else "nenhum",
                "duzia": (n - 1) // 12 + 1 if n != 0 else "nenhuma",
                "coluna": (n - 1) % 3 + 1 if n != 0 else "nenhuma"
            }

        cores, pares, duzias, colunas = [], [], [], []
        for n in numeros:
            info = analisar(n)
            cores.append(info["cor"])
            pares.append(info["par"])
            duzias.append(info["duzia"])
            colunas.append(info["coluna"])

        st.subheader("📊 Estatísticas Gerais")
        st.write("**Cores:**", dict(Counter(cores)))
        st.write("**Par/Ímpar:**", dict(Counter(pares)))
        st.write("**Dúzias:**", dict(Counter(duzias)))
        st.write("**Colunas:**", dict(Counter(colunas)))

        mais_freq = Counter(numeros).most_common(5)
        menos_freq = Counter(numeros).most_common()[-5:]

        st.subheader("🔥 Números mais frequentes")
        for n, f in mais_freq:
            st.write(f"Número {n} apareceu {f}x")

        st.subheader("❄️ Números menos frequentes")
        for n, f in menos_freq:
            st.write(f"Número {n} apareceu {f}x")

        st.subheader("💡 Sugestões de Aposta (baseado em histórico)")
        if Counter(cores)['preto'] > Counter(cores)['vermelho'] * 2:
            st.write("➡️ Alta chance de reverter para: **🔴 Vermelho**")
        if Counter(duzias)[1] > Counter(duzias)[2] and Counter(duzias)[1] > Counter(duzias)[3]:
            st.write("➡️ Dúzia mais ativa: **1ª Dúzia (1–12)**")
        if Counter(colunas)[2] > Counter(colunas)[1] and Counter(colunas)[2] > Counter(colunas)[3]:
            st.write("➡️ Coluna mais ativa: **2ª Coluna**")
        st.write("➡️ Aposte em números quentes como:", [n for n, _ in mais_freq])
