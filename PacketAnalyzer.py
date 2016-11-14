from __future__ import division
import socket
import math

import os

import struct

from ctypes import *

# Converts data into binary form

# and performs entropy analysis on packet data.



class PacketAnalyzer:

    def __init__(self):

        self.entropyResult = 0

    

    # Converts a list of filtered packet data into binary form

    # filteredPackets is a list of filtered packet data

    # Returns the binary form of the list

    def convertToBinary(self, filteredPackets):

        binaryPackets = []

        for packet in filteredPackets:  # examine each packet in the filtered packets list to convert each into binary

            binaryPacket = ''

            for packetChar in packet:

                packetCharValue = ord(packetChar)  # get ASCII value of each character

                packetCharValueBinary = self.convertNumberToBinary(packetCharValue, 8) # convert value into binary byte

                binaryPacket += packetCharValueBinary  # add binary byte value of character to binary packet string

            binaryPackets.append(binaryPacket)

        return binaryPackets



    # Converts a given (positive or zero) number into binary

    # num = number to convert to binary

    # numBits = how many bits to use to store the result

    # Note that if numBits cannot hold the value of num completely, the result will not be correct

    def convertNumberToBinary(self, num, numBits):

        byteString = ''  # start off byte string as all empty (the for loop below will build the bits)

        numRemaining = num

        for i in range(numBits, 0, -1): # go from numBits through 0 in steps of -1 (going backwards)

            if numRemaining >= 2 ** (i - 1):  # check if numRemaining >= 2^i (i.e., the value for this bit position

                byteString += '1'  # put 1 as bit if numRemaining was big enough to fill the bit

                numRemaining -= 2 ** (i - 1)  # decrement numReamining to subtract this filled bit's value

            else:

                byteString += '0'  # put 0 as bit if it numRemaining was too small

        return byteString


    def getNumericList(self, packetData):
        numericList = []
        
        # Turn packetData into string
        s = "".join(packetData)

        # Turn each character in string into a decimal number
        for n in s:
            numericList.append(ord(n))

        return numericList
    
    def hist(self,source):
        hist = {}
        l = 0
        for e in source:
            l += 1
            if e not in hist:
                hist[e] = 0
            hist[e] += 1
        return(l, hist)

    # Shannon's Entropy algorithm
    def determineEntropy(self, hist, l):
        elist = []
        for v in hist.values():
            c = v / l
            elist.append(-c * math.log(c, 2))
        return sum(elist)
    
    def printHist(self, h, l):
        flip = lambda(k,v) : (v,k)
        h = sorted(h.iteritems(), key = flip)
        print 'Sym\thi\tfi\tInf'
        for(k,v) in h:
            print '%s\t%f\t%f\t%f'%(k,v,v/l,-math.log(v/l, 2))
    

    def entropyAnalysis(self, packetData):
        print "Performing Entropy analysis\n"
        
        # Turn the packetData into decimal values
        numList = self.getNumericList(packetData)
        
        # print the number list as a string
        print repr(numList)
        (l,h) = self.hist(numList)
        #self.determineEntropy(h,l)
        print "Entropy:", self.determineEntropy(h,l)
        self.printHist(h, l)