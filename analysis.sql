create database retail_pulse;
use retail_pulse;

select * from retailpulse_cleaned;


select count(*)
from retailpulse_cleaned;
select * from retailpulse_cleaned;
select count(distinct(Product))
from retailpulse_cleaned;
select count(distinct(Customer_ID))
from retailpulse_cleaned;
select * from retailpulse_cleaned
limit 10;
select isnull(Revenue)
from retailpulse_cleaned;

select sum(Revenue) as Total_Revenue , sum(Cost) as Total_cost , sum(Profit) as Total_Profit
from retailpulse_cleaned;

select Category ,sum(Revenue) as Total_Revenue , sum(Cost) as Total_cost ,(SUM(Profit) / SUM(Revenue)) * 100 as Profit_margin
from retailpulse_cleaned
group by Category
order by Total_Revenue Desc ;

select Customer_ID ,sum(Revenue) as Total_Revenue , sum(Profit) as Total_profit 
from retailpulse_cleaned
group by Customer_ID
order by Total_Revenue Desc 
limit 10 ;

select Product ,sum(Revenue) as Total_Revenue , sum(Profit) as Total_profit 
from retailpulse_cleaned
group by Product
order by Total_Revenue Desc 
limit 10 ;

WITH monthly_sales AS (
    SELECT
        `Year`,
        `Month`,
        SUM(Revenue) AS Monthly_Revenue
    FROM retailpulse_cleaned
    GROUP BY `Year`, `Month`
),
monthly_comparison AS (
    SELECT
        `Year`,
        `Month`,
        Monthly_Revenue,
        LAG(Monthly_Revenue) OVER (
            ORDER BY `Year`, `Month`
        ) AS Previous_Month_Revenue
    FROM monthly_sales
)
SELECT
    `Year`,
    `Month`,
    Monthly_Revenue,
    Previous_Month_Revenue,
    Monthly_Revenue - Previous_Month_Revenue AS Revenue_Change,
    ROUND(
        (Monthly_Revenue - Previous_Month_Revenue)
        / NULLIF(Previous_Month_Revenue, 0) * 100,
        2
    ) AS MoM_Growth_Percent
FROM monthly_comparison
ORDER BY `Year`, `Month`;

with product_sales as (
                       select Product,sum(Revenue) as Total_revenue
                       from retailpulse_cleaned
                       group by Product 
                       )
select Product ,Total_Revenue,
Rank() over( ORDER BY Total_Revenue DESC
    ) AS Revenue_Rank
FROM product_sales
ORDER BY Revenue_Rank;
                         
                         


