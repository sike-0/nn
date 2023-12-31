# Final faces file: faces.py
# Saves cropped faces from images in imgs/ to faces/ directory.

from threading import Thread
from retinaface import RetinaFace
import os
import cv2

import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

IMGDIR = "imgs"
FACEDIR = "faces"

for dir in os.listdir(IMGDIR):
    if os.path.isdir(os.path.join(IMGDIR, dir)):
        os.makedirs(os.path.join(FACEDIR, dir), exist_ok=True)


def getFaceCoords(image: cv2.typing.MatLike) -> list | None:
    result: dict = RetinaFace.detect_faces(image)
    return [result[key]["facial_area"] for key in result]


def crop_and_save(dir: str, file: str) -> None:
    filepath = os.path.join(IMGDIR, dir, file)
    filename = file.split(".")[0]
    img = cv2.imread(filepath)
    faceCoords = getFaceCoords(img)
    for i, faceCoord in enumerate(faceCoords):
        [x1, y1, x2, y2] = faceCoord
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        face = img[y1:y2, x1:x2]
        face = cv2.resize(face, (160, 160))
        savepath = os.path.join(FACEDIR, dir, f"{filename}_face_{i}.jpg")
        cv2.imwrite(savepath, face)
        print(f"Done {savepath}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "colab":
        MAX_THREADS = 20
    else:
        MAX_THREADS = 3
    threads: list[Thread] = []
    for dir in os.listdir(IMGDIR):
        if os.path.isdir(os.path.join(IMGDIR, dir)):
            for file in os.listdir(os.path.join(IMGDIR, dir)):
                filename = file.split(".")[0]
                if os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_0.jpg"):
                    print(f"{FACEDIR}/{dir}/{filename}_face_0.jpg exists skipping")
                if (
                    (file.endswith(".jpg")
                    or file.endswith("png"))
                    and not os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_0.jpg")
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
                    while len(threads) >= MAX_THREADS:
                        for t in threads:
                            if not t.is_alive():
                                t.join()
                                threads.remove(t)
        else:
            if os.path.exists(f"{FACEDIR}/{dir}_face_0.jpg"):
                print(f"{FACEDIR}/{dir}_face_0.jpg exists skipping")
            if (
                (dir.endswith(".jpg")
                or dir.endswith("png"))
                and not os.path.exists(f"{FACEDIR}/{dir}_face_0.jpg")
            ):
                thread = Thread(
                    target=crop_and_save,
                    args=(
                        ".",
                        dir,
                    ),
                )
                thread.start()
                threads.append(thread)
                while len(threads) >= MAX_THREADS:
                    for t in threads:
                        if not t.is_alive():
                            t.join()
                            threads.remove(t)


if __name__ == "__main__":
    main()
