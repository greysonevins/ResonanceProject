from getImages import GetAmazonImages
from getGoogleData import GetGoogleVisionData
from usefulDf import UsefulDataFrame
from createImageFiles import CreateImageFiles
from analyzeData import AnalyzeImageData
from createPages import CreateLandingPage
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
import time

class ResonanceImageOntology:

    def run(self):
        print("=== Process 1 Start ==== ")
        print(" == Getting Amazon Images ==")
        print()
        getAmazonData = GetAmazonImages("devhw")
        imagesFinal = getAmazonData.getImages()
        print("Process 1 Complete")
        print("\n\n")

        print("=== Process 2 Start ==== ")
        print(" == Getting Google Vision Data ==")

        googleVision = GetGoogleVisionData(imagesFinal)
        imageWLabels = googleVision.getImageData()

        print("Process 2 Complete")
        print("\n\n")

        print("=== Process 3 Start ==== ")
        print(" == Saving Images and Creating DataFrame ==")

        createImageFiles = CreateImageFiles(imageWLabels)
        imageWLabels = createImageFiles.getNewDF()
        usefulDf = UsefulDataFrame(imageWLabels)
        newDF = usefulDf.makeDf()



        print("Process 3 Complete")
        print("\n\n")

        print("=== Process 4 Start ==== ")
        print(" == Analyzing Image Data with K-means and TfIdf ==")
        analyze = AnalyzeImageData(newDF=newDF)
        analyze.modelML()
        newDF = analyze.utlizeModel()
        newDF.to_csv("Data/finalDf.csv", index=False)
        analyze.plotML()


        print("Process 4 Complete")
        print("\n\n")

        print("=== Process 5 Start ==== ")
        print(" == Creating HTML from Data to Visualize ==")

        createPages = CreateLandingPage(newDF)
        createPages.makePages()

        print("Process 5 Complete")
        print("\n\n")

        print("=== Opening HTML File ===")
        chrome_options = Options()

        chrome_options.binary_location = ""
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)

        path = os.path.realpath("htmlBoiler/htmlOut/finalLandingPage.html")
        driver.get("file:///{}".format(str(path)))
        time.sleep(1000)
        driver.close()
        print()


if __name__ == "__main__":
    ResonanceImageOntology().run()
