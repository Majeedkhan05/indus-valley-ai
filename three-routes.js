/* =========================================================
   3D Trade Routes — flowing arcs over a stylized world disc
   Author: AI Hub Projects
   ========================================================= */
import * as THREE from 'three';

const canvas = document.getElementById('routes-canvas');
if (canvas) initRoutes(canvas);

function initRoutes(canvas) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0a0a0a, 0.05);

  const camera = new THREE.PerspectiveCamera(40, canvas.clientWidth / canvas.clientHeight, 0.1, 200);
  camera.position.set(0, 4.5, 9);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;

  // ── lights
  scene.add(new THREE.AmbientLight(0x352a18, 0.7));
  const k = new THREE.DirectionalLight(0xffd97a, 1.4); k.position.set(5, 8, 4); scene.add(k);
  const fill = new THREE.PointLight(0xb55530, 1.1, 24); fill.position.set(-4, -1, 3); scene.add(fill);

  // ── ground disc — stylized "world" plate
  const discGeo = new THREE.CircleGeometry(6, 96);
  const discMat = new THREE.MeshStandardMaterial({
    color: 0x1A1714, roughness: 0.9, metalness: 0.15,
    emissive: 0x1a1408, emissiveIntensity: 0.25
  });
  const disc = new THREE.Mesh(discGeo, discMat);
  disc.rotation.x = -Math.PI / 2;
  disc.position.y = -0.05;
  scene.add(disc);

  // grid lines on disc
  const gridGeo = new THREE.RingGeometry(5.95, 6, 96);
  const gridMat = new THREE.MeshBasicMaterial({ color: 0xC2A878, side: THREE.DoubleSide, transparent: true, opacity: 0.45 });
  const grid = new THREE.Mesh(gridGeo, gridMat); grid.rotation.x = -Math.PI / 2; grid.position.y = -0.04;
  scene.add(grid);
  for (let r = 1; r < 6; r++) {
    const ringGeo = new THREE.RingGeometry(r, r + 0.005, 96);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xC2A878, side: THREE.DoubleSide, transparent: true, opacity: 0.13 });
    const ring = new THREE.Mesh(ringGeo, ringMat); ring.rotation.x = -Math.PI / 2; ring.position.y = -0.04;
    scene.add(ring);
  }

  // ── nodes (cities)
  const NODES = [
    // [name, x, z, color, scale]
    ['Indus',     0.0,  0.0, 0xD4AF37, 1.0],
    ['Shortugai', -1.0, -2.4, 0xC2A878, 0.7],
    ['Magan',     2.4,  1.8, 0xB55530, 0.7],
    ['Dilmun',    1.8,  1.0, 0xC2A878, 0.7],
    ['Meluhha',   0.6,  0.4, 0xD4AF37, 0.6],
    ['Sumer',     3.6,  2.6, 0xff9b3c, 0.85],
    ['Susa',      3.2,  1.2, 0xff9b3c, 0.7],
    ['Lothal',   -0.4,  1.6, 0xD4AF37, 0.65],
    ['Dholavira', 0.4,  1.2, 0xD4AF37, 0.7]
  ];

  const nodeGroup = new THREE.Group();
  scene.add(nodeGroup);

  NODES.forEach(([name, x, z, color, s]) => {
    // pillar
    const pillarH = 0.05 + s * 0.08;
    const pillarGeo = new THREE.CylinderGeometry(0.045 * s, 0.05 * s, pillarH, 16);
    const pillarMat = new THREE.MeshStandardMaterial({ color, roughness: 0.4, metalness: 0.6, emissive: color, emissiveIntensity: 0.6 });
    const pillar = new THREE.Mesh(pillarGeo, pillarMat);
    pillar.position.set(x, pillarH / 2, z);
    nodeGroup.add(pillar);

    // glowing top node
    const dotGeo = new THREE.SphereGeometry(0.08 * s, 14, 14);
    const dotMat = new THREE.MeshBasicMaterial({ color });
    const dot = new THREE.Mesh(dotGeo, dotMat);
    dot.position.set(x, pillarH + 0.04, z);
    nodeGroup.add(dot);

    // halo ring
    const haloGeo = new THREE.RingGeometry(0.16 * s, 0.18 * s, 32);
    const haloMat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.55, side: THREE.DoubleSide });
    const halo = new THREE.Mesh(haloGeo, haloMat);
    halo.rotation.x = -Math.PI / 2; halo.position.set(x, 0.001, z);
    nodeGroup.add(halo);
    halo.userData = { baseScale: 1, t: Math.random() * Math.PI * 2 };
  });

  // ── arc routes — Indus → others
  const ROUTES = [
    [0, 1], // Indus → Shortugai
    [0, 2], // Indus → Magan
    [0, 3], // Indus → Dilmun
    [0, 5], // Indus → Sumer
    [3, 6], // Dilmun → Susa
    [2, 5], // Magan → Sumer
    [0, 7], // Indus → Lothal
    [0, 8]  // Indus → Dholavira
  ];

  const arcs = [];
  ROUTES.forEach(([i, j]) => {
    const a = new THREE.Vector3(NODES[i][1], 0.05, NODES[i][2]);
    const b = new THREE.Vector3(NODES[j][1], 0.05, NODES[j][2]);
    const dist = a.distanceTo(b);
    const mid = a.clone().add(b).multiplyScalar(0.5);
    mid.y = 0.4 + dist * 0.35;
    const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
    const tubeGeo = new THREE.TubeGeometry(curve, 48, 0.012, 8, false);
    const tubeMat = new THREE.MeshBasicMaterial({ color: 0xC2A878, transparent: true, opacity: 0.35 });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    scene.add(tube);

    // travelling spark
    const sparkGeo = new THREE.SphereGeometry(0.06, 12, 12);
    const sparkMat = new THREE.MeshBasicMaterial({ color: 0xD4AF37 });
    const spark = new THREE.Mesh(sparkGeo, sparkMat);
    scene.add(spark);

    // small glowing trail
    const trailMat = new THREE.MeshBasicMaterial({ color: 0xD4AF37, transparent: true, opacity: 0.15 });
    const trail = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), trailMat);
    scene.add(trail);

    arcs.push({ curve, spark, trail, t: Math.random(), speed: 0.0025 + Math.random() * 0.0035 });
  });

  // ── ambient sparks (gold dust)
  const dustCount = reduced ? 0 : 240;
  if (dustCount) {
    const positions = new Float32Array(dustCount * 3);
    const speeds = new Float32Array(dustCount);
    for (let i = 0; i < dustCount; i++) {
      positions[i*3] = (Math.random()-0.5) * 14;
      positions[i*3+1] = Math.random() * 5;
      positions[i*3+2] = (Math.random()-0.5) * 14;
      speeds[i] = 0.0008 + Math.random() * 0.002;
    }
    const dGeo = new THREE.BufferGeometry();
    dGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const dMat = new THREE.PointsMaterial({ color: 0xC2A878, size: 0.025, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending });
    const dust = new THREE.Points(dGeo, dMat);
    dust.userData = { positions, speeds };
    scene.add(dust);
  }

  // ── camera orbit
  let scrollY = 0;
  window.addEventListener('scroll', () => { scrollY = window.scrollY; }, { passive: true });

  const target = { x: 0, y: 0 };
  window.addEventListener('pointermove', (e) => {
    const rect = canvas.getBoundingClientRect();
    if (e.clientY < rect.top || e.clientY > rect.bottom) return;
    target.x = ((e.clientX - rect.left) / rect.width - 0.5) * 0.6;
    target.y = ((e.clientY - rect.top) / rect.height - 0.5) * 0.4;
  }, { passive: true });

  function onResize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
  }
  window.addEventListener('resize', onResize);

  const clock = new THREE.Clock();
  let frameId;
  function animate() {
    const t = clock.getElapsedTime();

    // gentle camera orbit
    const baseR = 9, baseY = 4.5;
    const angle = t * 0.05 + target.x * 0.6;
    camera.position.x = Math.sin(angle) * baseR * 0.18;
    camera.position.z = Math.cos(angle) * baseR;
    camera.position.y = baseY + target.y * 1.5 + Math.sin(t * 0.4) * 0.15;
    camera.lookAt(0, 0.4, 0);

    // pulsing halos
    nodeGroup.children.forEach(c => {
      if (c.userData && c.userData.baseScale !== undefined) {
        c.userData.t += 0.03;
        const s = 1 + Math.sin(c.userData.t) * 0.15;
        c.scale.set(s, s, 1);
        c.material.opacity = 0.4 + Math.sin(c.userData.t) * 0.25;
      }
    });

    // arc travel
    arcs.forEach(a => {
      a.t += a.speed;
      if (a.t > 1) a.t = 0;
      const p = a.curve.getPoint(a.t);
      a.spark.position.copy(p);
      a.trail.position.copy(p);
      a.trail.scale.setScalar(0.7 + Math.sin(t * 4 + a.t * 6) * 0.2);
    });

    // dust drift
    const dust = scene.children.find(c => c.type === 'Points');
    if (dust) {
      const pos = dust.userData.positions, sp = dust.userData.speeds;
      for (let i = 0; i < sp.length; i++) {
        pos[i*3+1] += sp[i];
        if (pos[i*3+1] > 5) pos[i*3+1] = 0;
      }
      dust.geometry.attributes.position.needsUpdate = true;
    }

    renderer.render(scene, camera);
    frameId = requestAnimationFrame(animate);
  }
  animate();

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting && frameId) { cancelAnimationFrame(frameId); frameId = null; }
      else if (e.isIntersecting && !frameId) { animate(); }
    });
  }, { threshold: 0 });
  io.observe(canvas);
}
