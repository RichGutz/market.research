# HANDOFF — Tienda.APPLE.PS5 Mini Web
**Última sesión:** 2026-02-21 22:55  
**Carpeta:** `C:\Users\rguti\Tienda.APPLE.PS5\`  
**Archivo principal:** `index.html` (todo en uno — HTML + CSS + JS, sin build tools)

---

## Estado Final de Esta Sesión ✅

| Producto | Silueta | Logo | Animación |
|---|---|---|---|
| iPhone 16 Pro | ✅ Portrait, pantalla azul, cámara, Dynamic Island | ✅ Apple SVG blanco semitransparente | ✅ Ensambla, flota, mouse 3D |
| MacBook Pro | ✅ Landscape, pantalla negra, bisagra, teclado, trackpad | ✅ Apple SVG gris sobre pantalla | ✅ Ídem |
| PlayStation 5 | ✅ Portrait, placas blancas, columna negra, LEDs azules | ✅ Botones △ □ ○ × PlayStation + texto | ✅ Ídem + LED pulse |

Loop completo: iPhone → MacBook → PS5 → iPhone ♻️

---

## Stack Técnico

- **Un solo `index.html`** — abre con doble clic en Windows
- **GSAP 3.12.5** CDN gratuito (sin plugins de pago)
- **SVG puro** + polígonos dinámicos
- **Google Fonts** — Inter

---

## Cómo Probar

1. Doble clic en `index.html`
2. Espera ~2s para el ensamblaje del iPhone
3. **Clic en el SVG** → siguiente producto | Flechas ← → | Botones ▲▼ | Dots de navegación
4. Mueve el mouse para el efecto 3D de paralaje

---

## Arquitectura Clave

### Array `PRODUCTS[]`
```js
{
  name, label, price,    // texto UI
  accent,                // CSS var(--accent) — color de marca
  glow, shadow,          // radial BG y drop-shadow del SVG
  vb: '0 0 W H',         // viewBox propio (iPhone/PS5=400×540, MacBook=500×380)
  ww, wh,                // dimensiones ideales del wrapper
  shards: [              // exactamente 12 arrays
    ['points', '#fill', opacity],
  ]
}
```

### Array `LOGO_HTML[]`
Cada entrada es HTML que se inyecta en `#logo-overlay` (div absoluto sobre el SVG).  
- Fade-in después del ensamblaje — Fade-out antes de la dispersión.

### Funciones principales
| Función | Rol |
|---|---|
| `scatter()` | Coloca piezas en aro alrededor, escala 0, opacidad 0 |
| `buildIn()` | GSAP timeline: expo.out stagger. Al completar → logo fade-in |
| `scatterOut()` | GSAP timeline: power3.in. Al inicio → logo fade-out |
| `goTo(ni)` | Orquesta: scatterOut → swap → scatter → setWrapper → buildIn |
| `setWrapper(pi)` | Ajusta tamaño del wrapper y viewBox al aspect ratio del producto |

---

## ✅ DOs

| # | Regla |
|---|---|
| 1 | `transform-box: fill-box; transform-origin: 50% 50%` en CSS para polígonos — rota sobre su propio centro |
| 2 | ViewBox diferente por producto — MacBook necesita landscape (`500×380`) |
| 3 | Wrapper dinámico calculado con `ww/wh` ratio + límites de viewport |
| 4 | Exactamente 12 polígonos en el array y en el DOM — ni uno más |
| 5 | Logos como overlay HTML independiente (no como polígono 13) |
| 6 | Logo fade-out ANTES de scatter, fade-in DESPUÉS de buildIn |
| 7 | Stagger con `i * 0.055` para el efecto "Species in Pieces" |
| 8 | Distribuir piezas en aro (ángulo = `(i/NS)*2π`) para scatter ordenado |

## ❌ DON'Ts

| # | Error a evitar |
|---|---|
| 1 | Un solo viewBox para todos los productos → MacBook aplastado |
| 2 | `transformOrigin` con px absolutos del viewBox → falla al cambiar producto |
| 3 | Más de 12 ítems en `shards[]` → el polígono 12 queda "fantasma" del anterior |
| 4 | Colores demasiado similares entre piezas adyacentes → silueta invisible |
| 5 | Diseñar coordenadas SVG sin verificar con captura de navegador |
| 6 | Hacer fade-out del logo junto con la dispersión (se ve floating en el aire) |

---

## Próximos Pasos Sugeridos

- [ ] Botón **"Comprar ahora"** con fade-in después del ensamblaje
- [ ] Página de detalle por producto al hacer clic en "Comprar"
- [ ] Logo Apple en la apertura de la tapa (animación de lid opening)
- [ ] Responsive para móvil (`< 480px`)
- [ ] **Prompt 2**: función `transitionToMacbook()` formal con MorphSVG si se adquiere licencia
- [ ] Agregar iPad o AirPods como 4to producto

---

## Brief Original

`PROMPT.txt` en la misma carpeta — 3 MASTER PROMPTs:
- **Prompt 1** — Hero iPhone ← **BASE COMPLETADA**
- **Prompt 2** — Morphing iPhone → MacBook ← pendiente
- **Prompt 3** — Morphing MacBook → PS5 + Loop ← pendiente (loop sí funciona)

---

## Reglas del Usuario (para el siguiente agente)

1. No ejecutar servidores de desarrollo — el HTML se abre directamente
2. No hacer `git commit/push` sin autorización explícita
3. Leer el archivo completo antes de modificar, luego reescribir completo
4. Un cambio a la vez — pedir al usuario que pruebe antes del siguiente
5. No refactorizar algo que funciona sin autorización
6. Comunicarse en **español**
7. Pedir autorización antes de cualquier modificación

---

*Sesión Antigravity — 2026-02-21*
