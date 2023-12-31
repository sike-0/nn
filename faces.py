# Final faces file: faces.py
# Saves cropped faces from images in imgs/ to faces/ directory.

from threading import Thread
from retinaface import RetinaFace
import os
import cv2

import sys

import logging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm


os.chdir(os.path.dirname(os.path.abspath(__file__)))

IMGDIR = "imgs"
FACEDIR = "faces"
LOGFILE = "error.log"

for dir in os.listdir(IMGDIR):
    if os.path.isdir(os.path.join(IMGDIR, dir)):
        os.makedirs(os.path.join(FACEDIR, dir), exist_ok=True)

# Configure the logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def getFaceCoords(imgPath: str) -> list | None:
    result = RetinaFace.extract_faces(imgPath)
    if len(result) == 0:
        return None
    return result


def crop_and_save(dir: str, file: str) -> None:
    filepath = os.path.join(IMGDIR, dir, file)
    filename = file.split(".")[0]
    faces = getFaceCoords(filepath)
    if faces:
        for i, face in enumerate(faces):
            face = cv2.resize(face, (160, 160))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            savepath = os.path.join(FACEDIR, dir, f"{filename}_face_{i}.jpg")
            cv2.imwrite(savepath, face)
            LOG.info(f"Done {savepath}")
    else:
        LOG.info(f"No face in {filepath}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "colab":
        MAX_THREADS = 10
    else:
        MAX_THREADS = 3
    LOG.info(f"Using {MAX_THREADS} threads")
    threads: list[Thread] = []
    for dir in os.listdir(IMGDIR):
        if os.path.isdir(os.path.join(IMGDIR, dir)):
            files = os.listdir(os.path.join(IMGDIR, dir))
            with logging_redirect_tqdm():
                progress_bar = tqdm(
                    files, desc=f"Processing {dir}", leave=False, position=0
                )
                for file in files:
                    filename = file.split(".")[0]
                    if os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_0.jpg"):
                        LOG.info(
                            f"{FACEDIR}/{dir}/{filename}_face_0.jpg exists skipping"
                        )
                    if (
                        file.endswith(".jpg") or file.endswith("png")
                    ) and not os.path.exists(f"{FACEDIR}/{dir}/{filename}_face_0.jpg"):
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
                                    progress_bar.update(1)
        else:
            if os.path.exists(f"{FACEDIR}/{dir}_face_0.jpg"):
                LOG.info(f"{FACEDIR}/{dir}_face_0.jpg exists skipping")
            if (dir.endswith(".jpg") or dir.endswith("png")) and not os.path.exists(
                f"{FACEDIR}/{dir}_face_0.jpg"
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
