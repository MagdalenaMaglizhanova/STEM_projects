import streamlit as st

st.title("🌬️ STEM урок: Вятърни мелници")

# Урок
st.header("Как работи вятърната мелница?")
st.markdown("""
Вятърните мелници използват силата на вятъра, за да въртят лопатките си. Това въртене се преобразува в енергия, която може да се използва за различни неща — например за производство на електричество или за смилане на зърно.

- Вятърът създава сила, която завърта лопатките.
- Скоростта на вятъра влияе на скоростта на въртене и колко енергия се произвежда.
- Лопатките са проектирани така, че да използват максимално вятърната енергия.

> **Задача:** Разбери как силата на вятъра влияе на въртенето и енергията.
""")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Wind_turbine_blades_rotating_in_sunlight_%28cropped%29.jpg/320px-Wind_turbine_blades_rotating_in_sunlight_%28cropped%29.jpg", caption="Вятърна мелница")

#  Слайдер за сила на вятъра
wind_speed = st.slider("Избери сила на вятъра", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# 3D визуализация с получена стойност на wind_speed от Streamlit
threejs_html = f"""
<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="UTF-8" />
  <title>STEM: Вятърна Турбина</title>
  <style>
    body {{ margin: 0; overflow: hidden; }}
    canvas {{ display: block; }}
    #info {{
      position: absolute;
      top: 10px; left: 10px;
      color: white;
      background: rgba(0,0,0,0.5);
      padding: 10px;
      font-family: sans-serif;
      z-index: 10;
    }}
  </style>
</head>
<body>
<div id="info">💨 Вятър: <span id="windSpeed">{wind_speed:.1f}</span> | ⚡ Енергия: <span id="energy">0</span> kWh</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<script>
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xaec6cf);

  const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.set(0, 3, 7);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 10, 7);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x404040));

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({ color: 0x228B22 })
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);

  const pole = new THREE.Mesh(
    new THREE.CylinderGeometry(0.1, 0.2, 3),
    new THREE.MeshStandardMaterial({ color: 0xffffff })
  );
  pole.position.y = 1.5;
  scene.add(pole);

  const hub = new THREE.Mesh(
    new THREE.SphereGeometry(0.2),
    new THREE.MeshStandardMaterial({ color: 0x999999 })
  );
  hub.position.y = 3;
  scene.add(hub);

  const blades = [];
  for (let i = 0; i < 3; i++) {{
    const blade = new THREE.Mesh(
      new THREE.BoxGeometry(0.05, 1, 0.1),
      new THREE.MeshStandardMaterial({{ color: 0xff0000 }})
    );
    blade.position.y = 3;
    blade.geometry.translate(0, 0.5, 0);
    scene.add(blade);
    blades.push(blade);
  }}

  const windSpeed = {wind_speed};

  let angle = 0;
  function animate() {{
    requestAnimationFrame(animate);
    angle += windSpeed * 0.01;
    blades.forEach((blade, i) => {{
      const rot = angle + (i * Math.PI * 2 / 3);
      blade.position.x = Math.sin(rot) * 0.3;
      blade.position.z = Math.cos(rot) * 0.3;
      blade.rotation.y = rot;
    }});
    document.getElementById('windSpeed').textContent = windSpeed.toFixed(1);
    document.getElementById('energy').textContent = (windSpeed * 5).toFixed(0);
    renderer.render(scene, camera);
  }}
  animate();

  window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }});
</script>
</body>
</html>
"""

st.header("Тествай мелницата")
st.components.v1.html(threejs_html, height=600, scrolling=False)

# Хипотеза
st.header("Направи хипотеза")

hypothesis = st.text_area("Как смяташ, че ще се промени въртенето и енергията при увеличаване на силата на вятъра?", height=150)

if st.button("Изпрати хипотезата"):
    if hypothesis.strip() == "":
        st.warning("Моля, напиши хипотеза преди да изпратиш.")
    else:
        st.success("Благодарим! Твоята хипотеза е записана.")
        st.write("Твоята хипотеза:")
        st.write(hypothesis)
