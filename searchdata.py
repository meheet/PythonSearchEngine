import os
import json

def get_outgoing_links(URL):
    f = open("urls.json", "r")
    fileList = json.load(f)
    f.close()
    if URL not in fileList:
        return None
    filePath = os.path.join(fileList[URL], "outgoingLinks")
    outgoingFile = open(filePath, "r")
    outgoingLinks = outgoingFile.readlines()
    for i in range(len(outgoingLinks)):
        outgoingLinks[i] = outgoingLinks[i].replace("\n", "")
    return outgoingLinks


def get_incoming_links(URL):
    f = open("urls.json", "r")
    fileList = json.load(f)
    f.close()
    if URL not in fileList:
        return None

    filePath = os.path.join(fileList[URL], "incomingLinks")
    incomingFile = open(filePath, "r")
    incomingLinks = incomingFile.readlines()
    for i in range(len(incomingLinks)):
        incomingLinks[i] = incomingLinks[i].replace("\n", "")
    return incomingLinks

def get_idf(word):
    word = word.lower()
    f = open("idf.json", "r")
    idf = json.load(f)
    f.close()
    if word in idf:
        return idf[word]
    return 0

def get_tf(URL, word):
    word = word.lower()
    f = open("urls.json", "r")
    fileList = json.load(f)
    f.close()
    if URL not in fileList:
        return 0

    fruitList = os.listdir(fileList[URL])
    if word in fruitList:
        filePath = os.path.join(fileList[URL], word)
        if os.path.exists(filePath) is False:
            return 0
        f = open(filePath, "r")
        tf = f.read()
        f.close()
        return float(tf)
    return 0

def get_tf_idf(URL, word):
    word = word.lower()
    f = open("urls.json", "r")
    fileList = json.load(f)
    f.close()
    if URL not in fileList:
        return 0

    fruitList = os.listdir(fileList[URL])
    if word in fruitList:
        filePath = os.path.join(fileList[URL], word+"tfidf")
        if os.path.exists(filePath) is False:
            return 0
        f = open(filePath, "r")
        tfidf = f.read()
        f.close()
        return float(tfidf)
    return 0

print(get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N.html"))
