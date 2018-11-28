import io
import os
from PIL import Image

class CreateImageFiles:

    def __init__(self, imageWLabels):

        self.imageWLabels = []
        for imageData in imageWLabels:
            dirname = os.path.realpath("Images/")
            realName = "__".join(imageData["name"].split("/"))
            with open("{}/{}".format(dirname, realName), "wb") as file:
                file.write(imageData["image"])
            try:
                img = Image.open("{}/{}".format(dirname, realName))
                img.verify()
                if imageData["labels"]:
                    self.imageWLabels.append(imageData)
                else:
                    print("Image {} corrupted".format(imageData["name"]))
                    print("Will be rejected from analysis")
                    continue

            except Exception as e:
                print("Image {} corrupted".format(imageData["name"]))
                print("Will be rejected from analysis")
                continue

    def getNewDF(self):
        return self.imageWLabels

if __name__ == "__main__":
    usefulDf = UsefulDataFrame(imageWLabels)
    newDf = usefulDf.makeDf()
