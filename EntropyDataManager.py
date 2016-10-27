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



