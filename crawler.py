import webdev
import os
import json
import math

global queue
global searchedPages
global pageCount
global urlFile
global fruitList
global isCleaned
isCleaned = False
pageCount = 0
queue = []
searchedPages = []
urlFile = {}
fruitList = []

def crawl(seed):
    global pageCount
    global fruitList
    global isCleaned

    #removes previous scrape data on first iteration if previous scraped data is found
    #NOTE: does not work at all if any modifications to files and name are done outside of this code and the rest of the program doesn't work if the directory isn't a clean slate
    if isCleaned is False and os.path.isfile("urls.json"):
        f = open("urls.json", "r")
        tempUrls = json.load(f)
        f.close()
        for url in tempUrls:
            fileList = os.listdir(tempUrls[url])
            for file in fileList:
                filePath = os.path.join(tempUrls[url], file)
                os.remove(filePath)
            os.rmdir(tempUrls[url])
            isCleaned = True

    href = []
    fruits = {}
    currentPage = webdev.read_url(seed)
    if len(queue) > 0:
        queue.pop(0)

    #basic text splits and getting title
    currentPage.lower()
    words = currentPage.split()
    titleSection = words[0].split(">")
    title = titleSection[3].replace("</title", "")

    # counting # of fruits
    for i in range(1, len(words)):
        if words[i] == "</p>":
            endPoint = i
            break
        if words[i] not in fruits:
            fruits[words[i]] = 1
        else:
            fruits[words[i]] += 1
        if words[i] not in fruitList:
            fruitList.append(words[i])

    #getting word count of document
    wordCount = 0
    for fruit in fruits:
        wordCount += fruits[fruit]

    #getting the href tag
    counter = 0
    for i in range(endPoint+1, len(words)):
        if words[i] == "<a" or words[i] == "</body></html>":
            continue
        link = words[i].split("\"")
        href.append(link[1])
        href[counter] = (href[counter])[2: : ]
        counter += 1

    #create file and associate name with the url
    directName = str(pageCount)
    urlFile[seed] = str(pageCount)
    pageCount += 1
    os.makedirs(directName)

    #writing down term frequency of fruits in a file
    for fruit in fruits:
        filePath = os.path.join(directName, fruit)
        fruitFile = open(filePath, "w")
        fruitFile.write(str((fruits[fruit]) / wordCount))
        fruitFile.close()

    #write down current url in a file
    filePath = os.path.join(directName, "url")
    url = open(filePath, "w")
    url.write(seed)
    url.close()

    #write down current title in a file
    filePath = os.path.join(directName, "title")
    titleFile = open(filePath, "w")
    titleFile.write(title)
    titleFile.close()

    # set up link to write down urls add current url
    link = (seed.split("/"))
    for i in range(len(link)-1):
        link[i] += "/"

    #add link for seed url
    if link not in searchedPages:
        searchedPages.append("".join(link))

    #write down outgoing links then set up queue and searched pages
    filePath = os.path.join(directName, "outgoingLinks")
    outgoingFile = open(filePath, "w")
    for i in range(len(href)):
        link[len(link)-1] = (href[i])
        newUrl = "".join(link)

        outgoingFile.write(newUrl + "\n")

        if (newUrl) not in searchedPages:
            queue.append(newUrl)
            searchedPages.append(newUrl)
    outgoingFile.close()



    #continue crawling untill queue is empty
    if len(queue) > 0:
        crawl(queue[0])

    #data sorting once crawling is done
    else:
        isCleaned = False
        #set up incoming links
        for url in urlFile:
            filePath = os.path.join(urlFile[url], "outgoingLinks")
            outgoingFile = open(filePath, "r")
            outgoingUrls = outgoingFile.readlines()
            outgoingFile.close()
            for outUrl in outgoingUrls:
                filePath = os.path.join(urlFile[outUrl.strip()], "incomingLinks")
                incomingFile = open(filePath, "w")
                incomingFile.write(url + "\n")
                incomingFile.close()

        #set up idf


        idf = {}
        fruitFile = open("fruits", "w")
        for fruit in fruitList:
            counter = 0
            for url in urlFile:
                fileList = os.listdir(urlFile[url])
                if fruit in fileList:
                    counter += 1
            idf[fruit] = math.log(((pageCount) / (counter+1)), 2)
            fruitFile.write(fruit+"\n")
        fruitFile.close()

        #set up tfidf
        for url in urlFile:
            fileList = os.listdir(urlFile[url])
            for file in fileList:
                if file in fruitList:
                    filePath = os.path.join(urlFile[url], (file+"tfidf"))
                    fruitIdf = open(filePath, "w")
                    filePath = os.path.join(urlFile[url], file)
                    fruitTf = open(filePath, "r")
                    tf = float(fruitTf.read())
                    fruitIdf.write(str(math.log(1+tf, 2) * idf[file]))
                    fruitIdf.close()
                    fruitTf.close()

        #dump tfidf and the file link associations in jsons
        idfJson = json.dumps(idf)
        idfFile = open("idf.json", "w")
        idfFile.write(idfJson)
        idfFile.close()

        urlJson = json.dumps(urlFile)
        jsonFile = open("urls.json", "w")
        jsonFile.write(urlJson)
        jsonFile.close()








#crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
