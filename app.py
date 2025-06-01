import streamlit as st

st.title("STEM Проект: Холандска Вятърна Мелница с 3D визуализация")

wind_speed_input = st.slider(
    "Изберете скорост на вятъра (m/s)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.1
)

threejs_html = f"""
<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="UTF-8" />
  <title>STEM: Холандска Вятърна Мелница</title>
  <style>
    body {{ margin: 0; overflow: hidden; background-color: #a0c4ff; }}
    canvas {{ display: block; }}
    #info {{
      position: absolute;
      top: 10px; left: 10px;
      color: #222;
      background: rgba(255,255,255,0.8);
      padding: 10px;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      z-index: 10;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }}
  </style>
</head>
<body>
<div id="info">💨 Вятър: <span id="windSpeed">{wind_speed_input:.1f}</span> m/s | ⚡ Енергия: <span id="energy">0</span> kWh</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<script>
  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.set(0, 3, 7);

  const renderer = new THREE.WebGLRenderer({{ antialias: true }});
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 10, 7);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x404040));

  // Земя
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({{ color: 0x228B22 }})
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);

  // Стълб
  const pole = new THREE.Mesh(
    new THREE.CylinderGeometry(0.2, 0.3, 4),
    new THREE.MeshStandardMaterial({{ color: 0xffffff }})
  );
  pole.position.y = 2;
  scene.add(pole);

  // Главата на мелницата (кубична, за класически вид)
  const head = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshStandardMaterial({{ color: 0x8b4513 }})
  );
  head.position.y = 4;
  scene.add(head);

  // Перки - 4 големи плоски правоъгълника
  const blades = [];
  const bladeLength = 3.0;
  const bladeWidth = 0.4;

  for (let i = 0; i < 4; i++) {{
    const blade = new THREE.Mesh(
      new THREE.BoxGeometry(bladeLength, 0.15, bladeWidth),
      new THREE.MeshStandardMaterial({{ color: 0x8b4513 }})
    );
    blade.position.y = 4;
    blade.geometry.translate(bladeLength / 2, 0, 0);
    blade.rotation.z = i * (Math.PI / 2);
    scene.add(blade);
    blades.push(blade);
  }}

  let angle = 0;
  const windSpeed = {wind_speed_input};

  function animate() {{
    requestAnimationFrame(animate);
    angle += windSpeed * 0.01;
    blades.forEach((blade) => {{
      blade.rotation.y = angle;
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

st.components.v1.html(threejs_html, height=600)
