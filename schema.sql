CREATE TABLE sales (
    id            integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sale_date     date NOT NULL,
    product_name  varchar(255) NOT NULL,
    quantity      decimal(10,3) NOT NULL,
    price         decimal(10,2) NOT NULL
);
