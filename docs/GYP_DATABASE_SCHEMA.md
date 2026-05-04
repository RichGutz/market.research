# Estructura de Base de Datos — Módulo GyP

**Fecha de diseño:** 2026-05-03  
**Plataforma:** Supabase (PostgreSQL)  
**Script de creación:** `backend/gyp_schema.sql`

---

## Resumen del Modelo

El módulo GyP utiliza **3 tablas relacionadas** para persistir todos los datos de la UI.  
La **`fecha_lote`** (tipo `DATE`) es el identificador único de negocio que conecta las 3 tablas.

```
gyp_lotes (1) ──────< gyp_productos (N)
gyp_lotes (1) ──────── gyp_costos_indirectos (1)
```

---

## Tabla 1: `gyp_lotes`

Cabecera del lote. Una fila = un viaje de compra.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID (PK) | ID técnico auto-generado |
| `fecha_lote` | DATE (UNIQUE) | **Llave de negocio del lote** |
| `status` | VARCHAR(20) | `EN PROCESO` o `CERRADO` |
| `total_costos_indirectos_usd` | NUMERIC(10,2) | Suma total costos |
| `total_compra_usd` | NUMERIC(10,2) | Total comprado en USA |
| `total_venta_usd` | NUMERIC(10,2) | Total vendido en USD |
| `total_ganancia_neta_usd` | NUMERIC(10,2) | Ganancia final del lote |
| `created_at` | TIMESTAMPTZ | Fecha de creación |
| `updated_at` | TIMESTAMPTZ | Última modificación (auto) |

---

## Tabla 2: `gyp_productos`

Detalle línea a línea de los productos del lote.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID (PK) | ID técnico auto-generado |
| `lote_fecha` | DATE (FK) | → `gyp_lotes.fecha_lote` |
| `qty` | INT | Cantidad de unidades |
| `modelo` | VARCHAR(255) | Nombre del modelo (del dropdown) |
| `venta_usd` | NUMERIC(10,2) | Precio de venta en USD |
| `compra_usd` | NUMERIC(10,2) | Precio de compra en USA |
| `prorrateo_usd` | NUMERIC(10,2) | Costo indirecto prorrateado |
| `ganancia_neta_usd` | NUMERIC(10,2) | Ganancia neta de esta línea |
| `created_at` | TIMESTAMPTZ | Fecha de creación |

---

## Tabla 3: `gyp_costos_indirectos`

Costos del viaje vinculados al lote. Relación 1 a 1 con `gyp_lotes`.

| Columna | Tipo | Descripción |
|---|---|---|
| `lote_fecha` | DATE (PK + FK) | → `gyp_lotes.fecha_lote` |
| `courier_usd` | NUMERIC(10,2) | Costo de courier |
| `courier_nota` | TEXT | Comentario libre |
| `transfer_usd` | NUMERIC(10,2) | Transferencia de dinero |
| `transfer_nota` | TEXT | Comentario libre |
| `airfare_usd` | NUMERIC(10,2) | Pasajes (Airfare) |
| `airfare_nota` | TEXT | Comentario libre |
| `food_usd` | NUMERIC(10,2) | Alimentación |
| `food_nota` | TEXT | Comentario libre |
| `transport_usd` | NUMERIC(10,2) | Transporte local |
| `transport_nota` | TEXT | Comentario libre |
| `ads_usd` | NUMERIC(10,2) | Publicidad |
| `ads_nota` | TEXT | Comentario libre |
| `other_usd` | NUMERIC(10,2) | Otros costos |
| `other_nota` | TEXT | Comentario libre |
| `updated_at` | TIMESTAMPTZ | Última modificación (auto) |

---

## Notas Técnicas

- **ON DELETE CASCADE:** Si se elimina un `gyp_lotes`, se eliminan automáticamente sus productos y costos.
- **Triggers `updated_at`:** Se actualizan solos al hacer cualquier `UPDATE`.
- **RLS (Row Level Security):** Activado en las 3 tablas. Solo usuarios autenticados de Supabase pueden operar.
- **Índices:** Creados sobre `fecha_lote` en `gyp_lotes` y `gyp_productos` para búsquedas rápidas.
