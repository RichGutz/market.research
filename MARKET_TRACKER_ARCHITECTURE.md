# 🧠 Arquitectura Core: Market Tracker (research.geeksoft.tech)

Esta documentación técnica detalla el funcionamiento exacto y el ciclo de vida de los datos de la herramienta mayorista "Market Search" (Apple & PS5 Tracker) al 100%.

Este ecosistema vive en el subdirectorio `/Market.Research` y está compuesto por 4 capas principales: Scraper, Base de Datos, Servidor API y Frontend Web. Todo está orquestado para actualizarse automáticamente mediante un Cron Job en el VPS (Hostinger).

---

## 1. El Motor de Extracción (Web Scraper)
**Archivo Principal:** `backend/scraper_peru.py` (y versiones futuras `v2`)

El Scraper es un robot programado en **Python Asíncrono** usando `Playwright`. Su propósito es barrer constantemente 5 de las tiendas tecnológicas más grandes del Perú: **Mercado Libre**, **iShop**, **Hiraoka**, **Ripley** y **Novox**.

### Flujo de Ejecución del Scraper:
1. **Lanzamiento (Trigger)**: Se activa ejecutando la función `run_market_scrapers()`. Automáticamente busca 6 keywords maestros, por ejemplo: `"iPhone"`, `"Apple Watch"`, `"MacBook"`, `"Apple AirPods"`, etc.
2. **Scraping Concurrente**: Gracias a `asyncio.gather()`, dispara la búsqueda en las 5 tiendas al mismo tiempo en navegadores invisibles (Headless), simulando clics, scrolls humanos y evadiendo pop-ups.
3. **Filtro Anti-Basura**: Por cada producto que encuentra ("iPhone 15 Pro Max"), lo pasa por una estricta función llamada `is_valid_result()`.
   - Limpia de palabras prohibidas: `"case"`, `"funda"`, `"correa"`, `"mica"`.
   - Si busca "Macbook", rechaza cualquier cosa que no diga "Macbook" o "Apple" en el título.
4. **Inserción Transaccional**: El scraper abre una conexión POST hacia la base de datos de **Supabase**. Dependiendo del nombre que buscó, inyecta los resultados a la tabla que le pertenece (`prices_iphone`, `prices_airpods`, etc.).

---

## 2. La Base de Datos (Supabase PostgreSQL)
### El Catálogo Semilla
**Archivo:** `backend/populate_db.py`
Para que la app funcione, existe una tabla madre llamada `apple_ps5_catalog`. Este archivo contiene todos los modelos base autorizados (ej. "AirPods 4 ANC") y sus respectivos precios americanos (`target_usa_price`) que sirven de referencia para calcular los márgenes.

### Las Tablas de Categoría
Las extracciones que el robot hace cada madrugada se guardan en las siguientes 7 tablas específicas:
- `prices_iphone`, `prices_iwatch`, `prices_ipad`, `prices_macbook`, `prices_playstation`, `prices_samsung`, `prices_airpods`.

*(Nota: Estas tablas guardan `store`, `scraped_title`, `price_pen`, `url`, `scraped_at` y el atributo moderno `image_url`)*.

### Las "Super Vistas" SQL Mágicas
**Archivo Base:** `backend/db/01_init_tables.sql` y `03_add_airpods.sql`
Para que el Frontend o la API no tengan que consultar 7 tablas distintas, dentro de Supabase viven dos Vistas (Views) que empaquetan todo automáticamente gracias a comandos `UNION ALL`:

1. **`vw_apple_ps5_market_prices`**: Devuelve una lista gigante con cada precio extraído por el robot en vivo. 
   - **Fix Crítico**: Cada `SELECT` dentro de la vista inyecta su propio nombre *(ej. `SELECT 'AirPods' as category, * FROM prices_airpods`)*. Esta columna "ficticia" es importantísima porque es la que permite que el Frontend sepa en qué pestaña dibujarlo.
2. **`vw_apple_ps5_margins`**: Une los precios mínimos (`MIN`) y promedio (`AVG`) contra el precio americano de la tabla maestro `apple_ps5_catalog`. (*Actualmente esperando integración HTML mediante template de tarjetas*).

---

## 3. El Servidor de Exposición (FastAPI)
**Archivo Principal:** `backend/api_market_v2.py`
Este pequeño servidor está constantemente encendido en el VPS gracias al demonio de Linux `systemd`. 

1. **Endpoint `/market-prices`**: Accede y jala toda la data empaquetada de la supervista `vw_apple_ps5_market_prices`. Lo devuelve tal cual como un JSON gigante al mundo exterior.
2. Nginx (tu servidor web intermedio) dirige en privado todas las solicitudes web a este puerto interno (8000).

---

## 4. La Cara del Robot (Frontend Web)
**Archivos:** `frontend/index.html` y `frontend/app.js`
Es una aplicación puramente estática (`Vanilla JS`) montada probablemente sobre Hostinger, que se carga en milisegundos en tu navegador:

1. **Primera Carga `app.init()`**: Al cargar la web, jala la última variable de TC (Tipo de Cambio) que dejaste guardada en tu navegador (`localStorage`). Esto permite que el cálculo de `Soles a USD$` sea exacto a lo que te interesa.
2. **Consumo de API**: Llama al servidor FastAPI a la ruta `/market-prices` para pedir todos los registros extraídos por el scraper en su historia.
3. **El "Filtro Destructor de Duplicados" (Deduplicación)**: 
   - Como el robot corre todos los días amontonando millones de precios en Supabase...
   - El código en `app.js` captura todo el JSON gigante e itera producto por producto.
   - Si detecta que hay 2 productos con la misma `url` (La misma tienda vendiendo el mismo producto), el código desecha el registro antiguo y **solo retiene el que tiene la fecha `scraped_at` más reciente**.
   - Con esto tu pantalla nunca se llena de basura.
4. **Renderizado (`app.render()`)**: Tras limpiar la basura, filtra el JSON usando la variable `category` que inyectó la vista SQL. Si estás en la pestaña PS5, filtra `p.category === 'PlayStation'`. Ordena por precio y los dibuja en la pantalla.

---

## 5. Arquitectura del Piloto Automático (Cron Job)
**Archivos:** `DOC_HOSTINGER_SETUP.md` y `backend/run_scraper.sh`
Para mantener un entorno local (en tu compu) inmaculado, el escrapeo exhaustivo se mudó completamente a la Nube (VPS de Hostinger).

- En Hostinger vive una regla del sistema: `33 3 * * *`.
- Todos los días a las 3:33 AM (Hora del servidor Hostinger), el sistema despierta al archivo `run_scraper.sh`.
- Este archivo entra a la carpeta del backend, **Enciende un Entorno Virtual Seguro de Python** (para evitar choques de compatibilidad de los Cron base), ejecuta `scraper_peru.py` y guarda posibles fallos en el documento de solo lectura `cron_scraper.log`.
- Se duerme hasta las 3:33 AM del día siguiente.
