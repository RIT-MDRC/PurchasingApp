'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Contains the functions that are simplifying the process
'''

def parseCommands(data_text):

    return list(word.lower() for word in data_text.split())
