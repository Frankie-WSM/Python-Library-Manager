'''
This is the program containing the main functions that read and write data to
the database and logfile.

Written by F118143
Completed on 10/12/2021
'''
from datetime import date

def search_table(search_term, file):
    '''
    This function searches eaither file for a certain term and outputs all data
    on the same line as this term.
    '''
    if file == 'database': #opening either file
        table = open("Database.txt","r")
        listOfLines = []
    else:
        table = open("logfile.txt","r")
        listOfLines = []

    for line in table: #loop reads line by line, splitting lines into elements
        l = line.strip()
        lineList = l.split("|")
        for element in lineList:
            if element == search_term:
                listOfLines.append(lineList)
            else:
                pass

    table.close() 
    return listOfLines 


def alter_db(ID, subject):
    '''
    This function looks for an ID in the database and alters the associated member
    ID to the person checking out or returning.
    '''
    dbRead = open("Database.txt","r") 
    allLines = dbRead.readlines() 
    count = 0
    s = '|' #seperator

    for element in allLines: #loop goes through all lines and changes stated one
        count += 1 
        l = element.strip()
        lineList = l.split('|')
        if lineList[0] == ID: 
            lineList[5] = subject+'\n'
            newLine = s.join(lineList)
            allLines[count - 1] = newLine 
            break
        else:
            pass

    dbRead.close()
    dbWrite = open("Database.txt","w")
    dbWrite.writelines(allLines) #to write all elements back in
    dbWrite.close()
    

def append_logfile(ID, subject):
    '''
    This function takes a book ID and a member ID and appends the logfile with
    this data when the book is withdrawn.
    '''
    lf = open("logfile.txt","a")
    s = '|'
    todaysDate = str(date.today())
    lf.write('\n'+ID+s+todaysDate+s+subject+s+'False')
    lf.close()


def register_return(ID):
    '''
    This function takes a book ID and accesses the logfile, finding the latest
    withdrawal of the book. It then sets the returned boolean to true.
    '''
    lfRead = open("logfile.txt","r")
    allLines = lfRead.readlines()
    allLines.reverse()
    count = 0
    s = '|'

    for element in allLines: #loop finds the last withdrawal of book
        count += 1
        l = element.strip()
        lineList = l.split('|')
        if lineList[0] == ID:
            lineList[3] = 'True'
            if allLines.index(element) != len(allLines): 
                newLine = s.join(lineList) +'\n' #new line if at bottom
            else:
                newLine = s.join(lineList)

            allLines[count - 1] = newLine 
            break
        else:
            pass

    lfRead.close() 
    allLines.reverse() 
    lfWrite = open("logfile.txt","w")
    lfWrite.writelines(allLines)
    lfWrite.close()


def count_logs(bookTitle):
    '''
    This function takes a books title and counts the amount of times it has been
    withdrawn in a dictionary.
    '''
    countTitle = dict()
    countTitle[bookTitle] = 0
    db = open('database.txt','r')
    allBooks = db.readlines()
    db.close()
    allBooks.pop(0)
    logfile = open('logfile.txt','r')
    allLogs = logfile.readlines()
    logfile.close()
    titleIDs = []

    for book in allBooks: #loop adds all IDs of a certain title to a list
        dbLine = book.split("|")
        if dbLine[2] == bookTitle:
            titleIDs.append(dbLine[0])
        else:
            pass

    for log in allLogs: #loop goes through all logs checking book IDs
        logLine = log.split("|")
        ID = logLine[0]
        if len(titleIDs) == 2: #max amount of one book in library is 2
            if logLine[0] == titleIDs[0] or logLine[0] == titleIDs[1]:
                countTitle[bookTitle] += 1
            else:
                pass
        else:
            if logLine[0] == titleIDs[0]:
                countTitle[bookTitle] += 1
            else:
                pass
    
    return countTitle 

#Testing
if __name__ == '__main__':
    
    #Testing search_table:

    print(search_table('Life Of Pi', 'database'))
    #expected:[['3', 'Action', 'Life Of Pi', 'Yann Martel', '2014-09-07', '0'],
    #          ['4', 'Action', 'Life Of Pi', 'Yann Martel', '2014-09-02', '0']]

    '''Testing alter_db & append_logfile & register_return:
    I will not test these functions induvidually as they must be used together
    to keep the logfile and database in sync. They have been tested in each of
    the modules that use them (checkout and return).'''

    #Testing count_logs:

    print(count_logs('Neuromancer'))
    #expected:{'Neuromancer': 8}
