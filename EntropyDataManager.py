import json
from Packet import Packet

# Class to manage File I/O for the program
# This class should be utilized by the GUI
# to save or load analyzed data
# Uses JSON dumping and loading to easily serialize / deserialize analytics


class EntropyDataManager:
    def __init__(self, filename):
        self.filename = filename

    # Opens the file of what self.filename currently is
    # (returns what json.load obtains)
    def openFile(self):
        f = open(self.filename, "r")
        return json.load(f)

    # Saves the given data to what self.filename currently is
    def saveFile(self, data):
        f = open(self.filename, "w")
        json.dump(data, f)

# testing the class
e = EntropyDataManager("test.txt")
data = [["1", 3], ["a", "b", "cccc", 50]]
print(data)
e.saveFile(data)
savedData = e.openFile()
print(savedData)
print(savedData[1][1])
print(type(savedData[1][1]))
if data[1][1] == savedData[1][1]:
    print("saved string matches original string")

# testing if this still works on Packet class
edm = EntropyDataManager("test2.txt")
packetData = []
for i in range(0, 10):
    p = Packet("Site " + str(i), "Head " + str(i), "Body " + str(i), i)
    packetData.append(p)
print(packetData[2])
# this will FAIL; Packet objects are not considered JSON serializable
# edm.saveFile(packetData)
# for p in packetData:
#     print(p)
# savedPacketData = edm.openFile()
# for sP in savedPacketData:
#    print(sP)

