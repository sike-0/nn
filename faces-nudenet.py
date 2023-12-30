import threading
from contourpy import max_threads
from nudenet import NudeDetector
from threading import Thread
import os
import cv2

os.chdir(os.path.dirname(os.path.abspath(__file__)))

IMGDIR = "imgs"
FACEDIR = "faces-nudenet"

# Test with 20 images
MAX_IMAGES = 20

# Directory structure:
# imgs/
#   - person1/
#       - image1.jpg
#       - image2.jpg
#   - person2/
#       - image1.jpg
#       - image2.jpg
# faces/
#   - person1/
#       - image1.jpg
#       - image2.jpg
#   - person2/
#       - image1.jpg
#       - image2.jpg

for dir in os.listdir(IMGDIR):
    os.makedirs(os.path.join(FACEDIR, dir), exist_ok=True)


def getFaceCoord(filepath: str) -> list | None:
    detector = NudeDetector()
    coords = detector.detect(filepath)
    for coord in coords:
        if coord["class"] == "FACE_FEMALE":
            return coord["box"]
    return None


def crop_and_save(dir: str, file: str) -> None:
    filepath = os.path.join(IMGDIR, dir, file)
    savepath = os.path.join(FACEDIR, dir, file)
    faceCoord = getFaceCoord(filepath)
    if faceCoord:
        [x1, y1, x2, y2] = faceCoord
        img = cv2.imread(filepath)
        face = img[y1 : y2 + y1, x1 : x2 + x1]
        face = cv2.resize(face, (160, 160))
        cv2.imwrite(savepath, face)
    print(f"Done {savepath}")


def main():
    threads: list[Thread] = []
    count = 0
    for dir in os.listdir(IMGDIR):
        for file in os.listdir(os.path.join(IMGDIR, dir)):
            if (
                file.endswith(".jpg")
                or file.endswith("png")
                and not os.path.exists(os.path.join(FACEDIR, dir, file))
                and count < MAX_IMAGES
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
                            count += 1


if __name__ == "__main__":
    main()
