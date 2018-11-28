from google.cloud import vision
from google.oauth2 import service_account
from google.cloud.vision import types
from tqdm import tqdm

class GetGoogleVisionData:
    def __init__(self, imagesFinal, creds="Thesis Work-f25bd7346f27.json"):
        self.credentials = service_account.Credentials.from_service_account_file(creds)
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)
        self.imagesFinal = imagesFinal

    def getImageData(self):
        imageWLabels = []

        for imageData in tqdm(self.imagesFinal):
            img = imageData["image"].read()

            try:
                image = types.Image(content=img)
                # Performs label detection on the image file
                response = self.client.label_detection(image=image)
                labels = response.label_annotations
                imageDict = {
                    "name"   : imageData["name"],
                    "image"  : img,
                    "labels" : labels

                }
                imageWLabels.append(imageDict)
            except Exception as e:
                print(e)
                print("This Image will be disregarded: {}".format(imageData["name"]))
        return imageWLabels

if __name__ == "__main__":
    googleVision = GetGoogleVisionData(imagesFinal)
    imageWLabels = googleVision.getImageData()
