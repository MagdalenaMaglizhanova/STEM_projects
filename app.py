import streamlit as st
from PIL import Image
import numpy as np
import cv2
import requests

st.title("Barcode Scanner с OpenCV и Open Food Facts")

uploaded_file = st.file_uploader("Качи снимка с баркод", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Качена снимка", use_column_width=True)

    # Конвертираме PIL image в numpy array за OpenCV
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Инициализираме OpenCV barcode detector
    detector = cv2.barcode_BarcodeDetector()

    # Опитваме да открием и декодираме баркод
    ok, decoded_info, decoded_type, points = detector.detectAndDecode(img)

    if ok and decoded_info:
        barcode = decoded_info[0]
        st.success(f"Разпознат баркод: {barcode}")

        # Търсим продукта в Open Food Facts
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(url)
        if response.status_code == 200:
            product_data = response.json()
            if product_data.get("status") == 1:
                product = product_data["product"]
                st.subheader(product.get("product_name", "Име не е налично"))
                st.write(f"Бранд: {product.get('brands', 'Няма информация')}")
                st.write(f"Съставки: {product.get('ingredients_text', 'Няма информация')}")
                st.write(f"Енергийна стойност: {product.get('nutriments', {}).get('energy-kcal_100g', 'Няма информация')} kcal/100g")
                if 'image_url' in product:
                    st.image(product['image_url'], caption="Продуктова снимка")
            else:
                st.error("Продуктът не е намерен в Open Food Facts.")
        else:
            st.error("Грешка при връзката с Open Food Facts API.")
    else:
        st.error("Не можа да се разчете баркод от снимката.")
