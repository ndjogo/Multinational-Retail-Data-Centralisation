USE aicore;

SELECT country_code, COUNT(*) AS num_of_stores FROM dim_store_details
GROUP BY country_code;

-- removing incorrect country code data 
DELETE FROM dim_store_details 
WHERE LENGTH(country_code) > 3; 

SELECT locality, COUNT(*) AS num_of_stores FROM dim_store_details
GROUP BY locality
ORDER BY num_of_stores DESC; 

SELECT d.month, ROUND(SUM(o.product_quantity * dim.product_price), 2) AS total_sales FROM orders_table as o 
INNER JOIN dim_date_times as d 
ON o.date_uuid = d.date_uuid
INNER JOIN dim_products as dim
ON o.product_code = dim.product_code 
GROUP BY d.month
ORDER BY total_sales DESC; 

SELECT DISTINCT store_type FROM dim_store_details; 
SELECT DISTINCT category FROM dim_products;



WITH new_store_details AS (SELECT store_code, 
CASE 
	WHEN store_type LIKE 'Web%' THEN 'Web' 
    ELSE 'Offline' 
END AS new_store_type
FROM dim_store_details)

SELECT COUNT(*) AS number_of_sales, SUM(product_quantity) AS product_quantity, new_store_type AS location 
FROM orders_table AS a 
INNER JOIN new_store_details AS s
ON a.store_code = s.store_code
GROUP BY new_store_type; 


SELECT store_type, ROUND(SUM(a.product_quantity*p.product_price), 2)  AS total_sales, 
ROUND((SUM(a.product_quantity*p.product_price)/SUM(SUM(a.product_quantity*p.product_price)) OVER())*100, 2) AS percetage_total
FROM orders_table AS a 
INNER JOIN dim_store_details as s
ON a.store_code = s.store_code
INNER JOIN dim_products as p
ON a.product_code = p.product_code
GROUP BY store_type
ORDER BY total_sales DESC; 



SELECT SUM(o.product_quantity*p.product_price) AS total_sales, 
d.year AS year,  d.month
FROM orders_table AS o 
INNER JOIN dim_products AS p 
ON o.product_code = p.product_code
INNER JOIN dim_date_times as d
ON o.date_uuid = d.date_uuid
GROUP BY d.year, d.month
ORDER BY total_sales DESC; 

SELECT SUM(staff_numbers), country_code FROM dim_store_details
GROUP BY country_code; 



SELECT SUM(o.product_quantity*p.product_price) AS total_sales, 
d.store_type AS store_type, 
d.country_code AS country_code 
FROM orders_table AS o 
INNER JOIN dim_products AS p 
ON o.product_code = p.product_code
INNER JOIN dim_store_details as d
ON o.store_code = d.store_code
WHERE country_code = 'DE'
GROUP BY store_type
ORDER BY total_sales DESC;



WITH time_taken AS (SELECT d.year AS year, 
AVG(c.date_payment_confirmed - d.timestamp) AS actual_time_taken
FROM orders_table as o 
INNER JOIN dim_date_times as d
ON o.date_uuid = d.date_uuid
INNER JOIN dim_card_details as c 
ON o.card_number = c.card_number
GROUP BY year
ORDER BY actual_time_taken)

SELECT year, CONCAT(
	'hours: ', FLOOR(actual_time_taken/3600000),
    ' minutes: ', FLOOR((actual_time_taken%3600000)/60000)) 
    AS time_difference 
FROM time_taken; 
    


SELECT d.year AS year, AVG(c.date_payment_confirmed - d.timestamp) AS actual_time_taken
FROM orders_table as o 
INNER JOIN dim_date_times as d
ON o.date_uuid = d.date_uuid
INNER JOIN dim_card_details as c 
ON o.card_number = c.card_number
GROUP BY year;
 


