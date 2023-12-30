from nudenet import NudeDetector
from threading import Thread
import os

DIR = "test"


# do this using threads
def process_image(image):
    print(image)
    detector = NudeDetector()
    coordinates = detector.detect(f"{DIR}/{image}")

    if len(coordinates) == 0:
        os.remove(f"{DIR}/{image}")
        return

    face = False
    for coord in coordinates:
        if coord["label"] == "FACE_F":
            face = True
            break

    if not face:
        os.remove(f"{DIR}/{image}")
        return


def main():
    threads = []
    for image in os.listdir(DIR):
        thread = Thread(target=process_image, args=(image,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
