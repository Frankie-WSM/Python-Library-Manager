'''
This program is used to return books when the return button is pressed. It
checks the users input and that the book isn't in the library and then
changes both the files using the suitable functions in database.py.

Written by F118143
Completed on 10/12/2021
'''
import database
from datetime import date

def return_book(ID):
    '''
    This function takes a book ID, checks it is valid and not already in the
    library, and then changes the logfile and database accordingly. It also
    povides a warning if the member has had the book for over 60 days.
    '''
    if ID == '':
        msg = 'Error: please enter a book ID to return.'
    else:
        try: #checks that the input is an integer, if not, recognises the error
            inp = int(ID)

        except ValueError:
            msg = 'Error: please enter a number for the book ID.'

        else:
            if 1 <= int(ID) <= 34:
                bookOut = database.search_table(ID,'database') 
                if bookOut[0][5] != '0':
                    success_msg = 'Return registered successfully.'
                    memberInfo = database.search_table(ID, 'logbook') 
                    todaysDate = date.today()
                    for log in memberInfo: #loop to check days loaned and change files
                        dateList = log[1].split("-")
                        dateOut = date(int(dateList[0]),
                                       int(dateList[1]), int(dateList[2])) 
                        delta = todaysDate - dateOut 
                        outDays = delta.days #subtract two dates and get output in days
                        if log[3] == 'False' and outDays >= 60:
                            overdue_msg = 'Warning: this book was loaned for '+\
                            str(outDays)+' days.'
                            msg = success_msg+'\n'*2+overdue_msg
                            database.register_return(ID)
                            database.alter_db(ID, '0')
                            break
                        else:
                            msg = success_msg
                            database.register_return(ID)
                            database.alter_db(ID, '0')
                else:
                    msg = 'Error: book already in library.'
            else:
                msg = 'Error: book ID doesn\'t exist, try again.'

    return msg

#Testing
if __name__ == '__main__':
    
    #Testing return_book:

    print(return_book(''))
    #expected:Error: please enter a book ID to return.

    print(return_book('234'))
    #expected:Error: book ID doesn't exist, try again.

    print(return_book('snh'))
    #expected:Error: please enter a number for the book ID.

    print(return_book('31'))
    #expected:Error: book already in library.

    print(return_book('14'))
    #expected:Return registered successfully.

    print(return_book('6'))
    #expected:Return registered successfully.

    #         Warning: this book was loaned for 109 days (or more).
