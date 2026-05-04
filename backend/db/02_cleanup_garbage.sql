-- SCRIPT DE LIMPIEZA DE BASURA EN SUPABASE
-- Aplica los mismos filtros de validación estricta que el Scraper para purgar ejecuciones anteriores.

-- 1. Eliminar por Palabras Prohibidas (Accesorios)
-- El operador ~* es para regex case-insensitive en PostgreSQL
DELETE FROM public.prices_iphone WHERE scraped_title ~* 'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|organizador|sticker|decal|skin|soporte|stand|audifonos';
DELETE FROM public.prices_iwatch WHERE scraped_title ~* 'correa|strap|funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|organizador|sticker|decal';
DELETE FROM public.prices_ipad WHERE scraped_title ~* 'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|keyboard|teclado|pencil|lapiz|soporte';
DELETE FROM public.prices_macbook WHERE scraped_title ~* 'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|bolso|maleta|estuche|adaptador|hub|mouse';
DELETE FROM public.prices_playstation WHERE scraped_title ~* 'funda|case|control|mando|joystick|sticker|skin|soporte|stand|audifonos|cable|cargador';
DELETE FROM public.prices_samsung WHERE scraped_title ~* 'funda|case|correa|strap|mica|protector|vidrio|templado|repuesto|cargador|cable';

-- 2. Eliminar por Pisos de Precio (Price Floor)
-- Evita que accesorios baratos que no fueron capturados por el regex permanezcan en la tabla
DELETE FROM public.prices_iphone WHERE price_pen < 1500;
DELETE FROM public.prices_macbook WHERE price_pen < 2500;
DELETE FROM public.prices_ipad WHERE price_pen < 1200;
DELETE FROM public.prices_iwatch WHERE price_pen < 800;
DELETE FROM public.prices_playstation WHERE price_pen < 1400;
DELETE FROM public.prices_samsung WHERE price_pen < 1500;

-- 3. Eliminar resultados que no contienen la marca principal (Ruido genérico)
DELETE FROM public.prices_iphone WHERE NOT (scraped_title ~* 'iPhone');
DELETE FROM public.prices_macbook WHERE NOT (scraped_title ~* 'Macbook|Mac Book|Air|Pro');
DELETE FROM public.prices_iwatch WHERE NOT (scraped_title ~* 'Watch|iWatch|Ultra|Series');
DELETE FROM public.prices_ipad WHERE NOT (scraped_title ~* 'iPad');
DELETE FROM public.prices_playstation WHERE NOT (scraped_title ~* 'PlayStation|PS5');
DELETE FROM public.prices_samsung WHERE NOT (scraped_title ~* 'Samsung|Galaxy|S26');

-- LOG de limpieza
SELECT 'Limpieza completada. Datos basura eliminados de todas las tablas de precios.' as status;
