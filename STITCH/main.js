/**
 * MAIN.JS — Controlador principal
 * Inicialización, navegación, eventos
 */

import { PRODUCTS, APPLE_LOGO_D } from './config.js';
import {
  buildIn, scatterOut, morphTo, stopFloat, spawnParticles,
  onMouseMove, updateUI, setWrapper
} from './animations.js';

const NS = 30; // 30 polígonos por producto
const LOGO_HTML = [
  // 0 - iPhone
  `<div style="position:absolute;top:${PRODUCTS[0].logoPos.top};left:${PRODUCTS[0].logoPos.left};transform:translate(-50%,-50%);">
    <svg viewBox="0 0 100 120" width="${PRODUCTS[0].logoPos.width}" height="${PRODUCTS[0].logoPos.height}">
      <path fill="rgba(255,255,255,0.22)" d="${APPLE_LOGO_D}"/>
    </svg>
  </div>`,
  // 1 - iPad
  `<div style="position:absolute;top:${PRODUCTS[1].logoPos.top};left:${PRODUCTS[1].logoPos.left};transform:translate(-50%,-50%);">
    <svg viewBox="0 0 100 120" width="${PRODUCTS[1].logoPos.width}" height="${PRODUCTS[1].logoPos.height}">
      <path fill="rgba(210,210,210,0.28)" d="${APPLE_LOGO_D}"/>
    </svg>
  </div>`,
  // 2 - MacBook
  `<div style="position:absolute;top:${PRODUCTS[2].logoPos.top};left:${PRODUCTS[2].logoPos.left};transform:translate(-50%,-50%);">
    <svg viewBox="0 0 100 120" width="${PRODUCTS[2].logoPos.width}" height="${PRODUCTS[2].logoPos.height}">
      <path fill="rgba(200,200,200,0.3)" d="${APPLE_LOGO_D}"/>
    </svg>
  </div>`,
  // 3 - AirPods
  `<div style="position:absolute;top:${PRODUCTS[3].logoPos.top};left:${PRODUCTS[3].logoPos.left};transform:translate(-50%,-50%);font-size:10px;color:rgba(255,255,255,0.5);font-weight:700;letter-spacing:2px;">AIRPODS</div>`,
  // 4 - Apple Watch
  `<div style="position:absolute;top:${PRODUCTS[4].logoPos.top};left:${PRODUCTS[4].logoPos.left};transform:translate(-50%,-50%);font-size:9px;color:rgba(255,255,255,0.5);font-weight:700;">⌚ WATCH</div>`,
  // 5 - PS5
  `<div style="position:absolute;top:${PRODUCTS[5].logoPos.top};left:${PRODUCTS[5].logoPos.left};transform:translate(-50%,-50%);text-align:center;">
    <svg viewBox="0 0 120 30" width="60" height="15" style="filter:drop-shadow(0 0 6px rgba(100,200,255,0.6));">
      <polygon points="15,4 25,24 5,24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="45" cy="15" r="10" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5"/>
      <path d="M68,8 L82,22 M68,22 L82,8" stroke="rgba(255,255,255,0.8)" stroke-width="2.5" stroke-linecap="round"/>
      <rect x="95" y="5" width="20" height="20" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5" stroke-linejoin="round"/>
    </svg>
    <div style="color:rgba(255,255,255,0.5);font-size:8px;letter-spacing:4px;margin-top:8px;font-weight:700;font-family:'Inter',sans-serif;">PS5</div>
  </div>`
];

let current = 0; // Índice de producto actual (0-5)
let morphState = 'A'; // Estado de morphing (A o B)
let locked = false;
let polys = [];

/**
 * Inicializar SVG con polígonos
 */
function createPolygons() {
  const svg = document.getElementById('product-svg');
  polys = [];
  for (let i = 0; i < NS; i++) {
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    p.id = 'sh' + i;
    svg.appendChild(p);
    polys.push(p);
  }
}

/**
 * Aplicar shards iniciales
 */
function applyShards(pi) {
  const prod = PRODUCTS[pi];
  prod.shardsA.forEach((s, i) => {
    polys[i].setAttribute('points', s[0]);
    polys[i].setAttribute('fill', s[1]);
    gsap.set(polys[i], { opacity: s[2] });
  });
}

/**
 * Navegar entre productos (0-5)
 */
function navProduct(dir) {
  if (locked) return;
  const newIdx = (current + dir + 6) % 6;
  goToProduct(newIdx);
}

/**
 * IR a un producto específico
 */
function goToProduct(ni) {
  if (locked || ni === current) return;
  locked = true;
  morphState = 'A'; // Resetear a estado normal

  const oldProd = PRODUCTS[current];
  const newProd = PRODUCTS[ni];
  current = ni;

  stopFloat();
  gsap.to('#logo-overlay', { opacity: 0, duration: 0.2 });
  setWrapper(ni, true);
  updateUI(ni);
  spawnParticles(newProd.accent);

  const tl = gsap.timeline({
    onComplete: () => {
      locked = false;
      document.getElementById('logo-overlay').innerHTML = LOGO_HTML[current];
      gsap.fromTo('#logo-overlay', { opacity: 0 }, { opacity: 1, duration: 0.8, ease: 'power2.out' });
      buildIn(polys, current);
    }
  });

  polys.forEach((p, i) => {
    const targetShard = newProd.shardsA[i];
    const ang = Math.random() * Math.PI * 2;
    const d = 120 + Math.random() * 100;

    const polyTl = gsap.timeline();
    polyTl.to(p, {
      x: Math.cos(ang) * d,
      y: Math.sin(ang) * d,
      rotation: Math.random() * 180 - 90,
      scale: 0.6 + Math.random() * 0.4,
      attr: { points: targetShard[0], fill: targetShard[1] },
      opacity: 0.5 + targetShard[2] * 0.5,
      duration: 0.55,
      ease: 'power2.out'
    }, 0);

    polyTl.to(p, {
      x: 0,
      y: 0,
      rotation: 0,
      scale: 1,
      opacity: targetShard[2],
      duration: 1.2,
      ease: 'expo.inOut'
    });

    tl.add(polyTl, i * 0.035);
  });
}

/**
 * Morphing ENTRE ESTADOS A/B en el mismo producto
 */
function toggleMorph() {
  if (locked) return;
  locked = true;
  morphState = morphState === 'A' ? 'B' : 'A';

  morphTo(polys, current, morphState);

  setTimeout(() => locked = false, 1200);
}

/**
 * Inicialización principal
 */
function init() {
  createPolygons();
  applyShards(0);
  setWrapper(0, false);
  buildIn(polys, 0, true);
  updateUI(0);

  document.getElementById('logo-overlay').innerHTML = LOGO_HTML[0];
  gsap.fromTo('#logo-overlay', { opacity: 0 }, { opacity: 1, duration: 0.8, ease: 'power2.out' });

  // Event Listeners
  document.getElementById('btn-next').addEventListener('click', () => navProduct(1));
  document.getElementById('btn-prev').addEventListener('click', () => navProduct(-1));

  // Dots para morphing A/B (no productos)
  document.querySelectorAll('.dot').forEach((d, i) => {
    d.addEventListener('click', toggleMorph);
  });

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseleave', () => {
    gsap.to('#light-point', { opacity: 0, duration: 0.8 });
  });

  // Teclado: flechas para productos
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navProduct(1);
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') navProduct(-1);
  });

  // Click en SVG para abrir tienda (Fase 2)
  document.getElementById('svg-wrapper').addEventListener('click', () => {
    console.log('Tienda será implementada en Fase 2');
  });
}

// Esperar a que GSAP esté listo
window.addEventListener('load', init);
