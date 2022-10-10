'''
This program contains all the fucntions to be used when the checkout button is
pressed in the menu. It registers a checkout in the logfile and database as long
as the requested book is available and the members email is valid.

Written by F118143
Completed on 10/12/2021
'''
import database
from datetime import date

def book_available(ID):
    '''
    This fucntion takes a book ID and checks the database to see if the book is
    loaned, then returns a corresponding boolean value.
    '''
    if 1 <= int(ID) <= 34: #this is the amount of books in the library
        bookInfo = database.search_table(ID, 'database')
        if bookInfo[0][5] == '0': #checking is no assigned member ID
            available = True
        else:
            available = False  
    else:
        available = 'Error: book ID does not exist, please try again.'

    return available


def checkout_book(ID, memberEmail):
    '''
    This function takes a member email which it turns to an ID, it also takes a book
    ID which it assigns the member to in the database. It also appends the logfile.
    '''
    if ID == '' or memberEmail == '':
        msg = 'Error: please enter both details.'

    else:
        try: 
            inp = int(ID)

        except ValueError:
            msg = 'Error: please enter a number for the book ID.'

        else:
            emailList = memberEmail.partition('@')
            memberID = emailList[0]
            memberWarning = member_check(memberID) 
            available = book_available(ID) 

            if available == False: #loop to check that book can be checked out
                msg = 'Error: this book is already loaned, please try again.'
            elif available == 'Error: book ID does not exist, please try again.':
                msg = available 
            else:
                if memberID[:2] == 'xz' or memberID[:2] == 'xl':
                    database.append_logfile(ID, memberID)
                    database.alter_db(ID, memberID)
                    msg = memberWarning + '\n'*2+'The book was checked out successfully.'
                else:
                    msg = 'Error: The member\'s email must be all lower case'+\
                    ' \n      All member IDs start with xz or xl'

    return msg 
  
def member_check(memberID):
    '''
    This function uses the datetime module to check if a member has had a book for
    longer than 60 days and if so returns the warning message or alternative
    message.
    '''
    memberInfo = database.search_table(memberID, 'logbook') 
    todaysDate = date.today()

    if len(memberInfo) == 0: #for new member
        msg = 'Member does not have any books overdue.'
        return msg
    else:
        for log in memberInfo: #loop to check every log of certain member
            dateList = log[1].split("-")
            dateOut = date(int(dateList[0]), int(dateList[1]), int(dateList[2])) 
            delta = todaysDate - dateOut 
            outDays = delta.days #subtract two dates and get output in days
            if log[3] == 'False' and outDays >= 60: 
                ID = log[0]
                book = database.search_table(ID, 'database')#info about overdue book
                msg = 'Warning: This member has a book '+str(outDays)+\
                ' days over due:'+'\n'*2+'Overdue Book ~~ ID: '+book[0][0]+\
                ',  Genre: '+book[0][1]+',  Title: '+book[0][2]+',  Author: '+\
                book[0][3]+',  Date Purchased:'+book[0][4]+'\n'
                break
            else:
                msg = 'Member does not have any books over due date.' 
    
    return msg

#Testing
if __name__ == '__main__':
    #Testing book_available:

    print(book_available('10'), book_available('32'))
    #expected: True False

    #Testing member_check:

    print(member_check('xzyc'))
    #expected:Warning: This member has a book 97 days (or more) over due:

    #         Overdue Book ~~ ID: 32,  Genre: Action,  Title: The Bourne Identity,
    #         Author: Robert Ludlum,  Date Purchased:2014-10-19

    print(member_check('xzww'))
    #expected:Member does not have any books over due date.

    #         Testing checkout_book:

    print(checkout_book('10', 'xpqm@coldmail.com'))
    #expected:Error: The member's email must be all lower case 
    #                All member IDs start with xz or xl

    print(checkout_book('10', '12412'))
    #expected:Error: The member's email must be all lower case 
    #                All member IDs start with xz or xl

    print(checkout_book('10', ''))
    #expected:Error: please enter both details.

    print(checkout_book('', ''))
    #expected:Error: please enter both details.

    print(checkout_book('sda', 'xzqm@coldmail.com'))
    #expected:Error: please enter a number for the book ID.

    print(checkout_book('14', 'xzqm@coldmail.com'))
    #expectedError: this book is already loaned, please try again.

    print(checkout_book('10', 'xzqm@coldmail.com'))
    #expected:Member does not have any books over due date.

    #         The book was checked out successfully.

    print(checkout_book('33', 'xzap@coldmail.com'))
    #expected:Warning: This member has a book 97 days (or more) over due:

    #         Overdue Book ~~ ID: 7,  Genre: Mystery,  Title: The Night Fire,
    #         Author: Michael Connelly,  Date Purchased:2014-09-05


    #         The book was checked out successfully.
