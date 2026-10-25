
import pandas as pd

df = pd.read_csv("retail_sales_analyzer.csv")

# Basic inspection
print(df.head(10))
print("Shape:\n", df.shape)
print(df.isnull().sum())
print(df.columns)
df.info()
print(df.describe())
print("Duplicates:", df.duplicated().sum())

print("Unique products:", df["Product"].nunique())
print("Unique categories:", df["Category"].nunique())
print("Unique customers:", df["Customer_ID"].nunique())
print("Unique regions:", df["Region"].nunique())

# Datetime conversion
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month Name"] = df["Order_Date"].dt.month_name()

print(df[["Order_Date", "Year", "Month", "Month Name"]].head(10))
print(df.sort_values("Order_Date", ascending=True).head(10))

# Group and aggregate

# Monthly revenue by year and month
monthly_revenue = df.groupby(["Year", "Month"])["Revenue"].sum()
monthly_revenue = monthly_revenue.sort_index()
print("Monthly revenue:\n", monthly_revenue)

print("Top 5 year-month combinations by revenue:")
print(monthly_revenue.sort_values(ascending=False).head(5))

# Total profit by category
total_profit = df.groupby("Category")["Profit"].sum()
print("Profit by category:\n", total_profit)

# Average profit by region
print("Average profit by region:\n",
      df.groupby("Region")["Profit"].mean())

# Yearly revenue
yearly_revenue = df.groupby("Year")["Revenue"].sum()
print("Yearly revenue:\n",
      yearly_revenue.sort_values(ascending=False))

# Top 10 customers by revenue
top_customers = df.groupby("Customer_ID")["Revenue"].sum()
print("Top 10 customers by revenue:\n",
      top_customers.sort_values(ascending=False).head(10))

# Category performance
category_performance = df.groupby("Category").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum")
)

print("Category performance:\n",
      category_performance.sort_values(
          by="Total_Revenue", ascending=False
      ))

# Data quality checks
print("Negative quantity records:\n",
      df[df["Quantity"] < 0])

print("Negative revenue records:\n",
      df[df["Revenue"] < 0])

print("Negative cost records:\n",
      df[df["Cost"] < 0])

print("Negative unit price records:\n",
      df[df["Unit_Price"] < 0])

print("Negative unit cost records:\n",
      df[df["Unit_Cost"] < 0])

print("Zero quantity records:\n",
      df[df["Quantity"] == 0])

invalid_discount = (
    (df["Discount_Pct"] < 0) |
    (df["Discount_Pct"] > 1)
)
print("Invalid discount records:\n", df[invalid_discount])

print("Data quality checks completed.")

# Business analysis: category profit margin
category_performance["Profit_Margin"] = (
    category_performance["Total_Profit"] /
    category_performance["Total_Revenue"]
) * 100

print("Category performance by profit margin:\n",
      category_performance.sort_values(
          by="Profit_Margin", ascending=False
      ))

# Month-over-month revenue growth
monthly_growth = monthly_revenue.pct_change() * 100
print("Monthly revenue growth (%):\n", monthly_growth)

# Regional performance
regional_performance = df.groupby("Region").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum")
)

regional_performance["Profit_Margin"] = (
    regional_performance["Total_Profit"] /
    regional_performance["Total_Revenue"]
) * 100

print("Regional performance:\n",
      regional_performance.sort_values(
          by="Total_Revenue", ascending=False
      ))

# Product performance
product_performance = df.groupby("Product").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum")
)

print("Top products by revenue:\n",
      product_performance.sort_values(
          by="Total_Revenue", ascending=False
      ).head(10))

print("Top products by profit:\n",
      product_performance.sort_values(
          by="Total_Profit", ascending=False
      ).head(10))

# Customer performance
customer_performance = df.groupby("Customer_ID").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order_ID", "count")
)

print("Top 10 customers by revenue:\n",
      customer_performance.sort_values(
          by="Total_Revenue", ascending=False
      ).head(10))

# Summary data quality checks
print("Zero or negative quantity:",
      (df["Quantity"] <= 0).sum())

print("Negative prices:",
      ((df["Unit_Price"] < 0) |
       (df["Unit_Cost"] < 0)).sum())

print("Negative revenue or cost:",
      ((df["Revenue"] < 0) |
       (df["Cost"] < 0)).sum())

print("Invalid discounts:",
      invalid_discount.sum())

print("Data types:\n", df.dtypes)

# Export processed dataset
df.to_csv("retailpulse_cleaned.csv", index=False)

print("Export completed: retailpulse_cleaned.csv")
