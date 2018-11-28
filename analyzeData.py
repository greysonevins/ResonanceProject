from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib
matplotlib.use('PS')

import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances_argmin_min

class AnalyzeImageData:

    def __init__(self, newDF, true_k=10):
        #Error
        self.newDF = newDF
        self.vectorizer = TfidfVectorizer()
        self.true_k = true_k
        self.model = ""
        self.labelNames = {}
        self.labelVal = {}

    def modelML(self):
        #vectorizes labels
        self.X = self.vectorizer.fit_transform(self.newDF["LabelDesc"])

        self.model = KMeans(n_clusters=self.true_k, init='k-means++', max_iter=100, n_init=1)
        self.model.fit(self.X)

        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()

        for i in range(self.true_k):

            valueLabel = "_".join([terms[ind] for ind in order_centroids[i, :3]])
            self.labelNames[i] = valueLabel

            valueLabel = ", ".join([terms[ind] for ind in order_centroids[i, :10]])
            self.labelVal[i] = valueLabel

    def utlizeModel(self):

        self.newDF["Label"] = self.model.labels_
        self.newDF["LabelNew"] = self.newDF["Label"].apply(lambda num: self.labelNames[num])

        closest, _ = pairwise_distances_argmin_min(self.model.cluster_centers_, self.X)
        self.newDF["Centroid"] = self.newDF.index.to_series().apply(lambda num: True if num in closest else False)

        self.newDF["CentroidAttr"] = self.newDF["Label"].apply(lambda num: self.labelVal[num])

        return self.newDF


    def plotML(self):

        y_kmeans = self.model.labels_
        labels = list(set(y_kmeans))

        transformedVector = self.model.transform(self.X)
        centroidVal = self.model.transform(self.model.cluster_centers_)


        colorDict = {}

        for i, val in enumerate(plt.get_cmap("viridis", self.true_k).colors):
            colorDict[labels[i]] = val

        for i, types in enumerate(labels):
            indices = [i for i, typ in enumerate(y_kmeans) if typ == types]
            x = [transformedVector[i,0] for i in indices]
            y = [transformedVector[i,1] for i in indices]
            plt.scatter(x, y, s=50, color=colorDict[types], label=self.labelNames[types])


        centers = self.model.cluster_centers_

        plt.scatter(centroidVal[:, 0], centroidVal[:, 1], c='black', s=200, alpha=0.5, label="Centroid *")

        plt.legend(bbox_to_anchor=(1.1, 1.05))

        plt.tight_layout()

        plt.savefig("Figures/KMeansFig.png", dpi=500)

if __name__ == "__main__":
    analyze = AnalyzeImageData(newDF=newDF).modelML()
    newDF = analyze.utlizeModel()
    analyze.plotML()
