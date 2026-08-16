# 📊 Superstore Sales Analytics Dashboard

An interactive sales analytics dashboard built using **Python, Pandas, Plotly and Streamlit** to analyze sales, profitability, customers, products, orders, shipping, discounts and business losses.

---

## 📌 Project Overview

The Superstore Sales Analytics Dashboard provides an interactive way to explore and analyze sales transaction data.

The dashboard allows users to filter the dataset by:

- Order Date
- Region
- State / Province
- Segment
- Category
- Sub-Category
- Ship Mode

All dashboard pages respond dynamically to the selected filters.

---

## 🎯 Business Objectives

The dashboard is designed to answer important business questions such as:

- What are the total sales and total profit?
- Which regions generate the highest sales?
- Which categories and sub-categories are most profitable?
- Which products generate the highest and lowest profits?
- How are sales and profit changing over time?
- Which customers generate significant revenue?
- Which orders are loss-making?
- What is the impact of discounts on profitability?
- Which shipping modes have the best shipping performance?
- Which products and categories require attention?

---

## 📊 Dashboard Pages

### 1. Executive Overview

Provides a high-level view of:

- Total Sales
- Total Profit
- Total Orders
- Total Quantity
- Profit Margin
- Sales by Region
- Sales by Category
- Profit by Category
- Monthly Sales and Profit
- Top Sub-Categories
- Top Products

---

### 2. Sales Analysis

Analyzes:

- Sales performance
- Regional sales
- Category sales
- Sub-category sales
- Product sales
- Customer sales
- Sales trends

---

### 3. Profitability Analysis

Analyzes:

- Total profit
- Profit margin
- Profit by category
- Profit by sub-category
- Profit by region
- Profit by segment
- Product profitability

---

### 4. Regional Analysis

Analyzes performance across geographical regions, states and cities.

---

### 5. Customer & Segment Analysis

Analyzes:

- Customer sales
- Customer profitability
- Segment performance
- Top customers
- Loss-making customers

---

### 6. Order Analysis

Analyzes order-level performance including sales, profit, quantity and order characteristics.

---

### 7. Shipping Analysis

Analyzes:

- Shipping days
- Shipping performance
- Ship modes
- Regional shipping performance
- Shipping trends
- Shipping impact on sales

---

### 8. Discount Analysis

Analyzes:

- Discount distribution
- Discount by category
- Discount by sub-category
- Discount by region
- Discount by segment
- Discount vs Sales
- Discount vs Profit
- Discount impact on profitability

---

### 9. Loss Analysis

Identifies:

- Loss-making orders
- Loss-making products
- Loss-making customers
- Loss by category
- Loss by sub-category
- Loss by region
- Loss by state
- Loss by city
- Discount vs Loss

---

### 10. Time Series Analysis

Analyzes:

- Monthly sales trends
- Monthly profit trends
- Order trends
- Sales growth
- Profit growth
- Yearly performance
- Monthly seasonality
- Category trends
- Regional trends

---

### 11. Product Analysis

Analyzes:

- Product sales
- Product profitability
- Product quantity
- Product discounts
- Top products
- Bottom products
- Category performance
- Sub-category performance
- Product-level details

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard application |
| Git / GitHub | Version control and project sharing |

---

## 🏗️ Project Structure

```text
Superstore_Dashboard/
│
├── app.py
├── check_data.py
├── requirements.txt
├── README.md
│
├── data/
│   └── sample_-_superstore.csv
│
├── pages/
│   ├── 02_Sales_Analysis.py
│   ├── 03_Profitability_Analysis.py
│   ├── 04_Regional_Analysis.py
│   ├── 05_Customer_Segment_Analysis.py
│   ├── 06_Order_Analysis.py
│   ├── 07_Shipping_Analysis.py
│   ├── 08_Discount_Analysis.py
│   ├── 09_Loss_Analysis.py
│   ├── 10_Time_Series_Analysis.py
│   └── 11_Product_Analysis.py
│
└── utils/
    ├── __init__.py
    ├── charts.py
    ├── data_loader.py
    ├── filters.py
    └── kpis.py