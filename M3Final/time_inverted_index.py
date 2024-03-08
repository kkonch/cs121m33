#TODO
#: Make combinatiosn assing an id to each list of indexes, and return a list of them as sets so that searching is a tad more efficientt


import os
import json
from bs4 import BeautifulSoup
from tokenizer import tokenize, computeWordFrequencies, checkSumTwo
from  searchIndex import booleanSearch, topTen
import time



#os.listdir("/Users/kevinshihora/Downloads/DEV")

class HTMLProcessor:
    def __init__(self):
        self.count = 0
        #This is the final inveerted index
        self.masterDict = {}
        #self.rawDict = {}
        self.masterIndexList = []
        self.checkSumHist = set()

    def getAllFiles(self, pathname):
            #TODO CUt out bad encoding and non HTML Files or if no URL is provided
            #print('here')
            new_list = []
            i = 0
            all_directories = os.listdir(pathname)
            # Final List of directories to return
            finalList = []
            # Sub folders (organized by domains)
            for directory in all_directories:
                # DS store created by mac - removed here
                if(directory != '.DS_Store'):
                    # Get all files that are jsons and add their paths to the final list
                    # Uncomment Print i to get total files found
                    subDirFiles = os.listdir(pathname+"/"+directory)
                    for file in subDirFiles:
                        # if i == 152:
                        #     print(pathname+"/"+directory+"/"+file)
                        if '.json' in file:
                            # Check if processing time exceeds 40 seconds
                            file_size_mb = os.stat(pathname+"/"+directory+"/"+file).st_size / (1024 * 1024)
                            if file_size_mb > 15:
                                print(f"Skipping {file} in {directory} due to file being too large")
                                continue  # Skip to the next file
                            finalList.append(pathname+"/"+directory+"/"+file)
                            i += 1
                        else:
                            continue
                else:
                    pass
                    # print(pathname, directory)
            # print(i)
            return finalList
    

    def writeFinalIndexing(self, a_dict, filename):
        with open(filename, "w") as f:
            for x in sorted(a_dict):
                freq = [a[1] for a in a_dict[x]]
                freq = sum(freq)

                f.write(str(x) + " : " + str(freq) + " : " + 
                        str([a for a in sorted(a_dict[x], key = lambda x: x[1], reverse=True)] )
                         + "\n")
    
    def writeUrlIndexOrder(self, filename):
        with open(filename, "w") as f:
            i = 0
            
            while i < len(self.masterIndexList):
                if (i != len(self.masterIndexList) -1):
                    f.write(str(self.masterIndexList[i]) + "\t")
                else:
                    f.write(str(self.masterIndexList[i]))
                i +=1


    def readaFile(self, pathname):
        
        data = 0
        with open(pathname) as f:
            data = f.read()
        
        data = json.loads(data)
        url = data.get("url", "Invalid Url")
        encoding = data.get("encoding", 'NA')
        

        if (url == "Invalid Url") or encoding == 'NA':
            return None
        
        
        
        # print(urls)
        htmlfile = data["content"]
        firstChars = htmlfile[:15]
        if encoding == 'utf-8':
            if (firstChars != '<!DOCTYPE html>'):
                return None
        res = checkSumTwo(htmlfile, self.checkSumHist)
        if res[1] == True:
            return None
        else:
            self.checkSumHist = res[0]
        
        self.masterIndexList.append(url)
        self.count += 1
        print(self.count)
        #print(pathname)
        # if self.count == 152:
        #     #we get stuck on 152 because its hella long
        #     print(pathname)
        return htmlfile

    def addToIndex(self, html_content, fileIndex):
        
        soup = BeautifulSoup(html_content, 'html.parser')
        heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "title", "p"]
        # print(soup.prettify())
        thisDocDict = {}
        otherThisDocDict = {}
        numTotalTokens = 0
        tokenizeRes = []
        thisDocDict = {}


        weight = 1
            

        for tags in soup.find_all():
            #print(tags, end='')
            #content = tags.content
            for x in tags.children:
                #if ("<p>" in str(x) and "</p>" in str(x)):
                #  print(x)
                # #  print(thisDocDict)
                
                #  print(thisDocDict)
                if ("<h6>" in x and "</h6>" in x):
                    weight = 2
                elif ("<h5>" in x and "</h5>" in x):
                    weight = 3
                elif ("<h4>" in x and "</h4>" in x):
                    weight = 4
                elif ("<h3>" in x and "</h3>" in x):
                    weight = 5
                elif ("<h2>" in x and "</h2>" in x):
                    weight = 6
                elif ("<h1>" in x and "</h1>" in x):
                    weight = 7
                elif ("<title>" in x and "</title>" in x):
                    weight = 8
                else:
                    pass
            tokenizeRes = tokenize(tags.text.strip())
            #print('\n' + str(weight))
            numTotalTokens += len(tokenizeRes)
            thisDocDict = computeWordFrequencies(tokenizeRes, thisDocDict, weight)
            otherThisDocDict = computeWordFrequencies(tokenizeRes, otherThisDocDict, 1)
        
        for key, val in thisDocDict.items():
            if key not in self.masterDict:
                self.masterDict[key] = []
            #For future optimization append and sort at the same time so we save time - loop through current list until
                #you find where it should be appended and append at that index
            self.masterDict[key].append((fileIndex, val, otherThisDocDict[key]))

        return numTotalTokens


    #Simplified the calling so we can just do this
    def parse(self, path, writePath):
        file_list = self.getAllFiles(path)
        fIndex = 0
        for f in file_list:
            htmlText = self.readaFile(f)
            if (htmlText == None):
                continue
            else:
                res = self.addToIndex(htmlText, fIndex)
                self.masterIndexList.append(res)
                fIndex+=1
        self.writeFinalIndexing(self.masterDict, writePath)
        self.writeUrlIndexOrder("URLINDEX.txt")





# Test the function


if __name__ == "__main__":


    #IMAGINE THIS IS YOUR UI
    #before displaying anything do this bit first

    html = HTMLProcessor()
    
    
    html.parse("aTEstDev", "report.txt")

   

    #Then once above code is done prompt for qeuery and tokenize it
    #pass tokenizesed querey in alphabetical order into boolean search function with the url list to get final url list
    #in order




    
