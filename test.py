from nudenet import NudeDetector
import multiprocessing
import os

DIR = "imgs"


def process_image(image):
    detector = NudeDetector()
    coordinates = detector.detect(f"{DIR}/{image}")

    if len(coordinates) == 0:
        os.remove(f"{DIR}/{image}")
        print(image)
        return

    face = False
    for coord in coordinates:
        if coord["label"] == "FACE_F":
            face = True
            break

    if not face:
        os.remove(f"{DIR}/{image}")
        print(image)
        return


def main():
    # use os.walk to get all files in subdirectories and create at max 4 processes
    processes = []
    for root, dirs, files in os.walk(DIR):
        for file in files:
            if file.endswith(".jpg"):
                process = multiprocessing.Process(target=process_image, args=(file,))
                process.start()
                processes.append(process)

                if len(processes) == 4:
                    for process in processes:
                        process.join()
                    processes = []


if __name__ == "__main__":
    main()
