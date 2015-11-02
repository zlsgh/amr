#!/usr/bin/env python
'''
Cleaning up the data from the 20 Newsgroups dataset
'''

import os


def main():
    path = "/Users/zschiller/Desktop/20news-18828/"
    i = 0
    l = len(os.listdir(path))
    j = 0
    for filename in os.listdir(path):
        # print "Working on", str(filename)
        if filename == ".DS_Store":
            pass
        else:
            if filename[-5:] == " copy":
                newName = filename.replace(" copy", "_1")
                os.rename(path + filename, path + newName)
                j += 1
            elif filename[-7:] == " copy 2":
                newName = filename.replace(" copy 2", "_2")
                os.rename(path + filename, path + newName)
                j += 1
            elif filename[-7:] == " copy 3":
                newName = filename.replace(" copy 3", "_3")
                os.rename(path + filename, path + newName)
                j += 1
            elif filename[-2:] == " 2":
                newName = filename.replace(" 2", "_1")
                os.rename(path + filename, path + newName)
                j += 1
        i += 1
        # print("completed " + str(i) + " of " + str(l) + '\n')
    print("replaced" + str(j))

main()
