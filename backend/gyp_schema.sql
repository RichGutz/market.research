-- ============================================================
-- MÓDULO GyP (Ganancias y Pérdidas) - Market Research
-- Script de Creación de Tablas en Supabase
-- Fecha: 2026-05-03
-- ============================================================

-- 1. TABLA PRINCIPAL DE LOTES
-- Cada fila representa un viaje/lote de compra.
-- La fecha_lote es la llave de negocio única (ID del lote).
-- ============================================================
CREATE TABLE IF NOT EXISTS gyp_lotes (
    id                          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fecha_lote                  DATE NOT NULL UNIQUE,
    status                      VARCHAR(20) NOT NULL DEFAULT 'EN PROCESO'
                                    CHECK (status IN ('EN PROCESO', 'CERRADO')),
    total_costos_indirectos_usd NUMERIC(10, 2) DEFAULT 0,
    total_compra_usd            NUMERIC(10, 2) DEFAULT 0,
    total_venta_usd             NUMERIC(10, 2) DEFAULT 0,
    total_ganancia_neta_usd     NUMERIC(10, 2) DEFAULT 0,
    created_at                  TIMESTAMPTZ DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para búsquedas rápidas por fecha
CREATE INDEX IF NOT EXISTS idx_gyp_lotes_fecha ON gyp_lotes (fecha_lote);


-- ============================================================
-- 2. TABLA DE PRODUCTOS DEL LOTE
-- Cada fila = un producto dentro de un lote.
-- Relación: Muchos productos -> Un lote (N:1)
-- ============================================================
CREATE TABLE IF NOT EXISTS gyp_productos (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    lote_fecha          DATE NOT NULL REFERENCES gyp_lotes(fecha_lote) ON DELETE CASCADE,
    qty                 INT NOT NULL DEFAULT 1,
    modelo              VARCHAR(255) NOT NULL,
    venta_usd           NUMERIC(10, 2) DEFAULT 0,
    compra_usd          NUMERIC(10, 2) DEFAULT 0,
    prorrateo_usd       NUMERIC(10, 2) DEFAULT 0,
    ganancia_neta_usd   NUMERIC(10, 2) DEFAULT 0,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para recuperar todos los productos de un lote rápidamente
CREATE INDEX IF NOT EXISTS idx_gyp_productos_lote ON gyp_productos (lote_fecha);


-- ============================================================
-- 3. TABLA DE COSTOS INDIRECTOS
-- Una sola fila por lote (relación 1:1 con gyp_lotes).
-- Cada costo tiene su campo numérico y su campo de nota/comentario.
-- ============================================================
CREATE TABLE IF NOT EXISTS gyp_costos_indirectos (
    lote_fecha          DATE NOT NULL PRIMARY KEY REFERENCES gyp_lotes(fecha_lote) ON DELETE CASCADE,

    courier_usd         NUMERIC(10, 2) DEFAULT 0,
    courier_nota        TEXT,

    transfer_usd        NUMERIC(10, 2) DEFAULT 0,
    transfer_nota       TEXT,

    airfare_usd         NUMERIC(10, 2) DEFAULT 0,
    airfare_nota        TEXT,

    food_usd            NUMERIC(10, 2) DEFAULT 0,
    food_nota           TEXT,

    transport_usd       NUMERIC(10, 2) DEFAULT 0,
    transport_nota      TEXT,

    ads_usd             NUMERIC(10, 2) DEFAULT 0,
    ads_nota            TEXT,

    other_usd           NUMERIC(10, 2) DEFAULT 0,
    other_nota          TEXT,

    updated_at          TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 4. FUNCIÓN AUTO-UPDATE para updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger en gyp_lotes
CREATE TRIGGER trg_gyp_lotes_updated_at
    BEFORE UPDATE ON gyp_lotes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger en gyp_costos_indirectos
CREATE TRIGGER trg_gyp_costos_updated_at
    BEFORE UPDATE ON gyp_costos_indirectos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================================
-- 5. ROW LEVEL SECURITY (RLS) - Recomendado en Supabase
-- ============================================================
ALTER TABLE gyp_lotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE gyp_productos ENABLE ROW LEVEL SECURITY;
ALTER TABLE gyp_costos_indirectos ENABLE ROW LEVEL SECURITY;

-- Política básica: solo usuarios autenticados pueden leer/escribir
CREATE POLICY "Acceso solo autenticados" ON gyp_lotes
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Acceso solo autenticados" ON gyp_productos
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Acceso solo autenticados" ON gyp_costos_indirectos
    FOR ALL USING (auth.role() = 'authenticated');
