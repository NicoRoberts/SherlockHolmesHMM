# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 17:03:58 2021

@author: Nicol
"""

#Nicolas Roberts
#8/13/21
#TCSS 435
#Assignment 3

#THe data structure in question shall be a dictionary, where each unique word maps to a list.

#NOT UP TO DATE
#Inside the list index 0 represents a deque (LinkedList) filled with words that appeared at position W^(i-1)
#Inside the list index 1 represents a deque (LinkedList) filled with words that appeared at position W^(i-2)

from collections import deque #deque acts as a linkedList with same runtimes for lookups.
import operator
import random

class TrigramMarkovModel:
    def __init__(self):
        self.myHashTable = {}
        self.myWordList = []
        self.index = 0
        
        self.phraseUsed = []
        self.newPhraseState = 0
        #0 Normal in not in list, start cycle if it is by returning random word
        #1 return bigram
        #2 return trigram single
        
        #process of debugging the sentences
        
    def hash(self, theText, firstSentence):
        theText = theText.replace("\n", "")
        wordList = theText.split(" ")
        
        if(len(wordList) == 1):
            if(wordList[0] == ''):
                del wordList[0]
            else:
                wordList.append(".") #period acts as its own word
        else:
            wordList.append(".") #period acts as its own word
        
        wordList = self.removeSpaces(wordList)
        self.myWordList = self.myWordList + wordList 
        
        if(firstSentence):
                self.index += 2 #skip putting the first two words as keys in the hashtable
                
        while(self.index < len(self.myWordList)):
            word = self.myWordList[self.index - 2]               
            if (word not in self.myHashTable.keys()): #add word as a key
                
                #dictionary to hold w^(i - 1) as key as w^(i) as value
                wordMinusOne = {}
                currentWordList = deque()
                
                frequencyCounter = {}
                frequencyCounter[self.myWordList[self.index]] = 1
                currentWordList.append(frequencyCounter)          
                wordMinusOne[self.myWordList[self.index - 1]] = currentWordList #key is the middle word in the block of three mapping to the current word w^i
                
                #print(currentWordList)
                
                
                container = wordMinusOne #container to hold 1 items
                #wordMinusOne is the dictionary that maps the middle word to a list of words w(i)
                #currentWordFrequency is the list of dictionaries that maps the words at w(i) to the frequency in the doc.
                
                self.myHashTable[word] = container
                
            else: #word is already a key in the hashtable
                container = self.myHashTable[word] #list of two dictionaries
                
                wm1Map = container
                
                
                potentialKey = self.myWordList[self.index - 1]
                
                if (potentialKey not in wm1Map.keys()):
                    currentWordList = deque()
                    
                    frequencyCounter = {}
                    frequencyCounter[self.myWordList[self.index]] = 1
                    currentWordList.append(frequencyCounter)
                    wm1Map[potentialKey] = currentWordList #add it as a key
                    
                   # print(currentWordList)
                    
                    #update hash table
                    container = wm1Map
                    self.myHashTable[word] = container
                
                else: #potential key exisits in word minus 1 map
                    #get value
                    currentWordsList = wm1Map[potentialKey] #a list
                    currentWordsDict = currentWordsList[0]
                    #print(currentWordsDict)
                    #check if current word w is in the currentWords List
                    if(self.myWordList[self.index] in currentWordsDict.keys()):
                        value = currentWordsDict[self.myWordList[self.index]]
                        value+=1
                        currentWordsDict[self.myWordList[self.index]] = value
                        
                        #print(currentWordsDict)
                        #update
                        currentWordsList[0] = currentWordsDict
                        wm1Map[potentialKey] = currentWordsList
                        #print(wm1Map)
                        
                    else: #not in the freq dictionary
                        currentWordsDict[self.myWordList[self.index]] = 1
                        #update currentWordsList
                       # print(currentWordsDict)
                        currentWordsList[0] = currentWordsDict
                        wm1Map[potentialKey] = currentWordsList
                       # print(wm1Map)
                    
                    #update hash table
                    container = wm1Map
                    self.myHashTable[word] = container
                
            self.index += 1
                    
                    
                
                #check wordMinusOne dictionary to see if w-1 is a key
                
                
                
    def removeSpaces(self, theWordList):
        index = 0

        for i in range(0, len(theWordList)):
            if(theWordList[index] == ''):
                del theWordList[index]
                index-=1
            index+=1
            
        return theWordList
    
    def computeHighestBigram(self, theHashTable, word):
        probabilityDict = {}
      
        #given 7 for testing
        nextWordDictionary = theHashTable[word]
        #denominator
        denominator = self.getCountofSingleWord(theHashTable, word)
        
        #numerator
        for key, frequencyList in nextWordDictionary.items():
            frequencyDictionary = frequencyList[0]
            count = 0
            for freqVals in frequencyDictionary.values():
                count += freqVals
              
            probabilityDict[key] = count / denominator
        
        value = max(probabilityDict.items(), key=operator.itemgetter(1))[0]
        return value
        
    def computeHighestTrigram(self, theHashTable, firstWord, secondWord, newPhraseState):
        value = ""
        if(self.newPhraseState == 0):
            probabilityDict = {}
            
            nextWordDictionary = theHashTable[firstWord]
            #denominator
            denominator = self.getCountofTwoWord(theHashTable, firstWord, secondWord)
            
            #numerator
            frequencyList = nextWordDictionary[secondWord]
            frequencyDictionary = frequencyList[0]
            
    
            for key, freqVals in frequencyDictionary.items():    
                probabilityDict[key] = freqVals / denominator

            value = max(probabilityDict.items(), key=operator.itemgetter(1))[0]
            #add phrase to list
            phrase = firstWord + " " + secondWord + " " + value
        
        #checks
        if(newPhraseState == 0 and not(phrase in self.phraseUsed)):
            self.addPhrase(phrase)
        elif(newPhraseState == 0 and(phrase in self.phraseUsed)):
            value = random.choice(list(theHashTable.keys()))
       #     self.phraseUsed.clear()
            self.newPhraseState = 1
        elif(newPhraseState == 1):
            value = self.computeHighestBigram(theHashTable, secondWord)
            self.newPhraseState = 2
        elif(newPhraseState == 2):
            value = self.computeHighestTrigramSingle(theHashTable, firstWord, secondWord)
            self.newPhraseState = 0
            
        return value
    
    def computeHighestTrigramSingle(self, theHashTable, firstWord, secondWord):
        probabilityDict = {}
        
        nextWordDictionary = theHashTable[firstWord]
        #denominator
        denominator = self.getCountofTwoWord(theHashTable, firstWord, secondWord)
        
        #numerator
        frequencyList = nextWordDictionary[secondWord]
        frequencyDictionary = frequencyList[0]
        

        for key, freqVals in frequencyDictionary.items():    
            probabilityDict[key] = freqVals / denominator
        
      
        
        value = max(probabilityDict.items(), key=operator.itemgetter(1))[0]
        return value
    
    def getCountofTwoWord(self, theHashTable, firstWord, secondWord):
        count = 0
        wordDict = theHashTable[firstWord]
        frequencyList = wordDict[secondWord]
        frequencyDictionary = frequencyList[0]
        
        for freqVals in frequencyDictionary.values():
                count += freqVals
        
        return count
    
    def getCountofSingleWord(self, theHashTable, word):
        count = 0
        wordDict = theHashTable[word]
        for frequencyList in wordDict.values():
            frequencyDictionary = frequencyList[0]
            for freqVals in frequencyDictionary.values():
                count += freqVals
        
        return count
    
    def getHashTable(self):
        return self.myHashTable
    
    def getPhraseUsed(self):
        return self.phraseUsed
    
    def addPhrase(self, thePhrase):
        self.phraseUsed.append(thePhrase)
        
    def getNewPhraseState(self):
        return self.newPhraseState
                
    
                
            
        