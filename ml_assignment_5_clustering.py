# -*- coding: utf-8 -*-
"""ml ASSIGNMENT 5 CLUSTERING.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15XD5PKDUZLG3H8wDZ8E670fhLzRCXOTp

# Preprocessing
"""

#  Import necessary libraries
import pandas as pd

import numpy as np

from sklearn.datasets import load_iris

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.preprocessing import StandardScaler

# Load the dataset
iris = load_iris()


df = pd.DataFrame(iris.data, columns=iris.feature_names)
print(df.isnull().sum())
df['target'] = iris.target

# Drop the target/label column
df_clean = df.drop('target', axis=1)


# Scale the features
scaler = StandardScaler()

X_scaled = scaler.fit_transform(df_clean)

"""# KMeans"""

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Apply KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans_labels = kmeans.fit_predict(X_scaled)


print("Cluster Centers:\n", kmeans.cluster_centers_)

"""### What is KMeans Clustering?

KMeans is a popular clustering method that divides data into K groups, where each group is centered around a point called a centroid.

Here’s how it works:

    Pick K random points as initial centroids.

    Assign each data point to the closest centroid (based on distance).

    Recalculate the centroids based on the new clusters.

    Repeat steps 2 and 3 until the clusters stop changing.

KMeans works well when the data forms round, evenly sized clusters, which is true for the Iris dataset. Since it’s clean and balanced with 3 natural groups (based on flower species), KMeans is a great fit.
"""

# Reduce dimensions to 2D for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot KMeans clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=kmeans_labels, palette='viridis', s=100)
plt.title('KMeans Clustering on Iris (PCA-reduced)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

from sklearn.metrics import silhouette_score
print("Silhouette Score (KMeans):", silhouette_score(X_scaled, kmeans_labels))

"""# Hierarchical Clustering

**What is Hierarchical Clustering?**

Hierarchical clustering is a method of grouping data into a tree-like structure. It starts with each point as its own cluster and gradually merges the closest ones based on distance until everything forms one big cluster.

    You can visualize this merging process using a dendrogram, which helps you decide how many clusters to keep by “cutting” it at a certain height.

    One great thing about this method is that you don’t need to decide the number of clusters in advance.

    It's a good fit for the Iris dataset because it's small (150 samples) and well-structured, making the merging process both efficient and meaningful.
"""

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# Compute linkage matrix
linkage_matrix = linkage(X_scaled, method='ward')

# Plot dendrogram
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix, truncate_mode='level', p=5)
plt.title("Dendrogram for Iris Dataset (Hierarchical Clustering)")
plt.xlabel("Sample index")
plt.ylabel("Distance")
plt.grid(True)
plt.show()

hier_labels = fcluster(linkage_matrix, t=3, criterion='maxclust')

# PCA for 2D plot
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=hier_labels, palette='Set1', s=100)
plt.title("Hierarchical Clustering on Iris (PCA-reduced)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

from sklearn.metrics import silhouette_score
print("Silhouette Score (Hierarchical):", silhouette_score(X_scaled, hier_labels))

"""## Final Conclusion

- Both **KMeans** and **Hierarchical Clustering** worked well on the Iris dataset, discovering 3 natural groupings that align closely with the known species.
- KMeans produced slightly better-defined clusters based on the **Silhouette Score (0.46)**, while hierarchical clustering came close with **0.45**.
- The PCA plots show that both methods formed meaningful clusters, especially KMeans, where the boundaries between groups were more distinct.
- Hierarchical clustering gave extra insight through the **dendrogram**, helping visualize how clusters were merged step-by-step.
- Overall, the Iris dataset was a great fit for both techniques due to its structure and size, and each method provided unique interpretability.

"""