import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="STEM Соларен Панел", layout="centered")

st.title("🔆 Влияние на ъгъла върху ефективността на соларен панел")

# 1. Теоретична част
with st.expander("📘 Научи повече"):
    st.markdown("""
    Слънчевите панели преобразуват светлината в електрическа енергия.
    Един от ключовите фактори, който влияе на ефективността им, е **ъгълът под който слънчевите лъчи попадат върху панела**.
    
    Колкото по-перпендикулярно светлината пада върху панела, толкова по-голямо количество енергия се абсорбира.
    """)

# 2. Симулация с 3D визуализация
st.subheader("🧪 Изпробвай как ъгълът влияе на енергийния добив")

angle = st.slider("Избери ъгъл на слънчевите лъчи спрямо панела (в градуси)", 0, 90, 45)

# Симулиран добив (максимален при 0 градуса)
energy_output = np.cos(np.radians(angle)) * 100  # % от максимума

fig = go.Figure(data=[go.Surface(
    z=[[energy_output]*5]*5, 
    colorscale='YlOrRd',
    showscale=False
)])
fig.update_layout(
    title=f"Енергиен добив: {energy_output:.1f}%",
    scene=dict(
        zaxis_title='Добив (%)',
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis=dict(range=[0, 100])
    ),
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# 3. Хипотеза
st.subheader("🧠 Формулирай хипотеза")
hypothesis = st.text_area("Какво ще стане, ако променим ъгъла или положението на панела?", "")

# 4. Проектна идея
st.subheader("🛠️ Твоята идея")
idea = st.text_area("Измисли проект, в който използваш соларна енергия – например зарядно устройство, лампа и т.н.", "")

if st.button("📤 Изпрати"):
    st.success("Браво! Успешно формулира хипотеза и идея за проект!")

---

