const adminButton = document.getElementById('adminButton');
adminButton.addEventListener('click', function() {
    window.location.href = 'admin.htm';
});


const gerenteButton = document.getElementById('gerenteButton');
adminButton.addEventListener('click', function() {
    window.location.href = 'gerente.htm';
});

// Función para hacer la llamada a la API y mostrar el inventario
function fetchInventory() {
    const dropdown = document.getElementById('storeIdDropdown');
    const nombreTienda = dropdown.value;
    if (!nombreTienda) {
        alert("Por favor, selecciona una tienda.");
        return;
    }
    fetch(`http://127.0.0.1:5000/api/inventory?nombre_tienda=${encodeURIComponent(nombreTienda)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la llamada a la API');
            }
            return response.json();
        })
        .then(data => {
            displayData(data);
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.body.innerHTML = `<h1>Error al obtener los datos del inventario: ${error.message}</h1>`;
        });
}

// Función para mostrar los datos en el cuerpo
function displayData(data) {
    const inventoryContent = document.getElementById('inventoryContent');
    inventoryContent.innerHTML = '';
    inventoryContent.style.display = 'block';

    if (data && data.inventario) {
        const h4 = document.createElement('h4');
        h4.textContent = `Inventario para la tienda: ${data.tienda}`;
        h4.style.color = '#4b8b3b';
        h4.style.marginTop = '20px';
        inventoryContent.appendChild(h4);

        const table = document.createElement('table');
        table.classList.add('inventory-table');

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const headerCell1 = document.createElement('th');
        headerCell1.textContent = 'Producto';
        const headerCell2 = document.createElement('th');
        headerCell2.textContent = 'Cantidad';

        headerRow.appendChild(headerCell1);
        headerRow.appendChild(headerCell2);
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        data.inventario.forEach(item => {
            const row = document.createElement('tr');
            const cell1 = document.createElement('td');
            cell1.textContent = item.nombre_producto;
            const cell2 = document.createElement('td');
            cell2.textContent = item.cantidad;

            row.appendChild(cell1);
            row.appendChild(cell2);
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        inventoryContent.appendChild(table);
    } else {
        const noDataMessage = document.createElement('h1');
        noDataMessage.textContent = 'No se encontraron datos.';
        noDataMessage.classList.add('text-black');
        inventoryContent.appendChild(noDataMessage);
    }
}

// Evento para cargar el inventario al hacer clic en el botón
document.getElementById('fetchInventoryButton').addEventListener('click', fetchInventory);

// Cargar las tiendas al cargar la página
loadStoreDropdown();





document.addEventListener('DOMContentLoaded', loadStoreDropdown);
async function registerProduct() {
    const nombreTienda = document.getElementById('storeIdDropdown').value;
    const nombreProducto = document.getElementById('productName').value.trim();
    const categoria = document.getElementById('productCategory').value.trim();
    const cantidad = parseInt(document.getElementById('productQuantity').value, 10);
    const precio = parseFloat(document.getElementById('productPrice').value);

    // Obtener la fecha actual en formato 'dd-mm-yyyy'
    const fecha = new Date();
    const fechaAlta = `${fecha.getDate().toString().padStart(2, '0')}-${(fecha.getMonth() + 1).toString().padStart(2, '0')}-${fecha.getFullYear()}`;

    // Validar que todos los campos son obligatorios
    if (!nombreTienda || !nombreProducto || !categoria || isNaN(cantidad) || isNaN(precio)) {
        alert('Todos los campos son obligatorios');
        return;
    }

    // Validar que la cantidad no sea negativa
    if (cantidad < 0) {
        alert('La cantidad no puede ser negativa');
        return;
    }

    try {
        // Hacer la llamada a la API para registrar el producto
        const response = await fetch('http://127.0.0.1:5000/api/registrar_producto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre_tienda: nombreTienda,
                nombre_producto: nombreProducto,
                categoria: categoria,
                fecha_alta: fechaAlta,
                cantidad: cantidad,
                precio: precio
            })
        });

        // Verificar la respuesta del servidor
        if (response.ok) {
            const result = await response.json();
            console.log(result); // Log para verificar el mensaje

            // Mostrar el mensaje de éxito en la página
            const successMessageDiv = document.getElementById('successMessage');
            successMessageDiv.innerText = result.message; // Asigna el mensaje de éxito
            successMessageDiv.style.display = 'block'; // Muestra el mensaje
        } else {
            const errorData = await response.json();
            console.error('Error desde el servidor:', errorData);
            alert(`Error: ${errorData.error || 'Error al registrar el producto'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al registrar el producto');
    }
}
async function registerSale() {
    // Limpiar mensajes anteriores
    const successMessageDiv = document.getElementById('successMessage');
    const errorMessageDiv = document.getElementById('errorMessage');
    successMessageDiv.innerText = ''; // Limpiar el mensaje de éxito
    successMessageDiv.style.display = 'none'; // Ocultar el mensaje de éxito

    errorMessageDiv.innerText = ''; // Limpiar el mensaje de error
    errorMessageDiv.style.display = 'none'; // Ocultar el mensaje de error

    const nombreTienda = document.getElementById('storeIdDropdown').value;
    const nombreProducto = document.getElementById('productName').value.trim();
    const cantidad = parseInt(document.getElementById('productQuantity').value, 10);

    if (!nombreTienda || !nombreProducto || isNaN(cantidad)) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (cantidad <= 0) {
        alert('La cantidad debe ser mayor que cero');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/registrar_venta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre_tienda: nombreTienda,
                nombre_producto: nombreProducto,
                cantidad_vendida: cantidad
            })
        });

        const result = await response.json();

        if (response.ok) {
            // Mostrar mensaje de éxito
            successMessageDiv.innerText = result.mensaje; // Asigna el mensaje de éxito
            successMessageDiv.style.display = 'block'; // Muestra el mensaje
        } else {
            // Mostrar mensaje de error
            errorMessageDiv.innerText = result.error; // Asigna el mensaje de error
            errorMessageDiv.style.display = 'block'; // Muestra el mensaje
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al registrar la venta');
    }
}

document.addEventListener('DOMContentLoaded', loadStoreDropdown);

// Función para registrar una tienda
async function registerStore() {
    // Limpiar mensajes anteriores
    const successMessageDiv = document.getElementById('successMessage');
    const errorMessageDiv = document.getElementById('errorMessage');
    successMessageDiv.innerText = ''; // Limpiar el mensaje de éxito
    successMessageDiv.style.display = 'none'; // Ocultar el mensaje de éxito
    errorMessageDiv.innerText = ''; // Limpiar el mensaje de error
    errorMessageDiv.style.display = 'none'; // Ocultar el mensaje de error

    const nombreTienda = document.getElementById('storeName').value.trim();
    const poblacion = document.getElementById('storePopulation').value.trim();
    const ubicacion = document.getElementById('storeLocation').value.trim();

    // Validar que todos los campos obligatorios están llenos
    if (!nombreTienda || !poblacion) {
        alert('El nombre de la tienda y la población son obligatorios');
        return;
    }

    try {
        // Hacer la llamada a la API para registrar la tienda
        const response = await fetch('http://127.0.0.1:5000/api/registrar_tienda', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre_tienda: nombreTienda,
                poblacion: poblacion,
                ubicacion: ubicacion || null // Enviar null si la ubicación está vacía
            })
        });

        // Verificar la respuesta del servidor
        if (response.ok) {
            const result = await response.json();
            console.log(result); // Log para verificar el mensaje

            // Mostrar el mensaje de éxito en la página
            successMessageDiv.innerText = result.message; // Asigna el mensaje de éxito
            successMessageDiv.style.display = 'block'; // Muestra el mensaje
        } else {
            const errorData = await response.json();
            console.error('Error desde el servidor:', errorData);
            alert(`Error: ${errorData.error || 'Error al registrar la tienda'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al registrar la tienda');
    }
}

// Asociar el evento de click al botón de registrar tienda
document.getElementById('registerStoreButton').addEventListener('click', registerStore);


// Evento para registrar la venta al hacer clic en el botón
document.getElementById('registerSaleButton').addEventListener('click', registerSale);


// Función para mostrar el informe de ventas en una tabla
async function fetchSalesReport() {
    const dropdown = document.getElementById('storeIdDropdown');
    const nombreTienda = dropdown.value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const salesReportContent = document.getElementById('salesReportContent');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    // Ocultar mensajes previos
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';
    salesReportContent.style.display = 'none';

    // Validar campos requeridos
    if (!nombreTienda || !startDate || !endDate) {
        errorMessage.innerText = "Por favor, completa todos los campos.";
        errorMessage.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/informe_ventas?nombre_tienda=${encodeURIComponent(nombreTienda)}&fecha_inicio=${encodeURIComponent(startDate)}&fecha_fin=${encodeURIComponent(endDate)}`);
        const result = await response.json();

        if (response.ok) {
            // Mostrar mensaje de éxito y cargar el informe de ventas
            successMessage.innerText = result.mensaje || "Informe de ventas cargado exitosamente.";
            successMessage.style.display = 'block';
            displaySalesReport(result);
        } else {
            // Mostrar mensaje de error en caso de respuesta no OK
            errorMessage.innerText = result.error || "Error al cargar el informe de ventas.";
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        errorMessage.innerText = 'Error al obtener el informe de ventas.';
        errorMessage.style.display = 'block';
    }
}

function displaySalesReport(data) {
    const salesReportContent = document.getElementById('salesReportContent');
    salesReportContent.innerHTML = '';
    salesReportContent.style.display = 'block';

    if (data && data.ventas && data.ventas.length > 0) {
        const h4 = document.createElement('h4');
        h4.textContent = `Informe de ventas para la tienda: ${data.nombre_tienda} desde ${data.fecha_inicio} hasta ${data.fecha_fin}`;
        h4.style.color = '#4b8b3b';
        salesReportContent.appendChild(h4);

        const table = document.createElement('table');
        table.classList.add('inventory-table');

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        const headerDate = document.createElement('th');
        headerDate.textContent = 'Fecha';

        const headerProduct = document.createElement('th');
        headerProduct.textContent = 'Producto';

        const headerQuantity = document.createElement('th');
        headerQuantity.textContent = 'Cantidad Vendida';

        headerRow.appendChild(headerDate);
        headerRow.appendChild(headerProduct);
        headerRow.appendChild(headerQuantity);
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        data.ventas.forEach(venta => {
            venta.detalles.forEach(detalle => {
                const row = document.createElement('tr');

                const dateCell = document.createElement('td');
                dateCell.textContent = venta.fecha;

                const productCell = document.createElement('td');
                productCell.textContent = detalle.producto;

                const quantityCell = document.createElement('td');
                quantityCell.textContent = detalle.cantidad;

                row.appendChild(dateCell);
                row.appendChild(productCell);
                row.appendChild(quantityCell);
                tbody.appendChild(row);
            });
        });
        table.appendChild(tbody);
        salesReportContent.appendChild(table);
    } else {
        const noDataMessage = document.createElement('div');
        noDataMessage.innerText = `No hay ventas registradas para la tienda '${data.nombre_tienda}' en el rango de fechas de ${data.fecha_inicio} hasta ${data.fecha_fin}.`;
        noDataMessage.style.color = 'green';
        noDataMessage.style.padding = '10px';
        noDataMessage.style.margin = '10px 0';
        salesReportContent.appendChild(noDataMessage);
    }
}