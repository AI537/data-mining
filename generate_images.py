
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")

try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False
    print("Mlxtend not found, skipping Association Rules plot.")

# Load and clean data
try:
    df = pd.read_csv("used_car_sales.csv")
    df.columns = df.columns.str.strip()
    # Sample for speed and consistency with report
    if len(df) > 2000:
        df = df.sample(n=2000, random_state=42)
    
    df = df[["Price-$", "Manufactured Year", "Mileage-KM", "Energy", "Gearbox", "Car Type", "Engine Power-HP"]]
    df.rename(columns={"Price-$": "price", "Manufactured Year": "year", "Mileage-KM": "mileage", "Energy": "fuel", "Gearbox": "gearbox", "Car Type": "car_type", "Engine Power-HP": "engine_hp"}, inplace=True)
    df = df[(df["price"] > 0) & (df["mileage"] > 0) & (df["year"] > 1990)]
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    # 1. Anomaly Plot
    iso = IsolationForest(contamination=0.05, random_state=42)
    df['outlier_status'] = iso.fit_predict(df[['price', 'mileage', 'year']])
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='mileage', y='price', hue='outlier_status', palette={1: 'blue', -1: 'red'})
    plt.title('Anomaly Detection: High Price outliers vs Mileage')
    plt.xlabel('Mileage (KM)')
    plt.ylabel('Price ($)')
    plt.legend(title='Status', labels=['Normal', 'Outlier'])
    plt.tight_layout()
    plt.savefig('anomaly_plot.png')
    plt.close()
    
    # Remove outliers for next steps
    df_clean = df[df['outlier_status'] == 1].drop('outlier_status', axis=1)
    
    # 2. Cluster Plot
    cluster_data = pd.get_dummies(df_clean, columns=['fuel', 'gearbox', 'car_type'], drop_first=True)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)
    kmeans = KMeans(n_clusters=5, random_state=42)
    df_clean['cluster'] = kmeans.fit_predict(scaled_data)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_clean, x='mileage', y='price', hue='cluster', palette='viridis', s=100)
    plt.title('Car Market Segmentation (5 Clusters)')
    plt.xlabel('Mileage (KM)')
    plt.ylabel('Price ($)')
    plt.legend(title='Cluster')
    plt.tight_layout()
    plt.savefig('cluster_plot.png')
    plt.close()
    
    # 3. Association Rules Plot (Only if library exists)
    if HAS_MLXTEND:
        ar_data = df_clean.copy()
        ar_data['price_bin'] = pd.qcut(ar_data['price'], q=3, labels=['Low Price', 'Mid Price', 'High Price'])
        ar_data['mileage_bin'] = pd.qcut(ar_data['mileage'], q=3, labels=['Low Mileage', 'Mid Mileage', 'High Mileage'])
        ar_data['year_bin'] = pd.cut(ar_data['year'], bins=[1990, 2010, 2018, 2025], labels=['Old', 'Modern', 'New'])
        basket = ar_data[['price_bin', 'mileage_bin', 'year_bin', 'fuel', 'gearbox', 'car_type']]
        basket_encoded = pd.get_dummies(basket)
        frequent_itemsets = apriori(basket_encoded, min_support=0.05, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
        price_rules = rules[rules['consequents'].astype(str).str.contains('Price')].head(15)
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=price_rules, x='support', y='confidence', size='lift', hue='lift', sizes=(100, 400))
        plt.title('Top Association Rules (Bubble Size = Lift)')
        plt.tight_layout()
        plt.savefig('association_plot.png')
        plt.close()

    print("Images generated successfully.")

except Exception as e:
    print(f"Error generating images: {e}")
