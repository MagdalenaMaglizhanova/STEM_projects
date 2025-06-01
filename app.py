import streamlit as st

st.title("STEM Проект: Вятърна Мелница с 3D визуализация")

# Слайдер за скорост на вятъра
wind_speed_input = st.slider(
    "Изберете скорост на вятъра (m/s)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.1
)

# HTML с Three.js визуализацията и използване на избраната скорост
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
<div id="info">💨 Вятър: <span id="windSpeed">{wind_speed_input:.1f}</span> m/s | ⚡ Енергия: <span id="energy">0</span> kWh</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<script>
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xaec6cf);

  const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.set(0, 3, 7);

  const renderer = new THREE.WebGLRenderer({{ antialias: true }});
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 10, 7);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x404040));

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({{ color: 0x228B22 }})
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);

  const pole = new THREE.Mesh(
    new THREE.CylinderGeometry(0.1, 0.2, 3),
    new THREE.MeshStandardMaterial({{ color: 0xffffff }})
  );
  pole.position.y = 1.5;
  scene.add(pole);

  const hub = new THREE.Mesh(
    new THREE.SphereGeometry(0.2),
    new THREE.MeshStandardMaterial({{ color: 0x999999 }})
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

  const windSpeed = {wind_speed_input};

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

# Показваме HTML в Streamlit
st.components.v1.html(threejs_html, height=500)
