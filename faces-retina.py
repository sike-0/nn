from threading import Thread
from retinaface import RetinaFace
import os
import cv2

os.chdir(os.path.dirname(os.path.abspath(__file__)))

IMGDIR = "imgs"
FACEDIR = "faces-retina"

for dir in os.listdir(IMGDIR):
    os.makedirs(os.path.join(FACEDIR, dir), exist_ok=True)


def getFaceCoords(image: cv2.typing.MatLike) -> list | None:
    result: dict = RetinaFace.detect_faces(image)
    # result output:
    #     {'face_1': {'score': 0.999447226524353,
    #   'facial_area': [218, 301, 372, 521],
    #   'landmarks': {'right_eye': [273.5159, 396.9055],
    #    'left_eye': [344.23557, 401.90427],
    #    'nose': [311.3778, 447.33206],
    #    'mouth_right': [270.64734, 472.3765],
    #    'mouth_left': [327.43912, 476.9867]}}}
    # get all facial_area in one list
    return [result[key]["facial_area"] for key in result]


def crop_and_save(dir: str, file: str) -> None:
    filepath = os.path.join(IMGDIR, dir, file)
    filename = file.split(".")[0]
    img = cv2.imread(filepath)
    faceCoords = getFaceCoords(img)
    for i, faceCoord in enumerate(faceCoords):
        [x1, y1, x2, y2] = faceCoord
        face = img[y1:y2, x1:x2]
        face = cv2.resize(face, (160, 160))
        savepath = os.path.join(FACEDIR, dir, f"{filename}_face_{i}.jpg")
        cv2.imwrite(savepath, face)
        print(f"Done {savepath}")


def main():
    threads: list[Thread] = []
    count = 0
    for dir in os.listdir(IMGDIR):
        for file in os.listdir(os.path.join(IMGDIR, dir)):
            filename = file.split(".")[0]
            if (
                file.endswith(".jpg")
                or file.endswith("png")
                and not os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_1.jpg")
                and count < 100
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
                while len(threads) >= 3:
                    for t in threads:
                        if not t.is_alive():
                            t.join()
                            threads.remove(t)
                            count += 1


if __name__ == "__main__":
    main()
