document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificación de Seguridad
    if (sessionStorage.getItem('gyp_authenticated') !== 'true') {
        window.location.href = 'login.html';
        return;
    }

    const userEmail = sessionStorage.getItem('gyp_user');
    if(userEmail) document.getElementById('displayUser').textContent = userEmail;

    document.getElementById('logoutBtn').addEventListener('click', () => {
        sessionStorage.clear();
        window.location.href = 'login.html';
    });

    // 2. Elementos del DOM
    const costInputs = document.querySelectorAll('.cost-input');
    const totalIndirectCostsEl = document.getElementById('totalIndirectCosts');
    const productsBody = document.getElementById('productsBody');
    const addProductBtn = document.getElementById('addProductBtn');
        const rowTemplate = document.getElementById('rowTemplate');
    
    // Configuración API
    const API_BASE_URL = window.location.origin.includes('localhost') ? 'http://localhost:8000' : '/api';

    
    // Totales de la tabla
    const totalPurchaseUSAEl = document.getElementById('totalPurchaseUSA');
    const totalSaleUSDEl = document.getElementById('totalSaleUSD');
    const totalProratedEl = document.getElementById('totalProrated');
    const totalNetProfitEl = document.getElementById('totalNetProfit');

    // Inicializar fecha
    document.getElementById('inputDate').valueAsDate = new Date();

    // 3. Lógica de Cálculos (Prorrateo y Ganancia)
    function calculateGyP() {
        // a. Sumar costos indirectos
        let totalIndirect = 0;
        costInputs.forEach(input => {
            totalIndirect += parseFloat(input.value) || 0;
        });
        totalIndirectCostsEl.textContent = `$ ${totalIndirect.toFixed(2)}`;

        // b. Calcular Costo Total de Compra USA para el prorrateo
        const rows = productsBody.querySelectorAll('.product-row');
        let totalPurchaseUSA = 0;
        
        rows.forEach(row => {
            const qty = parseFloat(row.querySelector('.row-qty').value) || 0;
            const buyUSA = parseFloat(row.querySelector('.row-buy-usa').value) || 0;
            totalPurchaseUSA += (qty * buyUSA);
        });

        let sumSaleUSD = 0;
        let sumProrated = 0;
        let sumProfit = 0;

        // c. Calcular cada fila
        rows.forEach(row => {
            const qty = parseFloat(row.querySelector('.row-qty').value) || 0;
            const buyUSA = parseFloat(row.querySelector('.row-buy-usa').value) || 0;
            const sellUSD = parseFloat(row.querySelector('.row-sell-usd').value) || 0;
            
            const rowTotalBuyUSA = qty * buyUSA;
            
            // Prorrateo: (Costo USA Fila / Costo USA Total Lote) * Total Costos Indirectos
            let prorated = 0;
            if (totalPurchaseUSA > 0) {
                prorated = (rowTotalBuyUSA / totalPurchaseUSA) * totalIndirect;
            }
            
            // Ganancia Neta USD: Venta USD Totales - Compra USA Totales - Prorrateo
            const rowTotalSellUSD = qty * sellUSD;
            const profit = rowTotalSellUSD - rowTotalBuyUSA - prorated;

            // Actualizar UI de la fila (Valores por UNIDAD o TOTAL fila? En este caso mostramos el Total de la Fila)
            row.querySelector('.row-prorated').textContent = `$ ${prorated.toFixed(2)}`;
            row.querySelector('.row-profit').textContent = `$ ${profit.toFixed(2)}`;
            
            // Colores para ganancia
            row.querySelector('.row-profit').style.color = profit >= 0 ? 'var(--highlight-green)' : 'var(--danger)';

            sumSaleUSD += rowTotalSellUSD;
            sumProrated += prorated;
            sumProfit += profit;
        });

        // d. Actualizar Totales Finales
        totalPurchaseUSAEl.textContent = `$ ${totalPurchaseUSA.toFixed(2)}`;
        totalSaleUSDEl.textContent = `$ ${sumSaleUSD.toFixed(2)}`;
        totalProratedEl.textContent = `$ ${sumProrated.toFixed(2)}`;
        totalNetProfitEl.textContent = `$ ${sumProfit.toFixed(2)}`;
        totalNetProfitEl.style.color = sumProfit >= 0 ? 'var(--highlight-green)' : 'var(--danger)';
    }

    // 4. Catálogo de Productos (Igual que en backend/populate_db.py)
    const catalogItems = [
        { category: "iPhone", name: "iPhone 17 128GB", usa: 799.00 },
        { category: "iPhone", name: "iPhone 17 Pro 256GB", usa: 1099.00 },
        { category: "iPhone", name: "iPhone 17 Pro Max 256GB", usa: 1199.00 },
        { category: "iPhone", name: "iPhone 16 128GB", usa: 799.00 },
        { category: "iPhone", name: "iPhone 16 Pro 256GB", usa: 1099.00 },
        { category: "iPhone", name: "iPhone 16 Pro Max 256GB", usa: 1199.00 },
        { category: "Macbook", name: "MacBook Air M5 13-inch 8GB 256GB", usa: 1099.00 },
        { category: "Macbook", name: "MacBook Air M5 15-inch 16GB 512GB", usa: 1499.00 },
        { category: "Macbook", name: "MacBook Pro 14-inch M5 Pro 18GB 512GB", usa: 1999.00 },
        { category: "Macbook", name: "MacBook Air M3 13-inch 8GB 256GB", usa: 1099.00 },
        { category: "Macbook", name: "MacBook Air M3 15-inch 16GB 512GB", usa: 1499.00 },
        { category: "Macbook", name: "MacBook Pro 14-inch M3 Pro 18GB 512GB", usa: 1999.00 },
        { category: "Macbook", name: "MacBook Pro 16-inch M3 Max 36GB 1TB", usa: 3499.00 },
        { category: "iWatch", name: "Apple Watch Series 11 42mm GPS", usa: 399.00 },
        { category: "iWatch", name: "Apple Watch Series 10 46mm GPS", usa: 429.00 },
        { category: "iWatch", name: "Apple Watch Series 9 45mm GPS", usa: 329.00 },
        { category: "iWatch", name: "Apple Watch Ultra 2", usa: 799.00 },
        { category: "iPad", name: "iPad Pro 13-inch M5 256GB", usa: 1299.00 },
        { category: "iPad", name: "iPad Pro 11-inch M4 256GB", usa: 999.00 },
        { category: "iPad", name: "iPad Pro 13-inch M4 256GB", usa: 1299.00 },
        { category: "iPad", name: "iPad Air 11-inch M2 128GB", usa: 599.00 },
        { category: "PlayStation", name: "PlayStation 5 Disc Edition", usa: 499.00 },
        { category: "PlayStation", name: "PlayStation 5 Slim Digital", usa: 399.00 },
        { category: "PlayStation", name: "PlayStation 5 Slim Standard", usa: 499.00 },
        { category: "PlayStation", name: "PlayStation 5 Pro", usa: 699.00 },
        { category: "Samsung", name: "Samsung Galaxy S26 Ultra 256GB", usa: 1199.00 },
        { category: "Samsung", name: "Samsung Galaxy S26 Ultra 512GB", usa: 1299.00 },
        { category: "AirPods", name: "Apple AirPods (2nd Gen)", usa: 129.00 },
        { category: "AirPods", name: "Apple AirPods (3rd Gen)", usa: 169.00 },
        { category: "AirPods", name: "Apple AirPods 4", usa: 129.00 },
        { category: "AirPods", name: "Apple AirPods 4 con ANC", usa: 179.00 },
        { category: "AirPods", name: "Apple AirPods Pro 2", usa: 249.00 },
        { category: "AirPods", name: "Apple AirPods Max", usa: 549.00 }
    ];

    let isDirty = false;
    let currentStatus = 'NUEVO';
    const inputDateEl = document.getElementById('inputDate');
    const badgeEl = document.getElementById('batchStatusBadge');

    function markDirty() {
        if (currentStatus !== 'CERRADO') {
            isDirty = true;
        }
    }

    // 5. Listeners para recálculo automático
    costInputs.forEach(input => {
        input.addEventListener('input', () => {
            calculateGyP();
            markDirty();
        });
    });

    const noteInputs = document.querySelectorAll('.cost-note');
    noteInputs.forEach(input => input.addEventListener('input', markDirty));

    function addRowListeners(row) {
        const inputs = row.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                calculateGyP();
                markDirty();
            });
        });
        
        row.querySelector('.delete-btn').addEventListener('click', () => {
            if (currentStatus === 'CERRADO') return;
            row.remove();
            calculateGyP();
            markDirty();
        });
    }

    // Agregar fila
    addProductBtn.addEventListener('click', () => {
        if (currentStatus === 'CERRADO') return;
        const clone = rowTemplate.content.cloneNode(true);
        const newRow = clone.querySelector('.product-row');
        
        // Llenar el select con el catálogo
        const select = newRow.querySelector('.row-desc');
        const categories = [...new Set(catalogItems.map(i => i.category))];
        categories.forEach(cat => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = cat;
            catalogItems.filter(i => i.category === cat).forEach(item => {
                const opt = document.createElement('option');
                opt.value = item.name;
                opt.textContent = item.name;
                optgroup.appendChild(opt);
            });
            select.appendChild(optgroup);
        });

        productsBody.appendChild(newRow);
        addRowListeners(newRow);
        calculateGyP();
        markDirty();
    });

    // --- 6. CICLO DE VIDA DEL LOTE (PERSISTENCIA Y ESTADOS) ---

    function fillFormData(data) {
        // Cargar Costos
        const c = data.costs;
        document.getElementById('costCourier').value = c.courier.val; document.getElementById('noteCourier').value = c.courier.note;
        document.getElementById('costTransfer').value = c.transfer.val; document.getElementById('noteTransfer').value = c.transfer.note;
        document.getElementById('costAirfare').value = c.airfare.val; document.getElementById('noteAirfare').value = c.airfare.note;
        document.getElementById('costFood').value = c.food.val; document.getElementById('noteFood').value = c.food.note;
        document.getElementById('costTransport').value = c.transport.val; document.getElementById('noteTransport').value = c.transport.note;
        document.getElementById('costAds').value = c.ads.val; document.getElementById('noteAds').value = c.ads.note;
        document.getElementById('costOther').value = c.other.val; document.getElementById('noteOther').value = c.other.note;

        // Cargar Productos
        productsBody.innerHTML = ''; 
        if (data.products && data.products.length > 0) {
            data.products.forEach(p => {
                addProductBtn.click();
                const lastRow = productsBody.lastElementChild;
                lastRow.querySelector('.row-qty').value = p.qty;
                lastRow.querySelector('.row-desc').value = p.desc;
                lastRow.querySelector('.row-buy-usa').value = p.buyUSA;
                lastRow.querySelector('.row-sell-usd').value = p.sellUSD;
            });
        } else {
            addProductBtn.click();
        }
    }

    function setUIState(status) {
        currentStatus = status;
        badgeEl.textContent = status;
        badgeEl.className = 'badge'; // reset
        
        const allInputs = document.querySelectorAll('input, select, textarea');
        const actionBtns = document.querySelectorAll('.delete-btn');

        if (status === 'CERRADO') {
            badgeEl.classList.add('badge-closed');
            allInputs.forEach(input => {
                if(input.id !== 'inputDate') input.classList.add('locked-input');
            });
            actionBtns.forEach(btn => btn.style.display = 'none');
            addProductBtn.style.display = 'none';
            document.getElementById('saveBatchBtn').style.display = 'none';
            document.getElementById('closeBatchBtn').style.display = 'none';
        } else if (status === 'EN PROCESO') {
            badgeEl.classList.add('badge-process');
            allInputs.forEach(input => input.classList.remove('locked-input'));
            actionBtns.forEach(btn => btn.style.display = 'inline-block');
            addProductBtn.style.display = 'inline-block';
            document.getElementById('saveBatchBtn').style.display = 'inline-block';
            document.getElementById('closeBatchBtn').style.display = 'inline-block';
        } else {
            badgeEl.classList.add('badge-new');
            allInputs.forEach(input => input.classList.remove('locked-input'));
            actionBtns.forEach(btn => btn.style.display = 'inline-block');
            addProductBtn.style.display = 'inline-block';
            document.getElementById('saveBatchBtn').style.display = 'inline-block';
            document.getElementById('closeBatchBtn').style.display = 'inline-block';
        }
    }

    function getFormDataJSON(status) {
        // Collect Products
        const products = [];
        productsBody.querySelectorAll('.product-row').forEach(row => {
            products.push({
                qty: parseFloat(row.querySelector('.row-qty').value) || 0,
                desc: row.querySelector('.row-desc').value || "",
                buyUSA: parseFloat(row.querySelector('.row-buy-usa').value) || 0,
                sellUSD: parseFloat(row.querySelector('.row-sell-usd').value) || 0
            });
        });

        // Collect Costs
        const costs = {
            courier: { val: document.getElementById('costCourier').value, note: document.getElementById('noteCourier').value },
            transfer: { val: document.getElementById('costTransfer').value, note: document.getElementById('noteTransfer').value },
            airfare: { val: document.getElementById('costAirfare').value, note: document.getElementById('noteAirfare').value },
            food: { val: document.getElementById('costFood').value, note: document.getElementById('noteFood').value },
            transport: { val: document.getElementById('costTransport').value, note: document.getElementById('noteTransport').value },
            ads: { val: document.getElementById('costAds').value, note: document.getElementById('noteAds').value },
            other: { val: document.getElementById('costOther').value, note: document.getElementById('noteOther').value }
        };

        return {
            date: inputDateEl.value,
            status: status,
            products: products,
            costs: costs
        };
    }

    async function saveBatch(status) {
        const data = getFormDataJSON(status);
        const saveBtn = document.getElementById('saveBatchBtn');
        const closeBtn = document.getElementById('closeBatchBtn');
        
        const originalSaveText = saveBtn.textContent;
        saveBtn.disabled = true;
        saveBtn.textContent = 'Guardando...';

        try {
            const response = await fetch(`${API_BASE_URL}/gyp/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Error en la respuesta del servidor');

            isDirty = false;
            setUIState(status);
            alert(`Lote ${status === 'CERRADO' ? 'CERRADO' : 'GUARDADO'} exitosamente en la nube para la fecha: ${inputDateEl.value}`);
        } catch (error) {
            console.error('Error salvando lote:', error);
            alert('Error crítico: No se pudo guardar en Supabase. Verifica tu conexión.');
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = originalSaveText;
        }
    }

    async function loadBatch(dateStr) {
        productsBody.innerHTML = ''; // Limpiar filas
        const loadingMsg = document.createElement('tr');
        loadingMsg.innerHTML = '<td colspan="7" style="text-align:center; padding: 20px;">Cargando datos desde la nube...</td>';
        productsBody.appendChild(loadingMsg);

        try {
            const response = await fetch(`${API_BASE_URL}/gyp/load/${dateStr}`);
            const result = await response.json();
            
            productsBody.innerHTML = ''; // Limpiar mensaje de carga

            if (result.status === 'success') {
                const data = result.data;
                fillFormData(data);
                setUIState(data.status);
            } else {
                // MIGRACIÓN: Si no hay en nube, buscar en localStorage antiguo
                const localDataStr = localStorage.getItem('gyp_batch_' + dateStr);
                if (localDataStr) {
                    if (confirm(`Encontramos datos locales de "${dateStr}" en esta computadora. ¿Deseas recuperarlos y subirlos a la nube?`)) {
                        const localData = JSON.parse(localDataStr);
                        fillFormData(localData);
                        setUIState(localData.status || 'EN PROCESO');
                        markDirty(); // Forzar estado sucio para que el usuario pueda darle a Guardar
                        alert("Datos locales cargados. Presiona 'GUARDAR LOTE' para sincronizarlos con la nube definitivamente.");
                        return;
                    }
                }

                // No existe lote en ningún lado, reset a nuevo
                costInputs.forEach(i => i.value = "0");
                document.querySelectorAll('.cost-note').forEach(i => i.value = "");
                addProductBtn.click();
                setUIState('NUEVO');
            }
        } catch (error) {
            console.error('Error cargando lote:', error);
            productsBody.innerHTML = '<td colspan="7" style="text-align:center; color: var(--danger); padding: 20px;">Error al conectar con la base de datos.</td>';
            setUIState('NUEVO');
        }
        
        calculateGyP();
        isDirty = false;
    }

    // Inicializar app
    let previousDate = new Date().toISOString().split('T')[0];
    inputDateEl.value = previousDate;
    
    // Primero añadimos la fila por defecto para que exista al cargar
    addProductBtn.click(); 
    loadBatch(inputDateEl.value); // Intentar cargar lo de hoy si existe

    // Manejo de cambio de fecha
    inputDateEl.addEventListener('change', (e) => {
        const newDate = e.target.value;
        if (isDirty) {
            const confirmDiscard = confirm("Tienes cambios sin guardar en este lote. ¿Estás seguro que deseas cambiar de fecha y perderlos?");
            if (!confirmDiscard) {
                e.target.value = previousDate; // Revertir fecha
                return;
            }
        }
        previousDate = newDate;
        loadBatch(newDate);
    });

    document.getElementById('saveBatchBtn').addEventListener('click', () => saveBatch('EN PROCESO'));
    
    document.getElementById('closeBatchBtn').addEventListener('click', () => {
        if(confirm("¿Estás seguro que deseas CERRAR este lote? No podrás hacer más modificaciones.")) {
            saveBatch('CERRADO');
        }
    });
});
