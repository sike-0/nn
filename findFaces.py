import threading
from mtcnn import MTCNN
from threading import Thread
import os
import cv2

os.chdir(os.path.dirname(os.path.abspath(__file__)))

IMGDIR = "imgs"
FACEDIR = "faces"

for dir in os.listdir(IMGDIR):
    os.makedirs(os.path.join(FACEDIR, dir), exist_ok=True)


def getFaceCoords(filepath: str) -> list | None:
    detector = MTCNN()
    result = detector.detect_faces(cv2.imread(filepath))
    return [res["box"] for res in result]


def crop_and_save(dir: str, file: str) -> None:
    filepath = os.path.join(IMGDIR, dir, file)
    filename = file.split(".")[0]
    faceCoords = getFaceCoords(filepath)
    for i, faceCoord in enumerate(faceCoords):
        [x, y, width, height] = faceCoord
        img = cv2.imread(filepath)
        face = img[y : y + height, x : x + width]
        face = cv2.resize(face, (160, 160))
        savepath = os.path.join(FACEDIR, dir, f"{filename}_face_{i}.jpg")
        cv2.imwrite(savepath, face)
        print(f"Done {savepath}")


def main():
    threads: list[Thread] = []
    for dir in os.listdir(IMGDIR):
        for file in os.listdir(os.path.join(IMGDIR, dir)):
            filename = file.split(".")[0]
            if (
                file.endswith(".jpg")
                or file.endswith("png")
                and not os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_1.jpg")
            ):
                thread = Thread(
                    target=crop_and_save,
                    args=(
                        dir,
                        file,
                    ),
                )
                thread.start()
                threads.append(thread)
                while len(threads) >= 6:
                    for t in threads:
                        if not t.is_alive():
                            t.join()
                            threads.remove(t)


if __name__ == "__main__":
    main()
