import os
import cv2
from keras_facenet import FaceNet
import pickle
import numpy as np
import umap

os.chdir(os.path.dirname(os.path.abspath(__file__)))

FACEDIR = "faces"

embedder = FaceNet()

embeddings = []
imgs = []
stats = {}

for dir in os.listdir(FACEDIR):
    imgFiles = os.listdir(os.path.join(FACEDIR, dir))
    stats[dir] = len(imgFiles)
    for file in imgFiles:
        if file.endswith(".jpg"):
            img = cv2.imread(f"{FACEDIR}/{dir}/{file}")
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.astype("float32")
            img = img.reshape(160, 160, 3)
            imgs.append(img)

imgs = np.array(imgs)
embeddings = np.array(embedder.embeddings(imgs)).reshape(-1, 512)
print(embeddings.shape)

reducer = umap.UMAP(n_components=2)
embedding = reducer.fit_transform(embeddings)
print(embedding.shape)

pickle.dump(embeddings, open("embeddings.pkl", "wb"))
pickle.dump(embedding, open("embeddings-umap.pkl", "wb"))
with open("stats.txt", "w") as f:
    for dir in stats:
        f.write(f"{dir}: {stats[dir]}\n")
    f.close()
