-- Script de Refactorización DB: Tablas por Categoría (Tienda Apple PS5)
-- Este script crea tablas específicas para cada tipo de producto.

-- 1. Tabla Maestra de Catálogo
CREATE TABLE IF NOT EXISTS public.apple_ps5_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) NOT NULL,
    model_name VARCHAR(150) NOT NULL UNIQUE,
    target_usa_price NUMERIC(10, 2) NOT NULL,
    reference_url TEXT,
    specs JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Tabla de Precios: iPhone
CREATE TABLE IF NOT EXISTS public.prices_iphone (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Tabla de Precios: iWatch
CREATE TABLE IF NOT EXISTS public.prices_iwatch (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Tabla de Precios: iPad
CREATE TABLE IF NOT EXISTS public.prices_ipad (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Tabla de Precios: Macbook
CREATE TABLE IF NOT EXISTS public.prices_macbook (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Tabla de Precios: PlayStation
CREATE TABLE IF NOT EXISTS public.prices_playstation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Tabla de Precios: Samsung [NEW]
CREATE TABLE IF NOT EXISTS public.prices_samsung (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. Vista Unificada para el Dashboard (Total Margins)
CREATE OR REPLACE VIEW public.vw_apple_ps5_margins AS
WITH all_prices AS (
    SELECT * FROM public.prices_iphone
    UNION ALL SELECT * FROM public.prices_iwatch
    UNION ALL SELECT * FROM public.prices_ipad
    UNION ALL SELECT * FROM public.prices_macbook
    UNION ALL SELECT * FROM public.prices_playstation
    UNION ALL SELECT * FROM public.prices_samsung
)
SELECT 
    c.id AS catalog_id,
    c.category,
    c.model_name,
    c.target_usa_price,
    ROUND(MIN(p.price_pen), 2) AS min_price_pen,
    ROUND(AVG(p.price_pen), 2) AS avg_price_pen,
    COUNT(p.id) as sample_size,
    MAX(p.scraped_at) as last_update
FROM 
    public.apple_ps5_catalog c
LEFT JOIN 
    all_prices p ON c.id = p.catalog_item_id
GROUP BY 
    c.id, c.category, c.model_name, c.target_usa_price;

-- 9. Vista Unificada de Precios Crudos (Sources)
CREATE OR REPLACE VIEW public.vw_apple_ps5_market_prices AS
SELECT * FROM public.prices_iphone
UNION ALL SELECT * FROM public.prices_iwatch
UNION ALL SELECT * FROM public.prices_ipad
UNION ALL SELECT * FROM public.prices_macbook
UNION ALL SELECT * FROM public.prices_playstation
UNION ALL SELECT * FROM public.prices_samsung;
