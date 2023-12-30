import pickle
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

embeddings = pickle.load(open("embeddings-umap.pkl", "rb"))
embeddings = np.array(embeddings)
print(embeddings.shape)

x = [i for i in embeddings[:, 0]]
y = [i for i in embeddings[:, 1]]

plt.scatter(x, y)
plt.show()
