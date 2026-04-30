/* =========================================================
   3D Hero Scene — rotating Indus seal + ambient dust
   Author: AI Hub Projects (Mohammed Majeed Khan)
   ========================================================= */
import * as THREE from 'three';

const canvas = document.getElementById('seal-canvas');
if (canvas) initScene(canvas);

function initScene(canvas) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0F0F0F, 0.04);

  const camera = new THREE.PerspectiveCamera(
    38,
    canvas.clientWidth / canvas.clientHeight,
    0.1,
    100
  );
  camera.position.set(0, 0.2, 7.2);

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  // ── lights ─────────────────────────────────────
  const ambient = new THREE.AmbientLight(0x352a18, 0.8);
  scene.add(ambient);

  const key = new THREE.DirectionalLight(0xffd97a, 1.7);
  key.position.set(3, 4, 5);
  scene.add(key);

  const rim = new THREE.PointLight(0xffba5c, 1.6, 24, 1.6);
  rim.position.set(-4, 2, -2);
  scene.add(rim);

  const back = new THREE.PointLight(0xb55530, 1.4, 30, 2);
  back.position.set(2, -2, -4);
  scene.add(back);

  // ── Indus seal (procedural disc + engraved motif) ──
  const sealGroup = new THREE.Group();
  scene.add(sealGroup);

  const sealRadius = 1.6;
  const sealThick = 0.25;

  // base disc — square seal with rounded edges (steatite look)
  const baseGeo = roundedBoxGeometry(sealRadius * 2, sealRadius * 2, sealThick, 0.08, 6);
  const baseMat = new THREE.MeshStandardMaterial({
    color: 0xC2A878,
    roughness: 0.55,
    metalness: 0.25,
    emissive: 0x2a1f10,
    emissiveIntensity: 0.18
  });
  const base = new THREE.Mesh(baseGeo, baseMat);
  sealGroup.add(base);

  // raised border ring on the front
  const borderGeo = new THREE.TorusGeometry(sealRadius * 0.92, 0.018, 16, 96);
  const borderMat = new THREE.MeshStandardMaterial({
    color: 0xD4AF37,
    roughness: 0.35, metalness: 0.6,
    emissive: 0x4a3010, emissiveIntensity: 0.4
  });
  const border = new THREE.Mesh(borderGeo, borderMat);
  border.position.z = sealThick / 2 + 0.001;
  sealGroup.add(border);

  // engraved motif — stylized "unicorn / one-horned bull" + script line
  const engravedMat = new THREE.MeshStandardMaterial({
    color: 0x8C7438,
    roughness: 0.85, metalness: 0.2,
    emissive: 0x1a1408, emissiveIntensity: 0.4
  });

  // animal silhouette via tube paths (procedural)
  const animalShape = new THREE.Shape();
  // body — flowing single-line bull, abstract
  animalShape.moveTo(-0.65, -0.05);
  animalShape.bezierCurveTo(-0.6, 0.18, -0.3, 0.28, 0.0, 0.2);
  animalShape.bezierCurveTo(0.35, 0.15, 0.55, 0.25, 0.62, 0.05);
  animalShape.bezierCurveTo(0.7, -0.12, 0.55, -0.18, 0.4, -0.18);
  animalShape.lineTo(0.4, -0.4);
  animalShape.lineTo(0.32, -0.4);
  animalShape.lineTo(0.32, -0.18);
  animalShape.lineTo(-0.2, -0.18);
  animalShape.lineTo(-0.2, -0.4);
  animalShape.lineTo(-0.28, -0.4);
  animalShape.lineTo(-0.28, -0.18);
  animalShape.bezierCurveTo(-0.5, -0.18, -0.62, -0.12, -0.65, -0.05);
  animalShape.closePath();

  const animalGeo = new THREE.ExtrudeGeometry(animalShape, {
    depth: 0.04,
    bevelEnabled: true,
    bevelThickness: 0.012,
    bevelSize: 0.012,
    bevelSegments: 2
  });
  animalGeo.translate(0, -0.05, 0);
  const animal = new THREE.Mesh(animalGeo, engravedMat);
  animal.position.z = sealThick / 2 + 0.005;
  animal.scale.set(1.1, 1.1, 1);
  sealGroup.add(animal);

  // separate horn so it overlaps cleanly
  const hornShape = new THREE.Shape();
  hornShape.moveTo(0.5, 0.18);
  hornShape.lineTo(0.84, 0.6);
  hornShape.lineTo(0.78, 0.62);
  hornShape.lineTo(0.46, 0.22);
  hornShape.closePath();
  const hornGeo = new THREE.ExtrudeGeometry(hornShape, {
    depth: 0.04, bevelEnabled: true, bevelThickness: 0.01, bevelSize: 0.01, bevelSegments: 2
  });
  hornGeo.translate(0, -0.05, 0);
  const hornMesh = new THREE.Mesh(hornGeo, engravedMat);
  hornMesh.position.z = sealThick / 2 + 0.005;
  hornMesh.scale.set(1.1, 1.1, 1);
  sealGroup.add(hornMesh);

  // sacred manger / standard at front
  const mangerShape = new THREE.Shape();
  mangerShape.moveTo(-0.95, -0.5);
  mangerShape.lineTo(-0.7, -0.5);
  mangerShape.lineTo(-0.7, -0.4);
  mangerShape.lineTo(-0.78, -0.4);
  mangerShape.lineTo(-0.78, -0.25);
  mangerShape.lineTo(-0.86, -0.25);
  mangerShape.lineTo(-0.86, -0.4);
  mangerShape.lineTo(-0.95, -0.4);
  mangerShape.closePath();
  const mangerGeo = new THREE.ExtrudeGeometry(mangerShape, { depth: 0.04, bevelEnabled: false });
  const manger = new THREE.Mesh(mangerGeo, engravedMat);
  manger.position.z = sealThick / 2 + 0.005;
  manger.scale.set(1.1, 1.1, 1);
  sealGroup.add(manger);

  // top register — proxy "script signs" as small bumps
  const signs = new THREE.Group();
  const signGeoTemplates = [
    new THREE.BoxGeometry(0.12, 0.1, 0.04),
    new THREE.CylinderGeometry(0.05, 0.05, 0.04, 16),
    new THREE.BoxGeometry(0.06, 0.16, 0.04),
    new THREE.TorusGeometry(0.06, 0.018, 12, 24)
  ];
  const signCount = 7;
  for (let i = 0; i < signCount; i++) {
    const tmpl = signGeoTemplates[i % signGeoTemplates.length].clone();
    const sign = new THREE.Mesh(tmpl, engravedMat);
    const x = -0.95 + i * (1.9 / (signCount - 1));
    sign.position.set(x, 0.78, sealThick / 2 + 0.025);
    if (tmpl.type === 'CylinderGeometry') sign.rotation.x = Math.PI / 2;
    signs.add(sign);
  }
  sealGroup.add(signs);

  // backing plate behind seal — metallic disc for depth
  const backingGeo = new THREE.CircleGeometry(sealRadius * 1.45, 64);
  const backingMat = new THREE.MeshStandardMaterial({
    color: 0x2a1f10, roughness: 0.4, metalness: 0.7,
    transparent: true, opacity: 0.65
  });
  const backing = new THREE.Mesh(backingGeo, backingMat);
  backing.position.z = -0.5;
  scene.add(backing);

  // glowing ring around the seal
  const ringGeo = new THREE.RingGeometry(sealRadius * 1.55, sealRadius * 1.6, 128);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0xD4AF37, transparent: true, opacity: 0.35, side: THREE.DoubleSide });
  const ring = new THREE.Mesh(ringGeo, ringMat);
  ring.position.z = -0.4;
  scene.add(ring);

  // outer wide ring — softer
  const outerGeo = new THREE.RingGeometry(sealRadius * 1.85, sealRadius * 1.88, 128);
  const outerMat = new THREE.MeshBasicMaterial({ color: 0xC2A878, transparent: true, opacity: 0.18, side: THREE.DoubleSide });
  const outerRing = new THREE.Mesh(outerGeo, outerMat);
  outerRing.position.z = -0.45;
  scene.add(outerRing);

  // ── particles (dust) ────────────────────────
  const particleCount = reducedMotion ? 0 : 600;
  if (particleCount > 0) {
    const positions = new Float32Array(particleCount * 3);
    const speeds = new Float32Array(particleCount);
    for (let i = 0; i < particleCount; i++) {
      positions[i * 3 + 0] = (Math.random() - 0.5) * 18;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 12;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10 - 2;
      speeds[i] = 0.0008 + Math.random() * 0.0025;
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const pMat = new THREE.PointsMaterial({
      size: 0.025, color: 0xD4AF37, transparent: true, opacity: 0.7,
      depthWrite: false, blending: THREE.AdditiveBlending
    });
    const dust = new THREE.Points(pGeo, pMat);
    scene.add(dust);
    dust.userData.speeds = speeds;
    dust.userData.positions = positions;
  }

  // ── pointer parallax ──────────────────────
  const target = { x: 0, y: 0 };
  const current = { x: 0, y: 0 };
  window.addEventListener('pointermove', (e) => {
    const nx = (e.clientX / window.innerWidth) * 2 - 1;
    const ny = (e.clientY / window.innerHeight) * 2 - 1;
    target.x = nx * 0.35;
    target.y = -ny * 0.25;
  }, { passive: true });

  // ── scroll-driven tilt ─────────────────────
  let scrollY = 0;
  window.addEventListener('scroll', () => { scrollY = window.scrollY; }, { passive: true });

  // ── resize ─────────────────────────────────
  function onResize() {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
  }
  window.addEventListener('resize', onResize);

  // ── animate ────────────────────────────────
  const clock = new THREE.Clock();
  let frameId;
  function animate() {
    const t = clock.getElapsedTime();

    // smooth parallax
    current.x += (target.x - current.x) * 0.05;
    current.y += (target.y - current.y) * 0.05;

    if (!reducedMotion) {
      sealGroup.rotation.y = current.x + Math.sin(t * 0.25) * 0.18 + scrollY * 0.0008;
      sealGroup.rotation.x = current.y * 0.5 + Math.sin(t * 0.15) * 0.05;
      sealGroup.position.y = Math.sin(t * 0.7) * 0.06 - scrollY * 0.0015;
      ring.rotation.z = t * 0.05;
      outerRing.rotation.z = -t * 0.03;

      const dust = scene.children.find(c => c.type === 'Points');
      if (dust) {
        const positions = dust.userData.positions;
        const speeds = dust.userData.speeds;
        for (let i = 0; i < speeds.length; i++) {
          positions[i * 3 + 1] += speeds[i];
          if (positions[i * 3 + 1] > 6) positions[i * 3 + 1] = -6;
        }
        dust.geometry.attributes.position.needsUpdate = true;
      }
    } else {
      sealGroup.rotation.y = current.x;
      sealGroup.rotation.x = current.y * 0.5;
    }

    renderer.render(scene, camera);
    frameId = requestAnimationFrame(animate);
  }
  animate();

  // pause when off-screen for perf
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting && frameId) {
        cancelAnimationFrame(frameId); frameId = null;
      } else if (e.isIntersecting && !frameId) {
        animate();
      }
    });
  }, { threshold: 0 });
  io.observe(canvas);
}

/* helper — rounded box */
function roundedBoxGeometry(width, height, depth, radius, smoothness) {
  const shape = new THREE.Shape();
  const eps = 0.00001;
  const w = width / 2 - radius;
  const h = height / 2 - radius;
  shape.absarc(eps - w, eps - h, eps, -Math.PI / 2, -Math.PI, true);
  shape.absarc(eps - w, h - eps, eps, Math.PI, Math.PI / 2, true);
  shape.absarc(w - eps, h - eps, eps, Math.PI / 2, 0, true);
  shape.absarc(w - eps, eps - h, eps, 0, -Math.PI / 2, true);
  const geo = new THREE.ExtrudeGeometry(shape, {
    depth: depth - radius * 2,
    bevelEnabled: true,
    bevelSegments: smoothness * 2,
    steps: 1,
    bevelSize: radius - eps,
    bevelThickness: radius,
    curveSegments: smoothness
  });
  geo.center();
  return geo;
}
