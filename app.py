import streamlit as st
from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode
import requests

st.title("📷 Barcode Scanner + Product Info")

uploaded_file = st.file_uploader("Качи снимка с баркод", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    # Конвертираме в numpy array за pyzbar
    image_np = np.array(image)

    # Сканираме баркода
    decoded_objects = decode(image_np)

    if decoded_objects:
        st.success(f"Намерени {len(decoded_objects)} баркод(а):")
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            st.write(f"Баркод: {barcode_data}")

            # Викаме Open Food Facts API
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode_data}.json"
            response = requests.get(url)
            data = response.json()

            if data.get("status") == 1:
                product = data["product"]
                st.subheader("Информация за продукта:")
                st.write(f"**Име:** {product.get('product_name', 'Няма данни')}")
                st.write(f"**Марка:** {product.get('brands', 'Няма данни')}")
                st.write(f"**Съставки:** {product.get('ingredients_text', 'Няма данни')}")
                st.write(f"**Нутриенти:** {product.get('nutriments', {})}")
            else:
                st.warning("Продуктът не е намерен в базата данни.")
    else:
        st.error("Не е намерен баркод на изображението. Опитай с друго изображение.")
