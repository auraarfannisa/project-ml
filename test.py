# -*- coding: utf-8 -*-
"""ML_Unsupervised_Kel7

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SGP9N0EkbDwHeJryTgSdhp59fj0Qmk5C

# 🤖 Customer Behavior Segmentation Analysis 💰

# 👯‍♀️ Anggota Kelompok: 👯‍♀️
1️⃣ Pujiani Rahayu Agustin - 24060122130067

2️⃣ Meyta Rizki Khairunisa - 24060122130085

3️⃣ Aura Arfannisa Az Zahra - 24060122130097

4️⃣ Nabila Betari Anjani - 24060122140169

# 📂 Eksplorasi Dataset 📂

# 📚 Library yang Diperlukann
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
import re

"""# 1. Import & Load Dataset

a. Import dataset
"""

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('customer.csv')
print(df.size)

"""b. Lima baris awal dari dataset"""

df.head()

"""c. Eksplorasi baris & kolom, tipe data"""

df.info()

"""d. Eksplorasi missing values"""

df.isnull().sum()

"""e. Eksplorasi data duplikat"""

print(f"Jumlah duplikasi: {df.duplicated().sum()}")
df = df.drop_duplicates()

"""f. Statistik deskriptif dataset"""

df.describe()

"""g. Penghapusan kolom 'Number'"""

#Drop kolom number
df.drop(["Number"], axis=1, inplace=True)

print(df.columns)

"""# 2. Visualisasi Distribusi Variabel Numerik

a. Visualisasi distribusi data menggunakan histogram
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Daftar variabel yang ingin diplot
variables = ['Age', 'Income', 'Spending_Score', 'Membership_Years', 'Purchase_Frequency', 'Last_Purchase_Amount']

# Cek apakah kolom-kolom ada di dalam DataFrame
for var in variables:
    if var in df.columns:
        print(f"Menampilkan distribusi untuk kolom: {var}")

        # Cek tipe data kolom
        if pd.api.types.is_numeric_dtype(df[var]):
            # Menghapus NaN sebelum plotting
            df[var].dropna(inplace=True)

            # Membuat plot histogram dengan KDE
            sns.histplot(df[var], kde=True, bins=30)
            plt.title(f'Distribusi {var}')
            plt.show()
        else:
            print(f"Kolom {var} bukan tipe numerik.")
    else:
        print(f"Kolom {var} tidak ditemukan dalam dataset.")

"""b. Visualisasi distribusi outlier menggunakan boxplot"""

df.plot(kind='box',
                       subplots=True,
                       layout=(6, 3),  # Ubah layout agar lebih besar dari jumlah fitur
                       sharex=False,
                       sharey=False,
                       figsize=(15, 20))  # Ukuran gambar lebih besar untuk tampilan jelas

plt.tight_layout()
plt.show()

"""c. Visualisasi matriks korelasi menggunakan heatmap"""

# Scaling data (pastikan semua kolom ada)
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_cleaned[numerical_columns]), columns=numerical_columns)

# Matriks korelasi
correlation_matrix = df_scaled.corr()

# Menampilkan matriks korelasi dengan lebih banyak desimal
print("=== Matriks Korelasi ===")
print(correlation_matrix.round(4))  # Membulatkan ke 4 desimal

# Visualisasi dengan lebih banyak desimal
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.4f', linewidths=0.5)  # Format 4 desimal
plt.title('Matriks Korelasi antar Variabel')
plt.show()

# Memeriksa kolom yang hilang
missing_columns = [col for col in numerical_columns if col not in df_scaled.columns]
print("Kolom yang hilang:", missing_columns)

"""# 3. Analisis Korelasi Antarfitur dalam Dataset

Berdasarkan matriks korelasi pada diaggram heatmap di atas, dapat ditarik kesimpulan bahwa:
"""

import pandas as pd

# Data hubungan korelasi antar fitur
data = {
    'Fitur': ['Income', 'Age', 'Spending_Score', 'Purchase_Frequency', 'Membership_Years', 'Last_Purchase_Amount'],
    'Berkorelasi Dengan': [
        'Age, Last_Purchase_Amount, Spending_Score',
        'Income, Last_Purchase_Amount, Spending_Score',
        'Age, Income, Last_Purchase_Amount',
        'Membership_Years',
        'Purchase_Frequency',
        'Age, Income, Spending_Score'
    ]
}

# Membuat DataFrame dari data
correlation_table = pd.DataFrame(data)

# Menampilkan tabel korelasi
correlation_table

"""Jika dibagi menjadi 2 cluster, maka hasil dari korelasi antarfitur tersebut adalah:"""

import pandas as pd

# Data kelompok dan fitur yang berkorelasi
data = {
    'Principal Component': ['PC1 (Variasi Ekonomi)', 'PC2 (Dimensi Waktu Membership)'],
    'Fitur': [
        'Income, Age, Last_Purchase_Amount, Spending_Score',
        'Membership_Years, Purchase_Frequency'
    ],
    'Keterangan': [
        'Pelanggan dengan pendapatan lebih tinggi mungkin juga memiliki skor belanja yang lebih tinggi atau melakukan pembelian lebih sering',
        'Pelanggan yang lebih lama menjadi anggota mungkin lebih sering melakukan pembelian'
    ]
}

# Membuat DataFrame dari data
group_table = pd.DataFrame(data)

# Menampilkan tabel kelompok
group_table

"""# 4. Dimensionality Reduction

a. Outlier handling
"""

# 2. Outlier Detection dan Handling menggunakan IQR method
def handle_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Replace outliers with bounds
    df[column] = np.where(df[column] > upper_bound, upper_bound,
                         np.where(df[column] < lower_bound, lower_bound, df[column]))
    return df

# Columns untuk outlier handling
numerical_columns = ['Age', 'Income', 'Spending_Score', 'Membership_Years',
                    'Purchase_Frequency', 'Last_Purchase_Amount']

for column in numerical_columns:
    df = handle_outliers(df, column)

df.plot(kind='box',
                       subplots=True,
                       layout=(6, 3),  # Ubah layout agar lebih besar dari jumlah fitur
                       sharex=False,
                       sharey=False,
                       figsize=(15, 20))  # Ukuran gambar lebih besar untuk tampilan jelas

plt.tight_layout()
plt.show()

"""b. Standarisasi data

# 5. Principal Component Analysis (PCA)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Fungsi untuk menganalisis korelasi antar fitur
def analyze_correlations(correlation_matrix, threshold=0.7):
    # Mencari pasangan fitur dengan korelasi tinggi
    high_correlations = []

    # Iterasi untuk setiap pasangan fitur
    for i in range(len(correlation_matrix.columns)):
        for j in range(i + 1, len(correlation_matrix.columns)):
            correlation = abs(correlation_matrix.iloc[i, j])
            if correlation > threshold:
                high_correlations.append({
                    'Feature 1': correlation_matrix.columns[i],
                    'Feature 2': correlation_matrix.columns[j],
                    'Correlation': correlation
                })

    # Mengubah hasil menjadi DataFrame dan mengurutkan berdasarkan nilai korelasi
    results_df = pd.DataFrame(high_correlations)
    if not results_df.empty:
        results_df = results_df.sort_values('Correlation', ascending=False)

    return results_df

# Skalakan data
scaler = StandardScaler()
df_scaled = df_cleaned.copy()
df_scaled[numerical_columns] = scaler.fit_transform(df_cleaned[numerical_columns])

# Matriks korelasi antar fitur
correlation_matrix = df_scaled[numerical_columns].corr()

# Menganalisis korelasi dengan threshold 0.7
correlations = analyze_correlations(correlation_matrix, threshold=0.7)

print("\nPasangan fitur dengan korelasi tinggi:")
print(correlations.to_string(index=False))

# Mengidentifikasi kelompok fitur yang berkorelasi
print("\nKelompok fitur yang saling berkorelasi:")

# Menentukan ambang batas korelasi
threshold = 0.9

# Dictionary untuk menyimpan hubungan korelasi
correlation_relationships = {}

# Identifikasi fitur redundan dan hubungan korelasi antar fitur
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > threshold:
            colname_1 = correlation_matrix.columns[i]
            colname_2 = correlation_matrix.columns[j]

            # Menyimpan fitur yang berkorelasi dalam bentuk set untuk menghindari duplikasi
            if colname_1 not in correlation_relationships:
                correlation_relationships[colname_1] = set()
            correlation_relationships[colname_1].add(colname_2)

            if colname_2 not in correlation_relationships:
                correlation_relationships[colname_2] = set()
            correlation_relationships[colname_2].add(colname_1)

# Menampilkan hasil hubungan korelasi
for feature, correlated_features in correlation_relationships.items():
    correlated_features_list = ', '.join(sorted(correlated_features))
    print(f"{feature}\t->\t{correlated_features_list}")

# PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(df_scaled[numerical_columns])

# Buat DataFrame baru dengan hasil PCA
pca_data = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Buat DataFrame komponen utama
components_df = pd.DataFrame(pca.components_, columns=df_scaled[numerical_columns].columns, index=['PC1', 'PC2'])

# Menampilkan nama kolom penyusun setiap komponen utama
print("\nKomponen Penyusun untuk PC1 dan PC2:")
for i, row in components_df.iterrows():
    print(f"Komponen penyusun {i}:")
    # Filter fitur dengan kontribusi signifikan (threshold 0.2)
    contributing_features = row.index[row.abs() > 0.2]
    # Menampilkan nama kolom
    print(", ".join(contributing_features))  # Gabungkan nama kolom dengan koma
    print()

"""**Analisis:**

**Komponen penyusun PC1: Age, Income, Spending_Score, Last_Purchase_Amount**

1. Kelompok fitur ini saling berkorelasi satu sama lain. Misalnya, Income berhubungan erat dengan Age, Last_Purchase_Amount, dan Spending_Score

2. Menunjukkan bahwa pelanggan dengan pendapatan lebih tinggi mungkin juga memiliki skor belanja yang lebih tinggi atau melakukan pembelian lebih sering.

**Komponen penyusun PC2: Membership_Years, Purchase_Frequency**

1. Fitur dalam kelompok ini memiliki korelasi yang jelas satu sama lain, di mana Membership_Years berhubungan dengan Purchase_Frequency.
2. Menunjukkan bahwa pelanggan yang lebih lama menjadi anggota mungkin lebih sering melakukan pembelian
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Menampilkan missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Visualisasi distribusi variabel income, spending score, dan last purchase amount
variables = ['Income', 'Spending_Score', 'Last_Purchase_Amount']
for var in variables:
    sns.histplot(df[var], kde=True, bins=30)
    plt.title(f'Distribusi {var}')
    plt.show()

# Scatter plot antar variabel untuk melihat pola
sns.pairplot(df[variables])
plt.title('Pairplot antar variabel')
plt.show()

# Normalisasi data menggunakan StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[variables])

# Konversi kembali ke DataFrame untuk kemudahan analisis
df_scaled = pd.DataFrame(df_scaled, columns=variables)

# Lakukan PCA untuk mereduksi dimensi
pca = PCA(n_components=2)  # Mengambil 2 komponen utama
df_pca = pca.fit_transform(df_scaled)

# Plotting variansi yang dijelaskan oleh tiap komponen
explained_variance = pca.explained_variance_ratio_
print("\nExplained Variance Ratio PCA:", explained_variance)

plt.figure(figsize=(8, 6))
plt.bar(range(1, 3), explained_variance, alpha=0.7, align='center', label='Individual Explained Variance')
plt.step(range(1, 3), np.cumsum(explained_variance), where='mid', label='Cumulative Explained Variance')
plt.title('Explained Variance by Principal Components')
plt.xlabel('Principal Components')
plt.ylabel('Explained Variance Ratio')
plt.legend(loc='best')
plt.show()

# Konversi hasil PCA ke DataFrame
df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2'])

# Menentukan jumlah cluster optimal menggunakan metode Elbow pada data PCA
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_pca)
    inertia.append(kmeans.inertia_)

# Plot Elbow Method
plt.plot(k_range, inertia, 'bo-')
plt.title('Elbow Method untuk Menentukan Jumlah Cluster (PCA)')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Inertia')
plt.show()

# Menentukan jumlah cluster optimal menggunakan Silhouette Score pada data PCA
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_pca)
    score = silhouette_score(df_pca, kmeans.labels_)
    silhouette_scores.append(score)

# Plot Silhouette Score
plt.plot(range(2, 11), silhouette_scores, 'bo-')
plt.title('Silhouette Score untuk Menentukan Jumlah Cluster (PCA)')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Silhouette Score')
plt.show()

# Memilih jumlah cluster optimal (misalnya, k=3 berdasarkan Elbow dan Silhouette Score)
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
df['cluster'] = kmeans.fit_predict(df_pca)

# Visualisasi hasil clustering berdasarkan principal components
sns.scatterplot(x=df_pca['PC1'], y=df_pca['PC2'], hue=df['cluster'], palette='Set1')
plt.title('Hasil Clustering dengan PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='Cluster')
plt.show()

# Menampilkan jumlah data pada tiap cluster
print("\nJumlah Data pada Tiap Cluster:")
print(df['cluster'].value_counts())

# Analisis cluster
print("\nStatistik Tiap Cluster:")
print(df.groupby('cluster')[variables].mean())