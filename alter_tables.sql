-- DO NOT RUN AGAIN 
USE aicore;

SELECT * FROM orders_table
LIMIT 20; 

-- Task 1: Cast the columns of the orders_table to the correct data types.

ALTER TABLE orders_table
MODIFY COLUMN date_uuid CHAR(36),
MODIFY COLUMN user_uuid CHAR(36),
MODIFY COLUMN card_number VARCHAR(24),
MODIFY COLUMN store_code VARCHAR(15),
MODIFY COLUMN product_code VARCHAR(15),
MODIFY COLUMN product_quantity SMALLINT;




DESCRIBE orders_table; 

-- Task 2: Cast the columns of the dim users to the correct data types.

ALTER TABLE dim_users
MODIFY COLUMN first_name VARCHAR(225),
MODIFY COLUMN last_name VARCHAR(225),
MODIFY COLUMN date_of_birth DATE,
MODIFY COLUMN country_code VARCHAR(10),
MODIFY COLUMN user_uuid CHAR(36),
MODIFY COLUMN join_date DATE;



SELECT LENGTH(country_code) AS l FROM dim_users
ORDER BY l DESC 
limit 10; 

DESCRIBE dim_products;

-- Task 4: Make changes to the dim_products table for the delivery team.

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(50);

UPDATE dim_products
SET weight_class = CASE
WHEN weight < 2 THEN 'Light'
WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
WHEN weight >= 140 THEN 'Truck Required'
END;

SELECT weight_class FROM dim_products; 


DESCRIBE dim_products; 

ALTER TABLE dim_products
RENAME COLUMN removed TO still_available; 


UPDATE dim_products
SET still_available = CASE 
WHEN still_available = 'Still_avaliable' THEN TRUE 
WHEN still_available = 'Removed' THEN FALSE
ELSE NULL
END; 



-- Task 5: Update the dim_products table with the required data types.

ALTER TABLE dim_products
MODIFY COLUMN uuid CHAR(36),
MODIFY COLUMN still_available BOOL;


-- Task 6: Update the dim_date times table.

DESCRIBE dim_date_times; 


ALTER TABLE dim_date_times
MODIFY COLUMN date_uuid CHAR(36);


-- Task 7: Updating the dim card details table.

DESCRIBE dim_card_details; 

ALTER TABLE dim_card_details
MODIFY COLUMN expiry_date VARCHAR(100);


-- Task 8: Create the primary keys in the dimension tables.

DESCRIBE dim_card_details; 

ALTER TABLE dim_card_details
ADD PRIMARY KEY(card_number);

ALTER TABLE dim_date_times
ADD PRIMARY KEY(date_uuid);

ALTER TABLE dim_products
ADD PRIMARY KEY(product_code);

ALTER TABLE dim_users
ADD PRIMARY KEY(user_uuid);


ALTER TABLE dim_users
ADD PRIMARY KEY(user_uuid);

ALTER TABLE dim_store_details
ADD PRIMARY KEY(store_code);

-- Task 9: Finalising the star-based schema & adding the foreign keys to the orders table.

ALTER TABLE orders_table
ADD CONSTRAINT fk_card 
FOREIGN KEY (card_number) REFERENCES dim_card_details (card_number);


-- SELECT DISTINCT card_number  FROM orders_table 
-- WHERE card_number NOT IN (SELECT card_number FROM dim_card_details_v3); 

-- SELECT COUNT(DISTINCT card_number) FROM orders_table;

-- SELECT COUNT(DISTINCT card_number) FROM dim_card_details;

-- SELECT DISTINCT card_number  FROM dim_card_details_v3
-- WHERE card_number NOT IN (SELECT card_number FROM orders_table);

-- SELECT COUNT(DISTINCT card_number) FROM dim_card_details_v2;


ALTER TABLE orders_table
ADD CONSTRAINT fk_date 
FOREIGN KEY (date_uuid) REFERENCES dim_date_times (date_uuid);


ALTER TABLE orders_table
ADD CONSTRAINT fk_product 
FOREIGN KEY (product_code) REFERENCES dim_products (product_code);

-- SELECT COUNT(DISTINCT product_code) FROM dim_products; 

-- SELECT DISTINCT product_code FROM orders_table; 

-- SELECT DISTINCT *  FROM orders_table 
-- WHERE product_code NOT IN (SELECT product_code FROM dim_products);

-- SELECT DISTINCT *  FROM dim_products 
-- WHERE product_code NOT IN (SELECT product_code FROM orders_table);

ALTER TABLE orders_table
ADD CONSTRAINT fk_store 
FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code);



ALTER TABLE orders_table
ADD CONSTRAINT fk_users
FOREIGN KEY (user_uuid) REFERENCES dim_users (user_uuid);



DESCRIBE dim_users; 

