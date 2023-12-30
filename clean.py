import os

# Directory structure:
# imgs/
#   - site1
#       - person1/
#           - image1.jpg
#           - image2.jpg
#       - person2/
#           - image1.jpg
#           - image2.jpg
#   - site2
#       - person1/
#           - image1.jpg
#           - image2.jpg
#       - person2/
#           - image1.jpg
#           - image2.jpg
# this is an example, there can be more than 2 levels of nesting

# Directory structure required:
# imgs/
#   - person1/
#       - image1.jpg
#       - image2.jpg
#   - person2/
#       - image1.jpg
#       - image2.jpg
# but output should also be:
# imgs/
#   - person1/ (or directory name that actually contains images)
#       - image1.jpg
#       - image2.jpg
#   - person2/ (or directory name that actually contains images)
#       - image1.jpg
#       - image2.jpg
# this is because the directory name is used as the label for the images


IMGDIR = "imgs"

# convert to the required directory structure
for dir, subdirs, files in os.walk(IMGDIR):
    if len(subdirs) == 0:
        continue
    for subdir in subdirs:
        for file in os.listdir(os.path.join(dir, subdir)):
            os.rename(os.path.join(dir, subdir, file), os.path.join(dir, file))
        os.rmdir(os.path.join(dir, subdir))

os.makedirs("useless", exist_ok=True)

for dir in os.listdir(IMGDIR):
    for file in os.listdir(f"{IMGDIR}/{dir}"):
        if not file.endswith(".jpg"):
            os.rename(f"{IMGDIR}/{dir}/{file}", f"useless/{file}")
