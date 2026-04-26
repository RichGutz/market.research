# Design System: Cyber-Organic Geometry

## 1. Overview & Creative North Star
**The Creative North Star: "The Digital Synthetic"**

This design system is a manifestation of the "Cyber-Organic Geometry" concept. It rejects the "flatness" of modern SaaS templates in favor of a high-end, editorial tech experience inspired by the biological-meets-digital aesthetic of *Species in Pieces*. 

The system operates on the tension between **precision (Cyber)** and **fluidity (Organic)**. We achieve this through "Fragmented Layouts"—breaking the rigid 12-column grid with asymmetric overlaps, sharp geometric masks for imagery, and soft, glowing glass surfaces. The goal is to make the user feel they are navigating a living, breathing piece of advanced hardware.

---

## 2. Colors
Our palette is rooted in absolute darkness to allow our "Cyber-Organic" accents to vibrate with intensity.

### The Palette
- **Background & Surface:** We use `#000000` (Surface-Container-Lowest) and `#0e0e0e` (Surface) as our foundation. These are not just "dark mode" colors; they are the void in which the interface floats.
- **Neon Accents:** 
    - **Primary (`#ff89ab`):** Neon Pink for high-energy actions and "organic" highlights.
    - **Secondary (`#00e3fd`):** Electric Cyan for "cyber" technical data and secondary CTAs.
    - **Tertiary (`#aa8aff`):** Cobalt/Purple for deep depth and sophisticated layering.

### The "No-Line" Rule
**Explicit Instruction:** 1px solid borders are strictly prohibited for sectioning. 
Structure must be defined through:
1.  **Background Shifts:** Transition from `surface` (#0e0e0e) to `surface-container-low` (#131313).
2.  **Negative Space:** Utilizing the `spacing-16` (5.5rem) and `spacing-20` (7rem) tokens to create editorial breathing room.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of light-reactive materials. 
- **Base Layer:** `surface-container-lowest` (#000000).
- **Raised Content:** `surface-container` (#191919).
- **Active Modals/Glass:** Use `surface-bright` (#2c2c2c) at 40% opacity with a `20px` backdrop-blur to create the "Glassmorphism" effect.

### The "Glass & Gradient" Rule
Flat buttons are forbidden for primary actions. Use linear gradients (e.g., `primary` to `primary-container`) with a `0 0 15px` outer glow using the `primary_dim` token to simulate light emission.

---

## 3. Typography
The typography is designed to feel like a heads-up display (HUD) in a premium cockpit.

- **Display & Headlines (Space Grotesk):** This font provides the "Cyber" technical edge. Use `letter-spacing: 0.05em` for all headlines. `display-lg` (3.5rem) should be used sparingly for hero statements, often overlapped by "Organic" product imagery.
- **Body & Labels (Inter):** Inter provides the legibility required for e-commerce. 
- **The Signature "Technical" Look:** All `label-md` and `label-sm` elements must be `text-transform: uppercase` with `letter-spacing: 0.15em`. This mimics engineering schematics.

---

## 4. Elevation & Depth
In this system, depth is a product of light and transparency, not shadows.

- **The Layering Principle:** Stack `surface-container-low` on `surface-dim`. The contrast is subtle (less than 2% difference), creating a sophisticated, expensive-feeling transition.
- **Ambient Glows (The Shadow Replacement):** Instead of black drop shadows, use tinted glows. For a floating card, use a shadow color derived from `secondary` at 10% opacity with a 40px blur. This creates an "under-glow" effect.
- **The "Ghost Border" Fallback:** If a container requires definition against a busy background, use a 1px border with `outline-variant` (#484848) at **15% opacity**. It should be felt, not seen.
- **Geometric Sharps:** Combine `roundedness-none` for structural containers with `roundedness-xl` for "glass" pills to emphasize the Cyber-Organic hybridity.

---

## 5. Components

### Buttons
- **Primary:** Gradient (`primary` to `primary-container`), `roundedness-sm`, uppercase `label-md` text. Add a subtle `box-shadow` glow on hover.
- **Glass Action (Tertiary):** Background of `white` at 5% opacity, `backdrop-filter: blur(10px)`, and a "Ghost Border."

### Input Fields
- **Styling:** Underline-only or 2-sided "bracket" borders. Avoid 4-sided boxes.
- **States:** On focus, the underline should animate from the center using the `secondary` (Cyan) color.

### Cards (Product/Feature)
- **Rule:** Forbid divider lines.
- **Structure:** Use a `surface-container-high` background. Images should "bleed" out of the card boundaries or be masked into sharp, triangular geometries (the Species in Pieces influence).

### Micro-Interactions: Particle Hover
When hovering over high-end tech products, triggering a "dust" or "particle" effect (using the `secondary` color) behind the product image is encouraged to simulate a digital scan.

### Data Fragments (Additional Component)
Small, floating metadata blocks (e.g., "SPEC_01", "VER_2.4") using `label-sm` in `secondary_dim`. These should be placed near imagery to reinforce the technical, "Cyber" nature of the shop.

---

## 6. Do's and Don'ts

### Do
- **Do** use intentional asymmetry. Place a `display-md` headline slightly off-center to create visual tension.
- **Do** use "Organic" masks. Crop product photos into non-rectilinear shapes.
- **Do** prioritize legibility. Even in a neon-heavy system, ensure `body-md` text stays on `on-surface` (#ffffff).

### Don't
- **Don't** use standard 1px borders or solid grey dividers. It kills the premium "fluid" feel.
- **Don't** use generic icons. Use thin-stroke (1px) technical icons that match the `outline` token.
- **Don't** over-saturate. Use the pure black background (#000000) to provide "rest" for the eyes between the neon accents.
- **Don't** use "default" easing. All transitions should be `cubic-bezier(0.22, 1, 0.36, 1)` (Expo Out) for a snappier, high-tech response.