# Plan de Desarrollo: Market Research Web App - Tienda Apple PlayStation 5

Este documento sirve como guía de continuidad para el desarrollo de la aplicación web de investigación de mercado.

## Contexto del Proyecto
El objetivo es una Web App rápida y responsive que permita comparar precios de artículos electrónicos (iPhones, iWatch, iPads, Macbooks, PlayStation) entre el mercado de EE.UU. y el mercado de Perú para calcular ganancias brutas en tiempo real durante negociaciones.

## Arquitectura y Tecnologías
- **Repositorio**: [https://github.com/RichGutz/Tienda.Apple.PS5.git](https://github.com/RichGutz/Tienda.Apple.PS5.git)
- **Backend**: Python con `FastAPI`.
- **Base de Datos**: `Supabase` (Integrada con la base de datos existente de `Scraper.Neoauto`).
- **Scraping**: Basado en la lógica avanzada de `Scraper.Neoauto` (Selenium/Playwright) para extraer precios de Mercado Libre Perú, Hiraoka, Saga Falabella, Ripley, Oechsle e iShop.
- **Frontend**: Web App optimizada para móviles (HTML/JS/Vanilla CSS).
- **Despliegue**: `Hostinger` (Subdominio), referido al flujo del proyecto `Petral.MARK`.

## Estado Actual
- [x] Transcripción de requerimientos desde audio.
- [x] Plan de implementación aprobado.
- [x] Estructura de carpetas inicial creada (`backend/`, `frontend/`).
- [x] Identificación de credenciales de Supabase en `Scraper.Neoauto`.

## Próximos Pasos (Para el siguiente GEMINI)
1. **Modelado de Datos**: Crear las tablas en Supabase para almacenar modelos de dispositivos y sus precios históricos en Perú.
2. **Motor de Scraping**: Desarrollar `backend/scraper_peru.py` tomando como referencia los extractores de Neoauto. Debe ser flexible para manejar cambios frecuentes en el DOM.
3. **Desarrollo de API**: Implementar los endpoints en `backend/api_market.py` para consultar precios y realizar el cálculo: `Ganancia Bruta = Precio Perú - Precio USA`.
4. **Interfaz de Usuario**: Desarrollar el MVP del frontend en `frontend/index.html` enfocado en UX móvil "one-tap".
5. **Integración**: Conectar el frontend con la API y validar el flujo completo.
6. **Efectos Visuales (Morphing)**: Mejorar la UI interactiva de `index.html` implementando un *morphing fluido real* entre dispositivos, usando interpolación de polígonos (attr points) y easings tecnológicos (como `expo.inOut`), en lugar de fade-outs engañosos, según los lineamientos del Master Prompt.
7. **Transición a Online Store (SPA)**: Ampliar el frontend interactivo hacia una tienda real. 
   - Modificar la base de datos (`Supabase` / `SQLite`) y `scraper_peru.py` para capturar la URL de la imagen principal (`image_url`) de cada producto.
   - Actualizar `api_market.py` para devolver estas imágenes.
   - En `index.html`, crear una animación estilo *Species in Pieces* donde el clic transversal rompa la figura central y revele (`fade in`) una nueva sección interconectada con el catálogo dinámico de la categoría activa, incluyendo sus fotos scrapeadas.

## Estructura de Carpetas
- `/backend`: Scripts de scraping y servidor API.
- `/frontend`: Código fuente de la interfaz web.
- `/audio_transcript`: Archivos originales de requerimientos y transcripciones.

---
> [!NOTE]
> Recuerda seguir las "User Rules" globales, especialmente en lo referente a no refactorizar código estable y documentar cada acción en `gemini_work_log.txt`.
