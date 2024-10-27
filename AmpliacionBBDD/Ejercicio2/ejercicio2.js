/*

Problemas de agregación para la colección de users


4.	Inicios de sesión recientes: recupere los usuarios que han iniciado sesión en los últimos 30 días.
5.	Nombres de usuario que comienzan con una letra: Encuentre todos los nombres de usuario que comiencen con una letra específica.
6.	Usuarios por último año de inicio de sesión: agrupe a los usuarios por el año de su último inicio de sesión y cuente el número de usuarios de cada año.
7.	Usuarios con campos faltantes: identifique a los usuarios que no tienen una dirección de correo electrónico.
8.	Edad media por nombre inicial: Calcula la edad media de los usuarios agrupados por la primera letra de su nombre.
9.	Usuarios con varias condiciones: busque usuarios que tengan más de 30 años y que hayan iniciado sesión en los últimos 6 meses.
Problemas de agregación para la colección de products
11.	Precio medio por categoría: Calcula el precio medio de los productos de cada categoría.
12.	Valor total del inventario: Calcule el valor total de todos los productos.
13.	Los 3 productos más caros: Encuentra los 3 productos más caros.
14.	Productos con una palabra clave específica: busque productos cuya descripción contenga una palabra clave específica.
15.	Recuento de productos por categoría: cuente el número de productos de cada categoría.
16.	Simulación de aumento de precios: Calcule los nuevos precios si los precios de todos los productos se incrementaron en un 10%.
17.	Productos con varias condiciones: busca productos que pertenezcan a una categoría específica y que tengan un precio superior a un determinado umbral.
Problemas de agregación para la colección de places
21.	Calificación promedio de los lugares: Calcule la calificación promedio de todos los lugares.
22.	Lugares cerca de un punto: Encuentre todos los lugares dentro de un radio de 10 kilómetros de un punto determinado.
23.	Los 5 lugares mejor valorados: Encuentra los 5 lugares mejor valorados.
24.	Lugares por proximidad: ordene los lugares por su distancia a un punto determinado.
25.	Lugares con una palabra clave de nombre específico: busque lugares cuyo nombre contenga una palabra clave específica.
26.	Lugares por recuento de calificación: cuente el número de lugares para cada valor de calificación.
27.	Lugares con múltiples condiciones: Encuentre lugares que tengan una calificación superior a 4.5 y estén a una cierta distancia de un punto determinado.

Información adicional

Trabaja con fechas.
Cómo usar Date como una fecha y no como una cadena. Y cómo obtener la diferencia entre la fecha actual y el atributo en días.
db.users.aggregate([{$addFields : {lastLogin : {$toDate : "$lastLogin"}}},{$addFields : {lastLoginDays: {$dateDiff : {startDate: "$lastLogin", endDate : "$$NOW", unit: "day"}}}}])
La  operación $addFields agrega un archivo por un nombre y una expresión para sus valores.
La  operación $toDate transforma un atributo en un tipo Date en lugar de un tipo String.
La  operación $dateDiff permite restar fechas con una unidad específica, en este caso con "días".
La  operación $$NOW devuelve la fecha actual en formato Date.
Para obtener más información sobre dateDiff, consulte el enlace

Trabajar con elementos existentes o no
Utilice el operador $exists para filtrar por un campo que sale o no.
Ejemplo de uso: 
db.users.aggregate([{$match : {name : {$exists : false}}}])

Trabajar con distancias
Utilice la operación $geoNear para consultar la distancia a un punto. Ejemplo:
db.buildings.aggregate([
    {
        $geoNear: {
            near: { type: "Point", coordinates: [-74.0445, 40.6892] },
            maxDistance: 5000,
            distanceField: "location",
            spherical: true
        }
    }
])
Detalles sobre los parámetros:
•	near: El punto con el que comparar.
•	distanceField: el campo de la colección que contiene el punto.
•	maxDistance: La distancia máxima en metros.
•	spherical: Se establece en true para considerar la curvatura de la Tierra.
Nota: Si omite el  parámetro maxDistance, la consulta devolverá todos los lugares ordenados por distancia en metros, en el  atributo location .



*/

/* 1.	Edad media de los usuarios: Calcula la edad media de todos los usuarios. */


db.Users.aggregate([

    {
        $group:{
            _id: null, 
            edadMedia: {$avg: "$age"}
        }
    },
    {
        $project:{
            _id: 0, 
            edadMedia: 1
        }

    }

])

/* 2.	Los 5 usuarios más antiguos: Encuentre los 5 usuarios más antiguos.*/
//$addFields crea un nuevo campo temporal

db.Users.aggregate([

    {
        $addFields:{ 
            lastLoginToDate: {$toDate: "$lastLogin"}
        }
    },
    {
        $sort:{
            lastLoginToDate:1
        }
    },
    {
        $limit:5
    },
    {
        $project:{
            firstName:1,
            lastName: 1,
            lastLogin:1
        }
    }

])

/* 3.	Usuarios con correos electrónicos de dominio específico: cuente el número de usuarios con direcciones de correo electrónico de un dominio específico (por ejemplo, example.com). */

db.Users.aggregate([

    {
        $match:{
            email: {$regex :/@example\.com$/}
        }
    },
    {
        $count: "UsuariosConDominioEspecifico"
    }
])