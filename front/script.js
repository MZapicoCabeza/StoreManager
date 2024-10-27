// Selecciona el botón "Administrador" usando su ID
const adminButton = document.getElementById('adminButton'); // Asegúrate de que este ID exista en tu HTML
// Agrega un evento al botón para escuchar el clic
adminButton.addEventListener('click', function() {
    window.location.href = 'admin.htm'; // Redirige a la página de inventario
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
        h4.style.color = '#ffffff';
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

// Función para registrar un producto en la tienda seleccionada
// Función para registrar un producto en la tienda seleccionada
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

    try {
        // Hacer la llamada a la API para registrar el producto
        const response = await fetch('http://127.0.0.1:5000/api/registrar_producto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_tienda: nombreTienda, // Asegúrate de que este es el ID correcto
                nombre_producto: nombreProducto,
                categoria: categoria,
                fecha_alta: fechaAlta, // Usar el formato correcto
                cantidad: cantidad,
                precio: precio
            })
        });

        // Verificar la respuesta del servidor
        if (!response.ok) {
            const errorData = await response.json(); // Obtén los datos del error
            console.error('Error desde el servidor:', errorData);
            alert(`Error: ${errorData.error || 'Error al registrar el producto'}`);
            return;
        }

        // Obtener el resultado de la respuesta de la API
        const result = await response.json();
        alert(result.message); // Mostrar el mensaje de éxito
    } catch (error) {
        console.error('Error:', error);
        alert('Error al registrar el producto');
    }
}


