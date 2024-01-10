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



