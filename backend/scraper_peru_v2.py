import asyncio
import json
import logging
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright
from dotenv import load_dotenv
from supabase import create_client, Client
import urllib.parse

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# User Agents para Playwright
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

# Palabras prohibidas para evitar accesorios
FORBIDDEN_WORDS = [
    "funda", "case", "correa", "strap", "mica", "protector", "vidrio", 
    "templado", "repuesto", "cargador", "cable", "organizador", "sticker", 
    "decal", "skin", "soporte", "stand", "audifonos", "keyboard", "teclado",
    "mouse", "bolso", "maleta", "estuche", "adaptador", "hub"
]

class PeruMarketScraper:
    def __init__(self):
        self.results_dir = Path(__file__).parent / "results"
        self.results_dir.mkdir(exist_ok=True)
        load_dotenv()
        
        # Conexión a Supabase
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            logger.error("Credenciales de Supabase no encontradas en .env")
            self.supabase = None
        else:
            self.supabase = create_client(url, key)

    def is_valid_result(self, title: str, price: float, category: str, term: str) -> bool:
        """Valida que el resultado no sea un accesorio y tenga un precio lógico."""
        # Normalización de capacidades (ej: "128GB" -> "128 gb")
        def normalize(text):
            t = text.lower()
            # Normalizar almacenamiento
            t = re.sub(r'(\d+)\s*(gb|tb)', r'\1 \2', t) 
            # Normalizar chips (iShop trick: M4 suele ser M3, M3 suele ser M2)
            # No reemplazamos, solo permitimos que ambos sean válidos en el match
            return t

        title_norm = normalize(title)
        term_norm = normalize(term)
        
        # 1. Filtro de accesorios y palabras prohibidas
        for word in FORBIDDEN_WORDS:
            if word in title_norm:
                return False
                
        # 2. Validación Básica de Marca o Familia según la Categoría
        if category == "iPhone" and "iphone" not in title_norm and "apple" not in title_norm:
            return False
        if category == "Macbook" and "macbook" not in title_norm and "apple" not in title_norm:
            return False
        if category == "iPad" and "ipad" not in title_norm and "apple" not in title_norm:
            return False
        if category == "iWatch" and "watch" not in title_norm and "apple" not in title_norm:
            return False
        if category == "PlayStation" and "ps5" not in title_norm and "playstation" not in title_norm:
            return False
        if category == "Samsung" and "samsung" not in title_norm and "galaxy" not in title_norm:
            return False
            
        return True

    async def _handle_popups(self, page):
        """Intenta cerrar popups comunes de tiendas peruanas."""
        try:
            selectors = [
                "button[id*='cookie']",
                "button[class*='close']",
                ".dy-lb-close" 
            ]
            for selector in selectors:
                try:
                    elements = await page.locator(selector).all()
                    for el in elements:
                        if await el.is_visible():
                            await el.click(timeout=1000)
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"Error manejando popups: {e}")

    async def _human_scroll(self, page):
        """Simula comportamiento de scroll humano."""
        for _ in range(2):
            await page.mouse.wheel(0, 600)
            await asyncio.sleep(random.uniform(0.5, 1.0))

    def _get_table_by_category(self, category: str) -> str:
        """Determina la tabla de Supabase basándose en la categoría."""
        mapping = {
            "iPhone": "prices_iphone",
            "iWatch": "prices_iwatch",
            "iPad": "prices_ipad",
            "Macbook": "prices_macbook",
            "PlayStation": "prices_playstation",
            "Samsung": "prices_samsung"
        }
        return mapping.get(category, "apple_ps5_market_prices")

    async def save_to_supabase(self, catalog_item_id: str, category: str, results: list):
        """Guarda los resultados del scraping en la tabla correspondiente de Supabase."""
        if not self.supabase or not results:
            return

        table_name = self._get_table_by_category(category)
        logger.info(f"Guardando {len(results)} resultados en la tabla {table_name}")

        for res in results:
            try:
                data = {
                    "catalog_item_id": catalog_item_id,
                    "store": res["store"],
                    "scraped_title": res["title"],
                    "price_pen": res["price"],
                    "url": res["url"],
                    "image_url": res.get("image_url", "")
                }
                # Usamos insert ya que queremos un historial o podemos usar upsert si tuviéramos un ID único de producto-tienda
                self.supabase.table(table_name).insert(data).execute()
            except Exception as e:
                logger.error(f"Error guardando en Supabase ({table_name}): {e}")

    async def scrape_mercadolibre(self, term: str, category: str, max_items: int = 3):
        logger.info(f"[Mercado Libre] Buscando: {term}")
        search_url = f"https://listado.mercadolibre.com.pe/{term.replace(' ', '-')}"
        results = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=random.choice(USER_AGENTS), viewport={"width": 1366, "height": 768})
                page = await context.new_page()
                await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                await self._human_scroll(page)
                
                items = await page.locator("li.ui-search-layout__item").all()
                for item in items:
                    if len(results) >= max_items: break
                    try:
                        title = await item.locator("h2").first.inner_text(timeout=2000)
                        price_text = await item.locator(".andes-money-amount__fraction").last.inner_text(timeout=2000)
                        price = float(price_text.replace('.', '').replace(',', '.'))
                        link = await item.locator("a.ui-search-link").first.get_attribute("href", timeout=2000)
                        
                        img_el = item.locator("img.ui-search-result-image__image")
                        img_url = ""
                        if await img_el.count() > 0:
                            img_url = await img_el.first.get_attribute("data-src") or await img_el.first.get_attribute("src") or ""
                        
                        # VALIDACIÓN ESTRICTA
                        if self.is_valid_result(title, price, category, term):
                            results.append({"store": "Mercado Libre", "title": title.strip(), "price": price, "url": link, "image_url": img_url})
                    except: continue
                await browser.close()
            except Exception as e: logger.error(f"Error ML: {e}")
        return results

    async def scrape_ishop(self, term: str, category: str, max_items: int = 3):
        """Scraper para iShop Perú (Tiendas iShop)."""
        logger.info(f"[iShop] Buscando: {term}")
        
        # iShop Naming Trick: Los modelos del catálogo a veces requieren búsqueda con espacio
        search_term = term.replace('128GB', '128 GB').replace('256GB', '256 GB').replace('512GB', '512 GB').replace('1TB', '1 TB')
        
        # Inconsistencias de iShop: Si buscamos M3, ellos lo tienen como M4
        if "M3" in search_term and "Macbook" in category:
            search_term = search_term.replace("M3", "M4")
        if "M2" in search_term and "iPad" in category:
            search_term = search_term.replace("M2", "M3")
            
        search_url = f"https://pe.tiendasishop.com/search?q={search_term.replace(' ', '+')}"
        results = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(user_agent=random.choice(USER_AGENTS))
                await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                
                # Seleccionar los items de la grilla (Shopify)
                items = await page.locator(".grid__item").all()
                for item in items:
                    if len(results) >= max_items: break
                    try:
                        # iShop MacBook Fix: El título visible está truncado en el HTML.
                        # Usamos el input oculto que contiene el nombre completo.
                        title_el = item.locator("input.fbt-value.frequent-products-tittlr")
                        if await title_el.count():
                            title = await title_el.first.get_attribute("value")
                        else:
                            # Fallback original
                            title_el = item.locator(".full-unstyled-link-1")
                            if not await title_el.count():
                                title_el = item.locator(".full-unstyled-link")
                            title = await title_el.first.inner_text(timeout=2000)
                        
                        # Precio Sale (Oferta)
                        price_el = item.locator(".price-item--sale")
                        if not await price_el.count():
                            price_el = item.locator(".price-item--regular")
                        
                        price_text = await price_el.first.inner_text(timeout=2000)
                        # Limpiar precio: "S/ 3,499.00" -> 3499.0
                        price = float(re.sub(r'[^\d.]', '', price_text.replace(',', '')))
                        
                        link = await item.locator("a.full-unstyled-link").first.get_attribute("href")
                        if not link.startswith("http"):
                            link = "https://pe.tiendasishop.com" + link
                        
                        img_el = item.locator("img.motion-reduce")
                        if not await img_el.count():
                            img_el = item.locator("img")
                        img_url = ""
                        if await img_el.count() > 0:
                            img_url = await img_el.first.get_attribute("src") or ""
                            if img_url and img_url.startswith("//"):
                                img_url = "https:" + img_url
                        
                        if self.is_valid_result(title, price, category, term):
                            results.append({"store": "iShop", "title": title.strip(), "price": price, "url": link, "image_url": img_url})
                    except Exception as e:
                        logger.debug(f"Error parseando item iShop: {e}")
                        continue
                await browser.close()
            except Exception as e:
                logger.error(f"Error iShop: {e}")
        return results

    async def scrape_hiraoka(self, term: str, category: str, max_items: int = 3):
        logger.info(f"[Hiraoka] Buscando: {term}")
        search_url = f"https://hiraoka.com.pe/catalogsearch/result/?q={term.replace(' ', '+')}"
        results = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(user_agent=random.choice(USER_AGENTS))
                await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                await self._human_scroll(page)
                items = await page.locator(".product-item").all()
                for item in items:
                    if len(results) >= max_items: break
                    try:
                        title = await item.locator(".product-item-name").inner_text(timeout=2000)
                        price_text = await item.locator(".price").first.inner_text(timeout=2000)
                        price = float(price_text.replace('S/', '').replace(',', '').strip())
                        link = await item.locator("a.product-item-link").first.get_attribute("href", timeout=2000)
                        
                        img_el = item.locator("img.product-image-photo")
                        img_url = ""
                        if await img_el.count() > 0:
                            img_url = await img_el.first.get_attribute("src") or ""
                        
                        if self.is_valid_result(title, price, category, term):
                            results.append({"store": "Hiraoka", "title": title.strip(), "price": price, "url": link, "image_url": img_url})
                    except: continue
                await browser.close()
            except Exception as e: logger.error(f"Error Hiraoka: {e}")
        return results

    async def scrape_ripley(self, term: str, category: str, max_items: int = 3):
        logger.info(f"[Ripley] Buscando: {term}")
        search_url = f"https://simple.ripley.com.pe/search/{term.replace(' ', '%20')}"
        results = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(user_agent=random.choice(USER_AGENTS))
                await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                items = await page.locator("a.catalog-product-item").all()
                for item in items:
                    if len(results) >= max_items: break
                    try:
                        title = await item.locator(".catalog-product-details__name").inner_text(timeout=2000)
                        price_text = await item.locator(".catalog-prices__offer-price").first.inner_text(timeout=2000)
                        price = float(price_text.replace('S/', '').replace(',', '').strip())
                        link = await item.get_attribute("href")
                        if not link.startswith("http"): link = "https://simple.ripley.com.pe" + link
                        
                        img_el = item.locator("img[data-src]")
                        if not await img_el.count():
                            img_el = item.locator("img")
                        img_url = ""
                        if await img_el.count() > 0:
                            img_url = await img_el.first.get_attribute("data-src") or await img_el.first.get_attribute("src") or ""
                            if img_url and img_url.startswith("//"): img_url = "https:" + img_url
                        
                        if self.is_valid_result(title, price, category, term):
                            results.append({"store": "Ripley", "title": title.strip(), "price": price, "url": link, "image_url": img_url})
                    except: continue
                await browser.close()
            except Exception as e:
                logger.error(f"Error Ripley: {e}")
        return results

    async def scrape_novox(self, term: str, category: str, max_items: int = 10):
        logger.info(f"[Novox] Buscando: {term}")
        search_url = f"https://novoxperu.com/search?q={urllib.parse.quote(term)}"
        results = []
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(user_agent=random.choice(USER_AGENTS))
                await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_selector('.yv-product-card', timeout=15000)
                items = await page.locator('.yv-product-card').all()
                
                for item in items:
                    if len(results) >= max_items: break
                    try:
                        title_el = item.locator('.yv-product-title')
                        if await title_el.count() == 0: continue
                        title = await title_el.first.inner_text(timeout=2000)
                        
                        price_el = item.locator('.yv-product-price')
                        if await price_el.count() == 0: continue
                        price_text = await price_el.first.inner_text(timeout=2000)
                        
                        link_el = item.locator('a').first
                        link = await link_el.get_attribute('href')
                        if not link.startswith('http'): link = "https://novoxperu.com" + link
                        
                        img_el = item.locator("img")
                        img_url = ""
                        if await img_el.count() > 0:
                            img_url = await img_el.first.get_attribute("src") or ""
                            if img_url and img_url.startswith("//"): img_url = "https:" + img_url
                        
                        # Limpieza del precio crudo (e.g. "S/ 3,190.00 S/ 3,490.00Oferta") -> 3190.00
                        prices_found = re.findall(r'(\d+[\d,]*\.\d+)', price_text)
                        if not prices_found: continue
                        price_clean = float(prices_found[0].replace(',', ''))
                        
                        if self.is_valid_result(title, price_clean, category, term):
                            results.append({"store": "Novox", "title": title.strip(), "price": price_clean, "url": link, "image_url": img_url})
                    except Exception as e:
                        logger.debug(f"Error parseando item Novox: {e}")
                        continue
                await browser.close()
            except Exception as e:
                logger.error(f"Error Novox: {e}")
        return results

    async def run_catalog_scrapers(self, limit_items: int = None):
        """Itera sobre el catálogo de Supabase y ejecuta los scrapers."""
        if not self.supabase:
            logger.error("No se puede iniciar el proceso sin Supabase.")
            return

        logger.info("--- Iniciando Scraping basado en Catálogo ---")
        try:
            # Obtener el catálogo de Supabase
            res = self.supabase.table("apple_ps5_catalog").select("*").execute()
            catalog_items = res.data
            
            if not catalog_items:
                logger.warning("El catálogo está vacío. Ejecute populate_db.py primero.")
                return
                
            if limit_items:
                catalog_items = catalog_items[:limit_items]
                
            for item in catalog_items:
                item_id = item.get("id")
                category = item.get("category")
                model_name = item.get("model_name")
                
                logger.info(f">>> INICIANDO CATÁLOGO: {category} (Buscando: {model_name})")
                
                # Ejecutar scrapers en paralelo
                tasks = [
                    self.scrape_mercadolibre(model_name, category, max_items=5),
                    self.scrape_ripley(model_name, category, max_items=5),
                    self.scrape_hiraoka(model_name, category, max_items=5),
                    self.scrape_ishop(model_name, category, max_items=5),
                    self.scrape_novox(model_name, category, max_items=5)
                ]
                
                all_results = await asyncio.gather(*tasks)
                flat_results = [res for sublist in all_results for res in sublist]
                
                if flat_results:
                    await self.save_to_supabase(item_id, category, flat_results)
                    logger.info(f"Catálogo {model_name}: {len(flat_results)} resultados guardados.")
                
                await asyncio.sleep(2)
                
            logger.info("--- Scraping de Catálogo Finalizado con éxito ---")
        except Exception as e:
            logger.error(f"Error en el proceso de catálogo: {e}")

    async def run_market_scrapers(self):
        """Dispara las búsquedas generales por categoría (ej: "iPhone") barriendo el mercado sin restricciones del catálogo."""
        logger.info("--- Iniciando Sweep de Mercado Múltiple ---")
        
        categories = {
            "iPhone": "iPhone",
            "iWatch": "Apple Watch",
            "iPad": "iPad",
            "Macbook": "MacBook",
            "PlayStation": "PS5 Consola",
            "Samsung": "Samsung Galaxy S"
        }
        
        try:
            for category, term in categories.items():
                logger.info(f">>> INICIANDO CATEGORÍA: {category} (Buscando: {term})")
                
                # Ejecutar scrapers en paralelo
                tasks = [
                    self.scrape_mercadolibre(term, category, max_items=15),
                    self.scrape_ripley(term, category, max_items=10),
                    self.scrape_hiraoka(term, category),
                    self.scrape_ishop(term, category),
                    self.scrape_novox(term, category, max_items=10)
                ]
                
                all_results = await asyncio.gather(*tasks)
                flat_results = [res for sublist in all_results for res in sublist]
                
                if flat_results:
                    # Guardamos sin catalog_item_id (None) para reflejar que es sweep general
                    await self.save_to_supabase(None, category, flat_results)
                    logger.info(f"Categoría {category}: {len(flat_results)} resultados guardados.")
                
                await asyncio.sleep(2)

            logger.info("--- Scraping de Mercado Finalizado con éxito ---")
        except Exception as e:
            logger.error(f"Error en el proceso de mercado: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    scraper = PeruMarketScraper()
    asyncio.run(scraper.run_catalog_scrapers())

