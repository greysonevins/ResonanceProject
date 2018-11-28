# Greyson Resonance Companies Test

## Configure Requirements

Please use install requirements first to start project. All requirements should be saved to this environment but please use `python3 install -r requirements.txt` if issues arise.


## The file
To run project. run `python3 main.py`

1. Getting Data

  - `getImages.py`
    - This file streams the files from the S3 bucket into an array. I choose not to stream the data until the files are created to ensure that the bytes remain until needed in the Google process.
  - `getGoogleData.py`
    - This file takes the image data and uses Google Vision API to get labels for the images. (Slow) The only issue is that the Google Vision API is slow at responses. Some have recommended chunking, but first attempts at experimenting, I could not find an optimal number of chunks, so I wanted to leave this as is to ensure that it will work.

  - `createImageFiles.py`
    - This file saves the images locally so they can be used. Also, it makes sure that the images are valid and have image labels from Google. All images that are rejected will noted in the terminal.

  - `usefulDf.py`
    - In order to analyze the data, I transformed the compounded Google and Aws image data into a final DataFrame to be used in the next step.



2. Analyzing Data

  -  `analyzeData.py`
    - This file makes use of TfIdf and K-means to group images with similiar TfIdf vectorized labels. In order to do this, I took the Google labels and created a final string that contains the Google labels multiplied by the weight of the score. Next, I created a standard grouping of 10 groups. This could be changed if need by adjusting the `true_k` value. The K-means algorithm transforms the data into groupings by attempting to find the k-number of groups that you impose. For that reason, every iteration of it will produce a unique result, however, the final groups look pretty accurate.

    - the final output will be a graph of the k-means output and a new dataframe with labels for the ontology. While k-means provides a label of the k-groups, I added a label based on the closest feature to the centroid. The centroid image is based on the closest TfIdf transformed vector closest to the K-means centroid using the minimum euclidian distance for the groups. The presumed "centroid" then can be used a base image for the group and the base labels that comprise the group which I use in my output. You will see in the graph, that there is a bigger marker for the centroid.

3. Displaying Data

  - `createPages.py`

    - In order to make the new modeled information useful, I created a function that will create two html components: (1) a home page with the groupings and a link to the subgroups; and (2) subpages based on the k-number of labels. This is useful because the html will change and update based on the file input. When the file is done loading, the Selenium module should open a new Chrome Driver tab to show the new html. If this fails for some reason, please open the created file `htmlBoiler/htmlOut/finalLandingPage.html` in your browser. You will be able to view the graph and click into the subgrouped pages as well.

    - Thank you!
