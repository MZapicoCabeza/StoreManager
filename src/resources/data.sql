--Carga inicial de datos. Se cargan de maestro a detalle

--Tienda
INSERT INTO Tienda (id_tienda, nombre, poblacion, ubicacion) VALUES
    (1, 'Tienda 1', 'Oviedo', 'Calle 1'),
    (2, 'Tienda 2', 'Gijon', 'Calle 2'),
    (3, 'Tienda 3', 'Aviles', 'Calle 3'),
    (4, 'Tienda 4', 'Ribadesella', 'Calle 4'),
    (6, 'Tienda 6', 'Ribadesella', 'Calle 4'),
    (5, 'Tienda 5', 'Ribadesella', 'Calle 5');

--Producto
-- Inserción de productos en la tabla Producto
INSERT INTO Producto (id_producto, id_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio) VALUES
    (1, 1, 'Manzanas', 'Frutas', '2024-01-05', 50, 0.50),     -- Producto para Tienda 1
    (2, 1, 'Leche', 'Lacteos', '2024-01-06', 200, 1.10),      -- Producto para Tienda 1
    (3, 2, 'Pan', 'Panaderia', '2024-01-07', 100, 1.00),      -- Producto para Tienda 2
    (4, 2, 'Cafe', 'Bebidas', '2024-01-08', 150, 1.50),       -- Producto para Tienda 2
    (5, 3, 'Pasta', 'Alimentos', '2024-01-09', 80, 5.25),     -- Producto para Tienda 3
    (6, 3, 'Tomates', 'Verduras', '2024-01-10', 60, 8.99),    -- Producto para Tienda 3
    (7, 4, 'Jabon', 'Higiene', '2024-01-11', 120, 6.00),      -- Producto para Tienda 4
    (8, 4, 'Arroz', 'Alimentos', '2024-01-12', 90, 3.50);     -- Producto para Tienda 4


--Cliente
INSERT INTO Cliente (DNI, nombre, apellido1, apellido2, fecha_nacimiento, fecha_alta_cliente)
VALUES 
    ('11111111A', 'Paula', 'Garcia', 'Fernandez','2000-01-01','2024-01-10'),
    ('22222222B', 'Pablo', 'Alvarez', 'Menendez','2002-02-02','2024-02-10'),
    ('33333333C', 'Martina', 'Rodriguez', 'Santos','2003-03-03','2024-03-10');


INSERT INTO Compra (id_compra, id_cliente, fecha, productos, precio_total) VALUES
    (1, '11111111A', '2024-10-01', 'Manzanas, Leche, Pan', 10.1),
    (2, '11111111A', '2024-10-05', 'Arroz, Pasta', 8.75),
    (3, '22222222B', '2024-06-06', 'Jabon', 6.00);



INSERT INTO Venta (id_venta, id_tienda, fecha, productos, cantidad_vendida) VALUES
(1, 1, '2024-10-01', 'Manzanas, Leche, Pan', '5, 2, 1'),
(2, 2, '2024-10-02', 'Huevos, Yogurt, Arroz', '12, 8, 3'),
(3, 3, '2024-10-03', 'Tomates, Pasta, Queso', '7, 4, 2'),
(4, 1, '2024-10-04', 'Cafe, Azucar, Leche', '3, 1, 2'),
(5, 2, '2024-10-05', 'Atun, Platanos, Cereal', '6, 10, 3');
