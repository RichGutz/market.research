// Configuración Base
// Configuración Base - Detección automática de entorno
const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:')
    ? "http://127.0.0.1:8000"
    : "/api";

const app = {
    state: {
        marketPrices: [],
        currentCategory: 'iPhone',
        sortOrder: 'desc',
        tc: 3.35
    },

    init() {
        // Cargar TC guardado
        const savedTC = localStorage.getItem('apple_ps5_tc');
        if (savedTC) {
            this.state.tc = parseFloat(savedTC);
        }
        const tcInput = document.getElementById('tipo-cambio');
        if (tcInput) tcInput.value = this.state.tc;

        this.refreshData();
    },

    async refreshData() {
        this.showLoading(true);
        try {
            console.log("Cargando precios de mercado desde:", API_URL);
            const res = await fetch(`${API_URL}/market-prices`);
            if (!res.ok) throw new Error("Error en /market-prices");

            const allPrices = await res.json();
            
            // DEDUPLICACIÓN: Asegurar que solo se muestran los datos más recientes por URL de tienda
            // Esto evita que precios pasados del mismo producto se amontonen en la tabla
            const latestPricesMap = new Map();
            allPrices.forEach(p => {
                if (!latestPricesMap.has(p.url)) {
                    latestPricesMap.set(p.url, p);
                } else {
                    const existing = latestPricesMap.get(p.url);
                    // Comparar timestamps para quedarse con el más nuevo
                    if (new Date(p.scraped_at) > new Date(existing.scraped_at)) {
                        latestPricesMap.set(p.url, p);
                    }
                }
            });
            this.state.marketPrices = Array.from(latestPricesMap.values());
            
            this.render();
        } catch (error) {
            console.error("Error al cargar datos:", error);
            document.getElementById('market-body').innerHTML = `
                <tr><td colspan="4" style="text-align:center; color:var(--status-avoid)">⚠️ Error al conectar con el servidor.</td></tr>
            `;
        } finally {
            this.showLoading(false);
        }
    },

    filterCategory(category) {
        this.state.currentCategory = category;
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });
        this.render();
    },

    updateTC() {
        const input = document.getElementById('tipo-cambio');
        if (!input) return;
        const val = parseFloat(input.value);
        if (!isNaN(val) && val > 0) {
            this.state.tc = val;
            localStorage.setItem('apple_ps5_tc', val);
            this.render();
        }
    },

    updateSort() {
        this.state.sortOrder = document.getElementById('sort-order').value;
        this.render();
    },

    render() {
        const body = document.getElementById('market-body');
        const emptyState = document.getElementById('empty-state');
        const tableCard = document.querySelector('.table-card');

        body.innerHTML = '';

        // 1. Filtrar por categoría
        // Mapeo flexible para PS5/PlayStation
        const targetCat = this.state.currentCategory;
        let filtered = this.state.marketPrices.filter(p => {
            if (targetCat === 'PlayStation') return p.category === 'PlayStation' || p.category === 'PS5';
            return p.category === targetCat;
        });

        // 2. Ordenar por precio
        filtered.sort((a, b) => {
            return this.state.sortOrder === 'desc'
                ? b.price_pen - a.price_pen
                : a.price_pen - b.price_pen;
        });

        if (filtered.length === 0) {
            tableCard.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        tableCard.style.display = 'block';
        emptyState.style.display = 'none';

        filtered.forEach(item => {
            const usdPrice = item.price_pen / this.state.tc;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="col-brief">
                    <div class="row-brief">${item.scraped_title}</div>
                </td>
                <td class="col-store">
                    <div class="row-store">${item.store}</div>
                </td>
                <td class="col-price">
                    <div class="row-price" style="font-weight:600; color:var(--text-light)">S/ ${item.price_pen.toLocaleString('es-PE', { minimumFractionDigits: 2 })}</div>
                </td>
                <td class="col-price-usd">
                    <div class="row-price-usd" style="font-weight:700; color:var(--accent)">$ ${usdPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
                </td>
                <td class="col-link">
                    <a href="${item.url}" target="_blank" class="btn-view">Ver Oferta</a>
                </td>
            `;
            body.appendChild(tr);
        });
    },

    showLoading(show) {
        const loadingEl = document.getElementById('loading-state');
        if (loadingEl) loadingEl.style.display = show ? 'flex' : 'none';
    }
};

document.addEventListener('DOMContentLoaded', () => app.init());

