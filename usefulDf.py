import pandas as pd

class UsefulDataFrame:

    def __init__(self, imageWLabels):
        self.imageWLabels = imageWLabels

    def makeDf(self):

        imgLabels2= []
        for image in self.imageWLabels:
            imgDict = {
                "name" : image["name"]
            }
            text = ""

            for ind, label in enumerate(image["labels"]):
                multiplyer = label.score * 10
                text+=(label.description + " ") * round(multiplyer)
                imgDict["Label{}".format(ind)] = label.description
                imgDict["LabelScore{}".format(ind)] = label.score

            imgDict["LabelDesc"] = text
            imgLabels2.append(imgDict)

        newDF = pd.DataFrame(imgLabels2)
        return newDF

if __name__ == "__main__":
    usefulDf = UsefulDataFrame(imageWLabels)
    newDF = usefulDf.makeDf()
