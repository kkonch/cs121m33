import bisect
import os
from itertools import combinations





def insert_into_sorted_list(sorted_list, item):
    bisect.insort(sorted_list, item, key=lambda x: x[1])
    return sorted_list


#returns and sorts ased on frequency - returns medianvalues first
def searchIndex(tokens:list):
    #print(tokens)
    returnDict = {}
    returnArr = []
    #2d array - each row is list of indexes per token
    notLast = True
    file = open('report.txt', 'r')
    while notLast:
        curTok = tokens.pop(0)
        found = False
        notEnd = True
        #checkign if at end of index
        while (not found) and notEnd:
            thisLine = file.readline()
            if (thisLine == ""):
                notEnd = False
            else:
                thisLine = thisLine.split(" : ")
                if thisLine[0] == curTok:
                    found = True
                    indList = thisLine[2][1:-2]
                    
                    indList = [int(a) for a in indList.split(", ")]
                    if len(indList) > 10:
                        indList = indList[:10]
                    #print(indList)
                    returnArr = insert_into_sorted_list(returnArr, (indList, int(thisLine[1])) )
                    returnDict[curTok] = set(indList)
        
        
        if len(tokens) == 0 or (not notEnd):
            notLast = False
    returnArr = [x[0] for x in sort_by_proximity_to_median(returnArr)]
    #print(returnArr)
    return (returnArr, returnDict)


def sort_by_proximity_to_median(lst):
    
    # Calculate the median
    #assuming lst is sorted
    n = len(lst)
    if (n <=1):
        return lst
    halfPoint = n//2
    median = lst[halfPoint][1] if n % 2 != 0 else (lst[halfPoint - 1][1] + lst[halfPoint][1]) / 2
    # Sort the list based on absolute differences from the median
    lst.sort(key=lambda x: -1 * abs(x[1] - median))
    return lst

def intersect(listA, listB, hist:set):
    returnL =  [x for x in listA if (x not in hist) and (x in listB)]
    
    return returnL

def get_combinations(lst):
    all_combinations = []
    for r in range(1, len(lst) + 1):
        combinations_r = list(combinations(lst, r))
        all_combinations.extend([list(combination) for combination in combinations_r])
    return all_combinations[::-1]

def orderResults(combinations):
    hist= set()
    returnList = []
    
    for combo in combinations:
        i = len(combo) -1 
        #print(y)
        j = i-1
        temp = [x for x in combo[i] if x not in hist]
        while j >=0:
            res = intersect(temp, combo[j], hist)
            temp = res
            j-=1
        for x in temp:
            hist.add(x)
        returnList.extend(temp)
            
    return returnList


def indexesToUrls(URL_List, indexes):

    return [URL_List[i] for i in indexes]


def booleanSearch(qeuery:list, URLIndexList ):
    searchIndexReturn = searchIndex(qeuery)
    searchIndexDict = searchIndexReturn[1]
    searchIndexReturn = searchIndexReturn[0]
    # finalL = []
    # for l in searchIndexReturn:
    #     finalL.extend(l)
    gc = get_combinations(searchIndexReturn)
    orderedRes = orderResults(gc)
    finalList = indexesToUrls(URLIndexList, orderedRes)
    # finalList = indexesToUrls(URLIndexList, finalL)
    return finalList


