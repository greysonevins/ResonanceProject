import boto3
from io import BytesIO
from tqdm import tqdm
import json
import os

bucket = "devhw"

class GetAmazonImages:

    def __init__(self, bucket, access_id="AKIAJPHCTAP7PDA2NHZA", access_key="3/gbbW+zVkw7su8Jggc2IRFLoAq0bH12qyioWiPG"):
        try:
            with open("aws_keys.json") as f:
                self.jsonKeys = json.loads(f.read())
        except Exception as e:
            print(e)
            print("need aws_keys.json file")

        self.bucket = bucket
        self.s3 = boto3.client("s3", aws_access_key_id=self.jsonKeys["access_id"], aws_secret_access_key=self.jsonKeys["access_key"])

    def getImages(self):
        listPictures = [ key["Key"] for key in self.s3.list_objects(Bucket=bucket)["Contents"]]
        imagesFinal = []
        for image in tqdm(listPictures):
            d = self.s3.get_object(Bucket=bucket, Key=image)

            bytesImg = BytesIO(d["Body"].read())

            imgDictVal = {"name": image,
                          "image": bytesImg}

            imagesFinal.append(imgDictVal)
        return imagesFinal


if __name__ == "__main__":
    getImages = GetAmazonImages("devhw")
    imagesFinal = getImages.getImages()
