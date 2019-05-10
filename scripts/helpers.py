'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Contains the functions that are simplifying the process
'''

# Returns all the workds entered in a text for later processing
def parseCommands(data_text):

    return list(word.lower() for word in data_text.split())

# Generates a random hex color value and returns a string
def getRandomColor():
    import random

    color = "#"

    for val in range(6):
        color += hex(random.randint(0, 16))[2:]

    return color
