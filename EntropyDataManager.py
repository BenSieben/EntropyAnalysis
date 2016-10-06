import json

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
