# 📊 Power BI - Superstore - Executive Business Intelligence Dashboard 

## 📌 Overview
This repository contains a **multi-page executive Business Intelligence dashboard** built in **Microsoft Power BI**, using the Superstore dataset.

The project is designed as a **portfolio-grade BI solution**, combining:
- Executive-level storytelling
- Strong analytical modeling
- Well-structured DAX measures
- Clear documentation for reproducibility and review

Because the Power BI tenant may expire, the dashboard is documented using **PDF exports and high-resolution screenshots** instead of live links.

---

## 🧭 Dashboard Structure

### Pages Included
1. **Executive Overview**
2. **Customer Intelligence**
3. **Discount & Profitability**
4. **Operations & Logistics**

Each page is designed around a **clear business question**, following enterprise BI best practices.

---

## 📄 Full Dashboard (PDF)
📎 **[Download PDF](pdf/Power%20BI%20Dashboard%20-%20Superstore.pdf)**

## 📊 Full Dashboard (PBIX)
📎 **[Download PBIX](pdix/Power%20BI%20Dashboard%20-%20Superstore.pbix)**

## 🧮 Dataset
📎 **[Access Superstore Dataset](../../../datasets/superstore/)**

---

## 🖼 Dashboard Pages & Business Logic

### Page 1 — Executive Overview
🎯 Business Question

“How is the business performing overall?”

### KPIs
- Total Sales
- Total Profit
- Profit Margin %
- Total Orders
- Average Order Value (AOV)
- Orders with Loss

### Key Visuals
- Monthly Sales & Profit trend
- Top profitable sub-categories
- Geographic sales distribution

### Design & Technical Notes
- Profit shown alongside Sales to expose margin erosion
- Negative values intentionally highlighted
- KPIs act as context indicators, not filters

### Executive Overview
![Executive Overview](assets/screenshots/executive-overview.gif)

### Page 2 — Customer Intelligence
🎯 Business Question

“Who drives revenue, and how concentrated is it?”

### KPIs
- Unique Customers
- Orders per Customer
- Top Customer Sales %
- Top 10 Customers Sales %

### Key Visuals
- Top Customers by Sales
- Customer Segment Mix (100% stacked)
- Concentration indicators (Top customer contribution)

### Design & Technical Notes
- TOPN logic used for ranking customers
- Combined absolute ($) and relative (%) labels
- Segment mix intentionally normalized (100%) to avoid scale bias

### Customer Intelligence
![Customer Intelligence](assets/screenshots/customer-intelligence.gif)

### Page 3 — Discount & Profitability
🎯 Business Question

“Are discounts helping or harming profitability?”

### KPIs
- Average Discount %
- Discounted Sales
- Profit with Discount
- Profit without Discount
- Orders with Loss

### Key Visuals
- Profit with vs without Discount (monthly)
- Profit by Discount Band
- Discount Bands: 0%, 0–10%, 10–20%, 20–30%, 30%+
- Loss drivers by Sub-Category

### Design & Technical Notes
- Discount bands implemented via calculated column
- Negative profit deliberately shown to avoid misleading visuals
- Sorting enforced via measure-based ordering (not alphabetic)

### Discount & Profitability
![Discount & Profitability](assets/screenshots/discount-profitability.gif)

### Page 4 — Operations & Logistics
🎯 Business Question

“Are we operationally efficient?”

### KPIs
- Average Shipping Days
- Total Shipped Orders

### Key Visuals
- Shipping Days by Ship Mode
- Monthly Shipping Days Trend
- Detailed Shipping Table (inspection only)

### Design & Technical Notes
- Tables do not cross-filter other visuals
- Trend visuals cross-highlight instead of filtering
- Focus on operational signal, not SLA enforcement

### Operations & Logistics
![Operations & Logistics](assets/screenshots/operations-logistics.gif)

---

## 🧱 Data Model
This project intentionally uses a **single-table analytical model**, as commonly done for lightweight Power BI portfolio projects.

### Model Diagram
![Model Diagram](assets/diagrams/Power%20BI%20Dashboard%20-%20Superstore.png)

---

## 🧮 Measures Documentation (DAX)

### Total Sales
```DAX
Total Sales =
SUM ( Orders[Sales] )
```


### Total Profit
```DAX
Total Profit =
SUM ( Orders[Profit] )
```

### Profit Margin %
```DAX
Profit Margin % =
DIVIDE ( [Total Profit], [Total Sales] )
```

### Total Orders
```DAX
Total Orders =
DISTINCTCOUNT ( Orders[Order ID] )
```

### Average Order Value (AOV)
```DAX
Average Order Value =
DIVIDE ( [Total Sales], [Total Orders] )
```

### Orders with Loss
```DAX
Orders with Loss =
CALCULATE (
    DISTINCTCOUNT ( Orders[Order ID] ),
    Orders[Profit] < 0
)
```

---

### Unique Customers
```DAX
Unique Customers =
DISTINCTCOUNT ( Orders[Customer Name] )
```

### Orders per Customer
```DAX
Orders per Customer =
DIVIDE ( [Total Orders], [Unique Customers] )
```

---

### Top Customer Sales %
```DAX
Top Customer Sales % =
DIVIDE (
    MAXX (
        VALUES ( Orders[Customer Name] ),
        [Total Sales]
    ),
    [Total Sales]
)
```

### Top 10 Customers Sales %
```DAX
Top 10 Customers Sales % =
DIVIDE (
    CALCULATE (
        [Total Sales],
        TOPN (
            10,
            VALUES ( Orders[Customer Name] ),
            [Total Sales],
            DESC
        )
    ),
    [Total Sales]
)
```

---

### Discounted Sales
```DAX
Discounted Sales =
CALCULATE (
    [Total Sales],
    Orders[Discount] > 0
)
```

### Average Discount %
```DAX
Avg Discount % =
AVERAGE ( Orders[Discount] )
```

---

### Profit with Discount
```DAX
Profit w/ Discount =
CALCULATE (
    [Total Profit],
    Orders[Discount] > 0
)
```

### Profit without Discount
```DAX
Profit w/o Discount =
CALCULATE (
    [Total Profit],
    Orders[Discount] = 0
)
```

---

### Discount Band
```DAX
Discount Band =
VAR d = Orders[Discount]
RETURN
SWITCH (
    TRUE(),
    d = 0, "0%",
    d > 0 && d <= 0.10, "0–10%",
    d > 0.10 && d <= 0.20, "10–20%",
    d > 0.20 && d <= 0.30, "20–30%",
    "30%+"
)
```

---

### Average Shipping Days
```DAX
Avg Shipping Days =
AVERAGE ( Orders[Shipping Days] )
```





## 📐 Measures & Calculations

This section documents all DAX measures created in the **Superstore – Power BI Dashboard**, grouped by logical folders as defined in the model.  
Each measure is designed to be reusable, filter-aware, and optimized for analytical clarity.

---

### 🔹 Core KPIs

#### Total Sales
Total revenue generated from all orders.
```DAX
Total Sales =
SUM ( Orders[Sales] )
```
#### Total Profit
Net profit after costs and discounts.
```
Total Profit =
SUM ( Orders[Profit] )
```
#### Total Orders
Distinct count of orders.
```
Total Orders =
DISTINCTCOUNT ( Orders[Order ID] )
```
#### Average Order Value (AOV)
Average revenue per order.
```
Average Order Value =
DIVIDE ( [Total Sales], [Total Orders] )
```
#### Profit Margin %
Profit as a percentage of sales.
```
Profit Margin % =
DIVIDE ( [Total Profit], [Total Sales] )
```
#### Profit Status
Categorizes profit as Positive or Loss.
```
Profit Status =
IF ( [Total Profit] < 0, "Loss", "Profit" )
```
#### Total Profit Color
Color logic for KPI conditional formatting.
```
Total Profit Color =
IF (
    [Total Profit] < 0,
    "#E74C3C",   -- Red
    "#2ECC71"    -- Green
)
```
#### Profit Margin % Color
Color logic for margin visualization.
```
Profit Margin % Color =
IF (
    [Profit Margin %] < 0,
    "#E74C3C",
    "#2ECC71"
)
```

---

### 🔹 Customer Intelligence
Unique Customers

Number of distinct customers.

Unique Customers =
DISTINCTCOUNT ( Orders[Customer Name] )

Sales per Customer

Average sales generated per customer.

Sales per Customer =
DIVIDE ( [Total Sales], [Unique Customers] )

Orders per Customer

Average number of orders per customer.

Orders per Customer =
DIVIDE ( [Total Orders], [Unique Customers] )

Customer Sales %

Customer contribution relative to total sales.

Customer Sales % =
DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( Orders ) ) )

Top Customer Sales %

Sales share of the single top customer.

Top Customer Sales % =
DIVIDE (
    MAXX ( VALUES ( Orders[Customer Name] ), [Total Sales] ),
    CALCULATE ( [Total Sales], ALL ( Orders ) )
)

Top 10 Customers Sales

Total sales generated by the top 10 customers.

Top 10 Customers Sales =
CALCULATE (
    [Total Sales],
    TOPN (
        10,
        SUMMARIZE (
            Orders,
            Orders[Customer Name],
            "CustomerSales", [Total Sales]
        ),
        [Total Sales],
        DESC
    )
)

Top 10 Customers Sales %

Sales concentration of the top 10 customers.

Top 10 Customers Sales % =
DIVIDE ( [Top 10 Customers Sales], [Total Sales] )

Customer Label

Labels customers as Top 10 or Other.

Customer Label =
IF (
    RANKX (
        ALL ( Orders[Customer Name] ),
        [Total Sales],
        ,
        DESC
    ) <= 10,
    "Top 10 Customers",
    "Other Customers"
)

🔹 Discount & Profitability
Discounted Sales

Sales generated from discounted orders.

Discounted Sales =
CALCULATE (
    [Total Sales],
    Orders[Discount] > 0
)

Non-Discount Sales

Sales generated without discounts.

Non-Discount Sales =
CALCULATE (
    [Total Sales],
    Orders[Discount] = 0
)

Avg Discount %

Average discount applied across orders.

Avg Discount % =
AVERAGE ( Orders[Discount] )

Profit w/ Discount

Profit from discounted orders only.

Profit w/ Discount =
CALCULATE (
    [Total Profit],
    Orders[Discount] > 0
)

Profit w/o Discount

Profit from non-discounted orders.

Profit w/o Discount =
CALCULATE (
    [Total Profit],
    Orders[Discount] = 0
)

Profit w/ Discount Color

Conditional formatting for discounted profit.

Profit w/ Discount Color =
IF (
    [Profit w/ Discount] < 0,
    "#E74C3C",
    "#2ECC71"
)

Orders with Loss

Number of orders with negative profit.

Orders with Loss =
CALCULATE (
    DISTINCTCOUNT ( Orders[Order ID] ),
    Orders[Profit] < 0
)

Loss Rate %

Percentage of orders generating losses.

Loss Rate % =
DIVIDE ( [Orders with Loss], [Total Orders] )

🔹 Growth & Time Intelligence
Sales YTD

Year-to-date sales.

Sales YTD =
TOTALYTD ( [Total Sales], Orders[Order Date] )

Sales PY

Sales from the previous year.

Sales PY =
CALCULATE (
    [Total Sales],
    SAMEPERIODLASTYEAR ( Orders[Order Date] )
)

Sales YoY %

Year-over-year sales growth.

Sales YoY % =
DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )







---

## 🎛 Interaction & Design Principles
- Minimal slicers to avoid filter overload
- KPIs do not filter other visuals
- Charts cross-filter each other
- Tables used only for inspection
- Consistent formatting across pages
- Color used for meaning, not decoration

---

## 🗂 Repository Structure
```
superstore/
│
├─ assets/
│   ├─ diagrams/
│   │   └─ Power BI Dashboard - Superstore.png
│   │
│   └─ screenshots/
│       ├─ customer-intelligence.gif
│       ├─ discount-profitability.gif
│       ├─ executive-overview.gif
│       └─ operations-logistics.gif
│
├─ pdf/
│   └─ Power BI Dashboard - Superstore.pdf
│
├─ pdix/
│   └─ Power BI Dashboard - Superstore.pbix
│
└─ README.md
```

---

## 🎯 Purpose
This project demonstrates:
- Executive dashboard design
- Business-oriented analytics
- Strong DAX fundamentals
- Portfolio-quality BI documentation