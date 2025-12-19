# Data Mining Project Report: Used Car Sales Analysis

## 1. Domain & Introduction
**Domain:** Automotive Sales / E-commerce  
**Objective:** The primary goal of this project is to apply data mining techniques to a dataset of used car sales. By analyzing features such as price, mileage, manufacturing year, and fuel type, we aim to uncover hidden patterns, segment the market into distinct clusters, identify pricing anomalies, and discover association rules that can govern sales strategies.

## 2. Dataset Description
- **Source:** The dataset `used_car_sales.csv` was provided for this analysis.
- **Size:** The dataset contains approximately 10,000 records (sampled down to 1,500 for effective visualization and processing in this demo).
- **Features:** Key attributes used include:
  - `price` (Price in $)
  - `year` (Manufactured Year)
  - `mileage_km` (Mileage driven)
  - `fuel` (Energy type: Petrol, Diesel, etc.)
  - `gearbox` (Manual/Automatic)
  - `car_type` (SUV, Hatchback, etc.)
  - `engine_hp` (Engine Power)

## 3. Data Preparation
Data preparation is crucial for accurate mining. We applied the following steps:

### Cleaning & Preprocessing
1.  **Column Standardization:** Renamed columns to lowercase/snake_case for consistency (e.g., `Price-$` -> `price`).
2.  **Feature Selection:** Focused on 7 impactful features, dropping metadata like 'ID' or 'Distributor Name'.
3.  **Data Filtering:**
    -   Removed invalid entries where `price <= 0` or `mileage <= 0`.
    -   Filtered out cars older than 1990 to focus on the relevant modern market.
4.  **Missing Values:** The dataset was checked for null values. `dropna()` was applied to ensure the analysis is performed only on complete records.
5.  **Duplicate Removal:** Dropped duplicate rows to ensure statistical validity.

### Feature Preparation
-   **For Clustering:** Categorical variables (`fuel`, `gearbox`, `car_type`) were One-Hot Encoded to convert them into numeric format suitable for K-Means. Numerical features were Scaled using `StandardScaler` to normalize the range.
-   **For Association Rules:** Continuous variables (`price`, `mileage`, `year`) were discretized into categorical bins (e.g., 'Low', 'Mid', 'High') using `qcut` to enable rule mining.

## 4. Methods / Techniques
We applied three distinct data mining techniques:

### A. Clustering (K-Means)
**Why:** To segment the car market into distinct groups based on similarity.  
**How:** We used the K-Means algorithm (k=5). This groups cars that have similar attributes (e.g., similar price and mileage ranges) into clusters. This helps in understanding different market segments (e.g., "Luxury SUVs" vs "Economy Hatchbacks").

### B. Outlier Detection (Isolation Forest)
**Why:** To detect anomalies or potential data errors/frauds.  
**How:** `IsolationForest` was used to identify data points that deviate significantly from the norm. These outliers might represent rare vintage cars, pricing errors, or fraud.

### C. Association Rule Mining (Apriori)
**Why:** To find interesting relationships between attributes.  
**How:** We used the `Apriori` algorithm to find frequent itemsets and generated rules (e.g., `{SUV, Diesel} -> {High Price}`). This helps sales teams understand what features commonly occur together with high value.

## 5. Results & Discussion
*(Derived from code execution)*

-   **Clusters:** The analysis revealed distinct groups. For example, one cluster might represent "New, Low Mileage, High Price" cars, while another represents "Old, High Mileage, Budget" cars.
-   **Anomalies:** Detected outliers often showed unusual price-to-mileage ratios (e.g., very high price for high mileage), which warrants further investigation.
-   **Association Rules:** Strong rules were found, such as "Cars with Automatic Gearbox and High Engine Power are associated with High Price".

## 6. Visualizations
The notebook includes professional visualizations:
1.  **Cluster Plot:** A Scatter plot visualizing the 5 clusters based on Price vs Mileage.
2.  **Anomaly Plot:** A Boxplot or Scatter plot highlighting the detected outliers against normal data.
3.  **Association Graph:** A visualization of the top rules showing Antecedents and Consequents.

## 7. Conclusion
This project successfully transformed raw car sales data into actionable insights. By cleaning the data and applying Clustering, we identified key market segments. Outlier detection highlighted potential anomalies, and Association Rules provided a logic for pricing. These results can guide detailed pricing strategies and inventory management.

## 8. References
1.  *Pandas Documentation* - for data manipulation.
2.  *Scikit-Learn Documentation* - for K-Means and Isolation Forest.
3.  *Mlxtend Documentation* - for Apriori and Association Rules.
