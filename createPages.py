import bs4
import pandas as pd
import numpy as np
import os



class CreateLandingPage:

    def __init__(self, clusterDf):
        self.centroids = clusterDf[clusterDf.Centroid == True]
        self.clusterDf = clusterDf

    def makePages(self):
        boilerPage = self.createBoilerSoup("htmlBoiler/visualHome.html")

        for key, row in self.centroids.iterrows():


            boilerSoup = self.createBoilerSoup("htmlBoiler/classifedGroup.html")

            boilerCard = self.addChanges(boilerSoup, row)

            linkSubPage = self.createSubPage(row["LabelNew"]) #return link

            link = boilerCard.find("a")
            link.attrs["href"] = linkSubPage

            addCard = boilerPage.find("div", attrs={"id":"rowGroups"})
            addCard.append(boilerCard)

        with open(os.path.realpath("htmlBoiler/htmlOut/finalLandingPage.html"), "wb") as file:
            file.write(boilerPage.encode("utf-8"))


        for subpage in self.centroids.LabelNew.values:
            subCluster = self.clusterDf[self.clusterDf.LabelNew == subpage]
            fileHtml = os.path.realpath("htmlBoiler/htmlOut/{}.html".format(subpage))
            soupSubPage = self.createBoilerSoup(fileHtml)

            for key, row in subCluster.iterrows():
                cardHtml = self.createBoilerSoup("htmlBoiler/classifiedImage.html")

                divAdd = soupSubPage.find("div", {"id":"rowGroups"})

                subImage = self.addChangesSubPage(cardHtml, row)

                divAdd.append(subImage)

            with open(fileHtml, "wb") as file:
                file.write(soupSubPage.encode("utf-8"))

    def createSubPage(self, subName):
        soup = self.createBoilerSoup("htmlBoiler/subPage.html")
        with open(os.path.realpath("htmlBoiler/htmlOut/{}.html".format(subName)), "wb") as subPage:
            h1 = soup.find("h1", "display-4")
            h1.string = "Label Group {}".format(subName)
            subPage.write(soup.encode("utf-8"))

        return os.path.realpath("htmlBoiler/htmlOut/{}.html".format(subName))

    def createBoilerSoup(self, fileName):
        with open(os.path.realpath(fileName)) as bImg:
            html = bImg.read()
            soup = bs4.BeautifulSoup(html, features="html.parser")
        return soup


    def addChanges(self, cardHtml, row):
        imageSrc = os.path.realpath("Images/{}".format(self.nameReal(row["name"])))
        img = cardHtml.find("img","card-img-top")
        img.attrs["src"] = imageSrc

        title = cardHtml.find("h5", "card-title")
        title.string = row["LabelNew"]


        p = cardHtml.find("p", "card-text")
        p.string = row["CentroidAttr"]

        return cardHtml


    def addChangesSubPage(self, cardHtml, row):
        imageSrc = os.path.realpath("Images/{}".format(self.nameReal(row["name"])))
        img = cardHtml.find("img","card-img-top")
        img.attrs["src"] = imageSrc

        title = cardHtml.find("h5", "card-title")
        title.string = row["name"]

        columns = [label for label in row.keys().values if "LabelScore" in label]


        link = cardHtml.find("a", attrs={"href":"#collapseExample"})
        link.attrs["href"] = "#{}_collapse".format(self.nameReal(row["name"]))
        link.attrs["aria-controls"] = "{}_collapse".format(self.nameReal(row["name"]))

        link = cardHtml.find("div", attrs={"id":"collapseExample"})
        link.attrs["id"] = "{}_collapse".format(self.nameReal(row["name"]))


        for column in columns:
            score = row[column]
            if not np.isnan(score):
                attribute = row[column.replace("Score", "")]
                newP = bs4.BeautifulSoup("<p><b>{}</b> : {} </p>".format(attribute, score), features="html.parser")
                pAdd = cardHtml.find("div", attrs={"class": "card card-body"})
                pAdd.append(newP)

            else:
                break

        return cardHtml


    @staticmethod
    def nameReal(name):
        newName = name.replace("/", "__")
        return newName




if __name__ == "__main__":
    cl = CreateLandingPage(newDF)
    cs.makePages()
