DROP TABLE IF EXISTS Tienda;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Compra;
DROP TABLE IF EXISTS Cliente;
Drop TABLE IF EXISTS Venta;

CREATE TABLE Tienda ( 
    id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(32),
    poblacion VARCHAR(32), 
    ubicacion VARCHAR(32)
);

CREATE TABLE Producto (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tienda INTEGER,
    nombre_producto VARCHAR(64),
    categoria VARCHAR(32),
    fecha_alta DATE,
    cantidad INTEGER,  
    precio DOUBLE (10, 2),
    FOREIGN KEY (id_tienda) REFERENCES Tienda(id_tienda) ON DELETE CASCADE
);

CREATE TABLE Cliente (
    DNI VARCHAR(9) NOT NULL PRIMARY KEY,
    nombre VARCHAR(32) , 
    apellido1 VARCHAR(32), 
    apellido2 VARCHAR(32),
    fecha_nacimiento DATE,
    fecha_alta_cliente DATE
);

CREATE TABLE Compra (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente VARCHAR(9),
    fecha DATE,
    productos TEXT,
    precio_total DOUBLE(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(DNI) ON DELETE CASCADE
);


CREATE TABLE Venta (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tienda INTEGER,
    fecha DATE,
    productos TEXT[],
    cantidad_vendida TEXT[],
    FOREIGN KEY (id_tienda) REFERENCES Tienda(id_tienda) ON DELETE CASCADE
);
