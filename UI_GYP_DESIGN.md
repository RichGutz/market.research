# Diseño UI - Módulo GyP (Ganancias y Pérdidas)
*Draft v1.0*

## 1. Organización del Worktree Propuesta (Market.Research)
Para integrar este módulo ordenadamente en el proyecto actual, sugiero la siguiente estructura para los nuevos archivos:

```text
C:\Users\rguti\Market.Research\
├── frontend\
│   ├── login.html       <-- Pantalla de autenticación simple
│   ├── login.css        <-- Estilos del login
│   ├── login.js         <-- Lógica para validar acceso
│   ├── gyp.html         <-- Nueva vista UI del GyP (protegida)
│   ├── gyp.css          <-- Estilos específicos del GyP
│   └── gyp.js           <-- Lógica dinámica (generar filas, sumar USD)
├── backend\
│   ├── api_auth.py      <-- Endpoint simple para validar credenciales
│   ├── api_gyp.py       <-- Nuevo endpoint para procesar y guardar los batches
│   └── ...
└── docs\
    ├── UI_GYP_DESIGN.md <-- (Este documento)
    └── UI_GYP_DESIGN.pdf
```

---

## 2. Mockup de Interfaz (Textual)

### [ PANTALLA 1: LOGIN SIMPLE ]
*(Inspirado en el CRM de NeoAuto. Restringe el acceso al módulo)*
- **Logo/Título:** `[ Market Tracker - Acceso Restringido ]`
- **Usuario:** `[ Input Texto ]`
- **Contraseña:** `[ Input Password ]`
- `[ Botón: INGRESAR ]`

---

### [ PANTALLA 2: MÓDULO GyP ]

#### [ SECCIÓN A: CABECERA Y CONFIGURACIÓN DEL BATCH ]
**[ Título: GyP - Nuevo Batch USA ]**
*(Nota: Toda la plataforma operará estrictamente en USD $)*

- **Producto Oficial:** `[ Dropdown List: iPhone 16 Pro, S26 Ultra, etc. ]` *(Lista de validación restrictiva)*
- **Fecha de Compra:** `[ Input Tipo Fecha: DD/MM/AAAA ]`
- **Cantidad de Productos Traídos:** `[ Input Numérico: Ej. 3 ]`
- `[ Botón: GENERAR FILAS ]`

---

### [ SECCIÓN B: DETALLE DE PRODUCTOS DEL BATCH ]
*(Esta tabla se auto-genera según el número ingresado arriba. Si puse "3", aparecen 3 filas)*

| Producto (Nombre Oficial) | 1. Precio de Venta ($) | 2. Precio de Compra USA ($) | 3. Costos Indirectos Asignados ($) | 4. Ganancia Neta ($) |
| :--- | :--- | :--- | :--- | :--- |
| `[ Selección bloqueada ]` | `[ Input: 0.00 ]` | `[ Input: 0.00 ]` | `[ Auto: Prorrateo por Costo USA ]` | `[ Auto: Col1 - Col2 - Col3 ]` |
| `[ Selección bloqueada ]` | `[ Input: 0.00 ]` | `[ Input: 0.00 ]` | `[ Auto: Prorrateo por Costo USA ]` | `[ Auto: Col1 - Col2 - Col3 ]` |
| `[ Selección bloqueada ]` | `[ Input: 0.00 ]` | `[ Input: 0.00 ]` | `[ Auto: Prorrateo por Costo USA ]` | `[ Auto: Col1 - Col2 - Col3 ]` |

*(La columna 3 se calcula automáticamente prorrateando los costos indirectos en base al Precio de Compra USA. La columna 4 es la resta automática).*

---

### [ SECCIÓN C: DESGLOSE DE COSTOS INDIRECTOS GLOBALES ]
*(Aquí se ingresan los gastos totales del viaje/batch)*

| Categoría de Costo | Monto (USD $) | Comentarios |
| :--- | :--- | :--- |
| **Tarifa Courier** | `[ Input: 0.00 ]` | `[ Input Texto: Ej. Fedex Miami... ]` |
| **Transferencia de dinero** | `[ Input: 0.00 ]` | `[ Input Texto: Comisiones bancarias... ]` |
| **Pasaje Aéreo** | `[ Input: 0.00 ]` | `[ Input Texto: Ej. Vuelo a MIA... ]` |
| **Alimentación** | `[ Input: 0.00 ]` | `[ Input Texto ]` |
| **Transporte** | `[ Input: 0.00 ]` | `[ Input Texto: Ej. Uber aeropuerto... ]` |
| **Publicidad** | `[ Input: 0.00 ]` | `[ Input Texto: Ads o promoción... ]` |
| **Otros** | `[ Input: 0.00 ]` | `[ Input Texto ]` |

**[ Total Costos Indirectos: $ 0.00 ]** *(Sumatoria automática)*

---

### [ SECCIÓN D: RESULTADO FINAL ]
- **Resumen Financiero:**
  - Ingresos Totales de Venta: `$ 0.00`
  - Costos Totales (Compra + Indirectos): `$ 0.00`
  - **Ganancia Neta del Batch:** `$ 0.00`

`[ Botón: GUARDAR BATCH GyP ]`
