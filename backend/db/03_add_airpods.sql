-- 1. Crear la Tabla Identica a las Demás
CREATE TABLE IF NOT EXISTS public.prices_airpods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_item_id UUID REFERENCES public.apple_ps5_catalog(id) ON DELETE CASCADE,
    store VARCHAR(50) NOT NULL,
    scraped_title VARCHAR(255) NOT NULL,
    price_pen NUMERIC(10, 2) NOT NULL,
    url TEXT NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    image_url TEXT
);

-- 2. Actualizar la Vista Unificada para el Dashboard (Total Margins)
CREATE OR REPLACE VIEW public.vw_apple_ps5_margins AS
WITH all_prices AS (
    SELECT * FROM public.prices_iphone
    UNION ALL SELECT * FROM public.prices_iwatch
    UNION ALL SELECT * FROM public.prices_ipad
    UNION ALL SELECT * FROM public.prices_macbook
    UNION ALL SELECT * FROM public.prices_playstation
    UNION ALL SELECT * FROM public.prices_samsung
    UNION ALL SELECT * FROM public.prices_airpods
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

-- 3. Actualizar la Vista Unificada de Precios Crudos (Sources)
CREATE OR REPLACE VIEW public.vw_apple_ps5_market_prices AS
SELECT * FROM public.prices_iphone
UNION ALL SELECT * FROM public.prices_iwatch
UNION ALL SELECT * FROM public.prices_ipad
UNION ALL SELECT * FROM public.prices_macbook
UNION ALL SELECT * FROM public.prices_playstation
UNION ALL SELECT * FROM public.prices_samsung
UNION ALL SELECT * FROM public.prices_airpods;
