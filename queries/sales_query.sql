SELECT
    soh.SalesOrderID,
    soh.OrderDate,
    sod.LineTotal,
    p.Name AS ProductName,
    sp.Name AS StateProvince
FROM Sales.SalesOrderHeader soh
JOIN Sales.SalesOrderDetail sod
    ON soh.SalesOrderID = sod.SalesOrderID
JOIN Production.Product p
    ON sod.ProductID = p.ProductID
JOIN Person.Address a
    ON soh.ShipToAddressID = a.AddressID
JOIN Person.StateProvince sp
    ON a.StateProvinceID = sp.StateProvinceID
