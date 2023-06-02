import os
import math
import json
import searchdata

def search(phrase, boost):
    f = open("urls.json", "r")
    urls = json.load(f)
    urlList = []
    queryTfid = []

    phrase = phrase.lower()
    fruitOrder = phrase.split(" ")
    #remove duplicates from list
    fruitOrder = list(set(fruitOrder))

    for fruit in fruitOrder:
        queryTfid.append(math.log(1+(1/len(fruitOrder)), 2) * searchdata.get_idf(fruit))

    for i in range(-1, len(queryTfid)-1):
        if queryTfid[i] == 0:
            queryTfid.remove(queryTfid[i])
            fruitOrder.remove(fruitOrder[i])


#    print(queryTfid)
    #print(fruitOrder)
    for url in urls:
        result = {}
        dataTfid = []
        result["url"] = url

        filePath = os.path.join(urls[url], "title")
        titleFile = open(filePath, "r")
        title = titleFile.readline()
        result["title"] = title

        for fruit in fruitOrder:
            dataTfid.append(searchdata.get_tf_idf(url, fruit))

        numerator = 0
        dataSquared = 0
        querySquared = 0
        for i in range(-1, len(queryTfid)-1):
            numerator += (dataTfid[i]*queryTfid[i])
            dataSquared += dataTfid[i]**2
            querySquared += queryTfid[i]**2

        if dataSquared == 0:
            score = 0
        else:
            score = (numerator/((dataSquared**0.5)*(querySquared**0.5)))
        result["score"] = score

        urlList.append(result)
    return urlList



print(search("coconut coconut orange blueberry lime lime lime tomato", False))
