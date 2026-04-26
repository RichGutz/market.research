/**
 * ANIMATIONS.JS — Timelines GSAP reutilizables
 * Sincronización de morphing y efectos visuales
 */

import { PRODUCTS } from './config.js';

let floatAnim = null;

/**
 * Construir todos los polígonos (entrada inicial)
 */
function buildIn(polys, current, isFirst = false) {
  const prod = PRODUCTS[current];
  const tl = gsap.timeline({
    onComplete: () => startFloat(polys, current)
  });

  polys.forEach((p, i) => {
    const shard = prod.shardsA[i];
    tl.to(p, {
      attr: { points: shard[0], fill: shard[1] },
      x: 0,
      y: 0,
      scale: 1,
      rotation: 0,
      opacity: shard[2],
      duration: isFirst ? 1.4 : 1.1,
      ease: 'expo.out'
    }, i * 0.055);
  });

  return tl;
}

/**
 * Dispersar polígonos para salida (al abrir tienda)
 */
function scatterOut(polys) {
  stopFloat();
  const tl = gsap.timeline();
  polys.forEach((p, i) => {
    const ang = Math.random() * Math.PI * 2;
    const d = 800 + Math.random() * 600;
    tl.to(p, {
      x: Math.cos(ang) * d,
      y: Math.sin(ang) * d,
      rotation: Math.random() * 800 - 400,
      scale: 0.2,
      opacity: 0,
      duration: 0.8,
      ease: 'power4.in'
    }, i * 0.015);
  });
  return tl;
}

/**
 * Morphing ENTRE ESTADOS (A ↔ B dentro de la misma categoría)
 */
function morphTo(polys, current, targetState) {
  const prod = PRODUCTS[current];
  const targetShards = targetState === 'A' ? prod.shardsA : prod.shardsB;

  const tl = gsap.timeline({
    onComplete: () => startFloat(polys, current)
  });

  polys.forEach((p, i) => {
    const targetShard = targetShards[i];
    const ang = Math.random() * Math.PI * 2;
    const d = 80 + Math.random() * 60;

    const polyTl = gsap.timeline();

    // Fase 1: Explosión suave + Morphing en vuelo
    polyTl.to(p, {
      x: Math.cos(ang) * d,
      y: Math.sin(ang) * d,
      rotation: Math.random() * 180 - 90,
      scale: 0.7 + Math.random() * 0.3,
      attr: { points: targetShard[0], fill: targetShard[1] },
      opacity: 0.6 + targetShard[2] * 0.4,
      duration: 0.45,
      ease: 'power2.out'
    }, 0);

    // Fase 2: Ensamblaje en nueva posición
    polyTl.to(p, {
      x: 0,
      y: 0,
      rotation: 0,
      scale: 1,
      opacity: targetShard[2],
      duration: 0.95,
      ease: 'expo.inOut'
    });

    tl.add(polyTl, i * 0.035);
  });

  return tl;
}

/**
 * Flotación continua (hover effect)
 */
function startFloat(polys, current) {
  floatAnim = gsap.to(polys, {
    y: -11,
    duration: 2.8,
    ease: 'sine.inOut',
    yoyo: true,
    repeat: -1
  });
}

/**
 * Detener flotación
 */
function stopFloat() {
  if (floatAnim) {
    floatAnim.kill();
    floatAnim = null;
  }
  gsap.to('svg polygon', { y: 0, duration: 0.3 });
}

/**
 * Spawn partículas (efecto de transición)
 */
function spawnParticles(color) {
  const container = document.getElementById('particles-container');
  for (let i = 0; i < 40; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.background = color;
    p.style.boxShadow = `0 0 10px ${color}`;
    if (Math.random() > 0.5) p.style.borderRadius = '0%';
    container.appendChild(p);

    const angle = Math.random() * Math.PI * 2;
    const velocity = 80 + Math.random() * 300;

    gsap.to(p, {
      x: Math.cos(angle) * velocity,
      y: Math.sin(angle) * velocity,
      rotation: Math.random() * 360,
      scale: Math.random() * 3,
      opacity: 0.8,
      duration: 0.2 + Math.random() * 0.4,
      ease: 'power3.out',
      onComplete: () => {
        gsap.to(p, {
          opacity: 0,
          scale: 0,
          y: '+=50',
          duration: 0.6 + Math.random() * 1.2,
          ease: 'power2.in',
          onComplete: () => p.remove()
        });
      }
    });
  }
}

/**
 * Luz dinámica que sigue el mouse
 */
function onMouseMove(e) {
  const cx = window.innerWidth / 2;
  const cy = window.innerHeight / 2;
  const rx = ((e.clientY - cy) / cy) * -9;
  const ry = ((e.clientX - cx) / cx) * 13;

  gsap.to('#svg-wrapper', {
    rotateX: rx,
    rotateY: ry,
    duration: 0.85,
    ease: 'power2.out'
  });

  gsap.to('#light-point', {
    x: e.clientX,
    y: e.clientY,
    opacity: 0.15,
    duration: 0.4,
    ease: 'power2.out'
  });

  const intensity = Math.abs(rx) + Math.abs(ry);
  gsap.to('#glass-overlay', {
    opacity: 0.1 + intensity * 0.02,
    duration: 0.5
  });
}

/**
 * Actualizar UI (colores, texto, dots)
 */
function updateUI(pi) {
  const p = PRODUCTS[pi];
  const els = ['#prod-name', '#prod-label', '#prod-price'];

  gsap.to(els, {
    opacity: 0,
    y: -10,
    duration: 0.22,
    onComplete: () => {
      document.getElementById('prod-name').textContent = p.name;
      document.getElementById('prod-label').textContent = p.label;
      document.getElementById('prod-price').innerHTML = `Desde <span>${p.price}</span>`;
      gsap.to(els, { opacity: 1, y: 0, duration: 0.34 });
    }
  });

  document.documentElement.style.setProperty('--accent', p.accent);
  document.documentElement.style.setProperty('--bg-color', p.bg || '#09090b');
  document.getElementById('glow-bg').style.background =
    `radial-gradient(ellipse 70% 60% at 50% 52%, ${p.glow} 0%, transparent 70%)`;
  document.getElementById('product-svg').style.filter =
    `drop-shadow(0 20px 55px ${p.shadow})`;

  document.querySelectorAll('.dot').forEach((d, i) => {
    const isActive = i === pi;
    d.classList.toggle('active', isActive);
    d.style.background = isActive ? p.accent : 'rgba(255,255,255,.2)';
    d.style.boxShadow = isActive ? `0 0 14px ${p.accent}` : 'none';
  });
}

/**
 * Ajustar tamaño del SVG wrapper
 */
function setWrapper(pi, animate = false) {
  const p = PRODUCTS[pi];
  const vh = window.innerHeight;
  const vw = window.innerWidth;
  const maxH = Math.min(p.wh, vh * 0.6);
  const maxW = Math.min(p.ww, vw * 0.82);
  const ratio = p.ww / p.wh;

  let fw = maxW;
  let fh = fw / ratio;
  if (fh > maxH) {
    fh = maxH;
    fw = fh * ratio;
  }

  const el = document.getElementById('svg-wrapper');
  if (animate) {
    gsap.to(el, { width: fw, height: fh, duration: 0.45, ease: 'power2.inOut' });
  } else {
    gsap.set(el, { width: fw, height: fh });
  }
}

export {
  buildIn,
  scatterOut,
  morphTo,
  startFloat,
  stopFloat,
  spawnParticles,
  onMouseMove,
  updateUI,
  setWrapper
};
