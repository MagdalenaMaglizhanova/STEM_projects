import streamlit as st
import cv2
import numpy as np
import easyocr
import requests

# OCR четец
reader = easyocr.Reader(['en'])

st.title("📷 Barcode Scanner с Open Food Facts")

uploaded_file = st.file_uploader("Качи изображение с баркод", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Преобразуване на файла в NumPy масив
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Показване на изображението
    st.image(image_np, caption='Качено изображение', channels="BGR")

    # Преобразуване в сиво за OCR
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Извличане на текст
    result = reader.readtext(gray)

    found = False
    for detection in result:
        text = detection[1]
        if text.isdigit() and len(text) >= 8:
            st.success(f"🔍 Разчетен баркод: {text}")
            found = True

            # Заявка към Open Food Facts API
            url = f"https://world.openfoodfacts.org/api/v0/product/{text}.json"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:
                    product = data.get("product", {})
                    name = product.get("product_name", "Няма име")
                    brands = product.get("brands", "Неизвестна марка")
                    nutriments = product.get("nutriments", {})
                    calories = nutriments.get("energy-kcal_100g", "Няма данни")

                    st.info(f"🛒 **Продукт:** {name}\n🏷️ **Марка:** {brands}\n🔥 **Калории (на 100g):** {calories}")
                else:
                    st.warning("❌ Продуктът не беше намерен в Open Food Facts.")
            else:
                st.error("⚠️ Възникна грешка при свързване с Open Food Facts.")
            break

    if not found:
        st.error("❗️ Не беше разчетен баркод. Увери се, че е ясен, хоризонтален и без размазване.")
