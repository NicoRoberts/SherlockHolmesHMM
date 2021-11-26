# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 17:04:25 2021

@author: Nicol
"""

#Nicolas Roberts
#8/13/21
#TCSS 435
#Assignment 3

import Markov
import random

#Driver of the program
def main():
    inputBook1 = "stud.txt"
    inputBook2 = "sign.txt"
    
    
    model = Markov.TrigramMarkovModel()
    
    #test = 1, actual 0
    text1 = getText(inputBook1, 0)
    text2 = getText(inputBook2, 0)
    
    sentenceList1 = cleanText(text1)
    sentenceList2 = cleanText(text2)
    
    sentenceList1 = removeSpaces(sentenceList1)
    sentenceList2 = removeSpaces(sentenceList2)
    
    print("\n\nTraining Markov Model...\n\n")
    
    hashSentence(sentenceList1, model, True)
    hashSentence(sentenceList2, model, False)
    
    hashTable = model.getHashTable()
    
    print("\n\nTraining complete\nGenerating Story...\n")
    
    generateStory(model, hashTable)
    
    print("done. See generated README.txt")
    
def generateStory(theModel, theHashTable):
    outF = open("Readme.txt", "w")
    firstWordList = ["in", "sherlock"] #starting word will be one of the starting words from either book
    randomIndex = random.randint(0, 1)
    
    currentWords = 0
    maxWords = 2000
    
    firstWord = firstWordList[randomIndex] #change to randomIndex later
    outF.write(firstWord + " ")
    #print(firstWord + " ")
    currentWords+=1
    
    secondWord = theModel.computeHighestBigram(theHashTable, firstWord)
    outF.write(secondWord + " ")    
    #print(secondWord + " ")
    currentWords+=1
    
    thirdWord = theModel.computeHighestTrigramSingle(theHashTable, firstWord, secondWord)
    outF.write(thirdWord + " ") 
    #print(thirdWord)
    currentWords+=1
    
    
    
    wordMinusTwo = secondWord
    wordMinusOne = thirdWord
    #find current word and update
    while(currentWords <= maxWords):
        state = theModel.getNewPhraseState()
        nextWord = theModel.computeHighestTrigram(theHashTable, wordMinusTwo, wordMinusOne, state)
        outF.write(nextWord + " ") 
        #print(nextWord)
        currentWords+=1
        
        wordMinusTwo = wordMinusOne
        wordMinusOne = nextWord
        
        if (currentWords % 20 == 0):
            outF.write("\n")
    
    outF.close()
    
    
    
def hashSentence(theSentenceList, theModel, firstSentence):
    for sentence in theSentenceList:
        theModel.hash(sentence, firstSentence)
        firstSentence = False
    
def getText(theFileName, test):
    file = open(theFileName, 'r')
    if (test == 1):
        lines = file.readlines()
        testText = ""
        for i in range(0, 20):
            if (i > 7): #skip preliminary book title author etc.
                if (lines[8] == ""):
                    continue
                else:
                    testText = testText + lines[i]
        
        return testText.lower()
                
    else:
        lines = file.readlines()
        text = ""
        for i in range(0, len(lines)):
            if (i > 7): #skip preliminary book title author etc.
                if (lines[8] == ""):
                    continue
                else:
                    text = text + lines[i]
        
        return text.lower() #return lower case text
        
    file.close()
    
def removeSpaces(theSentenceList):
    for i in range(0, len(theSentenceList)): #each sentence
        currentSentence = theSentenceList[i].split(" ")
        index = 0
        for j in range(0, len(currentSentence)):
            if(currentSentence[index] == ""):
                currentSentence.remove(currentSentence[index])
            else:
                index += 1
                
        theSentenceList[i] = " ".join(currentSentence)
    
    return theSentenceList
        

    
def cleanText(theText):
    splitText = theText.split('.')
    
    for i in range(0, len(splitText)):
        splitText[i] = removePunctuation(splitText[i])
        
    return splitText
    

# Python program to remove punctuation from a given string
# Function to remove punctuation
# From GEEKSFORGEEKS
def removePunctuation(string):
 
    # punctuation marks
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
 
    # traverse the given string and if any punctuation
    # marks occur replace it with null
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
 
    return string

main() #call to execute the program
    