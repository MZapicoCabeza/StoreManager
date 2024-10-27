// Función para hacer la llamada a la API y obtener los nombres de las tiendas
async function fetchStoreData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/tiendas'); // Llama a la API para obtener las tiendas
        if (!response.ok) {
            throw new Error('Error al cargar las tiendas');
        }

        const tiendasText = await response.text();
        return tiendasText.split('<br>').map(tienda => tienda.trim()).filter(tienda => tienda !== ''); // Devuelve un array de nombres de tiendas
    } catch (error) {
        console.error('Error:', error);
        return []; // Devuelve un array vacío en caso de error
    }
}

// Función para llenar el menú desplegable con los nombres de las tiendas
async function loadStoreDropdown() {
    const tiendas = await fetchStoreData(); // Llama a la función que obtiene los datos de la API

    const dropdown = document.getElementById('storeIdDropdown');
    dropdown.innerHTML = '<option value="">Selecciona una tienda</option>'; // Limpiar las opciones

    // Llenar el menú desplegable con los nombres de las tiendas obtenidas
    tiendas.forEach(tienda => {
        const option = document.createElement('option');
        option.textContent = tienda; // Nombre de la tienda como texto visible
        dropdown.appendChild(option);
    });
}

// Llamar a la función para cargar las tiendas al cargar la página
document.addEventListener('DOMContentLoaded', (event) => {
    loadStoreDropdown(); // Carga las tiendas dinámicamente
});