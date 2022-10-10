'''
This program is used to get the information of the specified book when the
search button is pressed. It can also highlight books that are overdue if that
book has been searched.

Written by F118143
Completed on 10/12/2021
'''
import database
from datetime import date

def get_books(book):
    '''
    This function takes a book title and finds all books with this title
    (different IDs). It then collects the row of data and returns it as a
    single string.
    '''
    msg = ""
    if book == '':
        msg = 'Error: please enter a book title.'
    else:
        bookList = database.search_table(book,'database') 
        if len(bookList) == 0: 
            msg = 'Error: There are no books with this title, please try again.'
        else:
            for line in bookList: #loop prints all books with searched title
                overdue = check_overdue(line[0])
                if overdue == False:
                    lineStr = 'ID: '+line[0]+',  Genre: '+line[1]+',  Title: '+\
                    line[2]+',  Author: '+line[3]+',\nDate Purchased: '+\
                    line[4]+',  Holding member: '+line[5]+'\n'
                    msg = msg+'\n'*2+lineStr 
                else: #vvvfor overdue bookvvv
                    lineStr = 'ID: '+line[0]+',  Genre: '+line[1]+',  Title: '+\
                    line[2]+',  Author: '+line[3]+',\nDate Purchased: '+\
                    line[4]+',  Holding member: '+line[5]+\
                    '  (Warning: this book is overdue)'
                    msg = msg+'\n'*2+lineStr 
    return msg


def check_overdue(ID):
    '''
    This fucntion takes a book Id and checks using the logbook and datetime
    module if the book is overdue. If so it will return True, if not, False.
    '''
    bookInfo = database.search_table(ID, 'logbook')
    todaysDate = date.today()

    for log in bookInfo: #loop goes through every log for a book ID
        dateList = log[1].split("-")
        dateOut = date(int(dateList[0]), int(dateList[1]), int(dateList[2])) 
        delta = todaysDate - dateOut #^^date in this format for subtraction^^
        outDays = delta.days  
        if log[3] == 'False' and outDays >= 60:
            overdue = True
        else:
            overdue = False

    return overdue
    

#Testing
if __name__ == '__main__':
    print(get_books('Dune'))
    #expected:ID: 26,  Genre: Fantasy,  Title: Dune,  Author: Frank Herbert,
    #         Date Purchased: 2014-10-13,  Holding member: 0
    print(get_books('2nsan8'))
    #expected:ID: 27,  Genre: Fantasy,  Title: Dune,  Author: Frank Herbert,
    #         Date Purchased: 2014-10-13,  Holding member: xlma

    #         Error: There are no books with this title, please try again.
    print(check_overdue('3'))
    #expected:False
    print(check_overdue('32'))
    #expected:True
