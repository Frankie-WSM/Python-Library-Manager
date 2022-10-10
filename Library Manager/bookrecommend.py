'''
Book recommend includes all the functions that are used when the librarian inputs
a member's email address. The functions all call each other apart from give_chart
which is called via button press in the menu (main) program.

Written by F118143
Completed on 10/12/2021
'''
import database
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def give_chart(memberEmail):
    '''
    This function first takes an input from the menu program, and makes a member
    email into an ID and checks it is valid. If so it gets the members recommended
    books from the top_books function and returns the pie chart that is
    constructed using matplotlib along with a message, or just the latter.
    '''
    font = {'family' : 'Verdana', #properties for the pie chart writing
              'weight' : 'normal',
              'size'   : 10}
    plt.rc('font', **font)

    if memberEmail == '':
        msg = 'Error: please enter both details.'
        figBool = False
    else: 
        emailList = memberEmail.partition('@')
        memberID = emailList[0]
        if memberID[:2] == 'xz' or memberID[:2] == 'xl':
            memberLogs = database.search_table(memberID, 'logfile')
            if memberLogs == []: #for new member
                msg = 'Error: Member has not\nwithdrawn books before.'
                figBool = False
            else:
                titleList, amountList = top_books(memberID) #pie chart is made here
                fig1, ax2 = plt.subplots()
                ax2.pie(amountList, labels=titleList,
                        autopct='%1.1f%%', startangle=90)
                ax2.axis('equal')
                msg = '8 most reccomended books for '+memberID+':'
                figBool = True
        else:
            msg = 'Error: The member\'s email must be all lower case \n'+\
                  '      All member IDs start with xz or xl'
            figBool = False

    if figBool == True:
        return(fig1, msg, figBool)
    else:
        fig1 = 0
        return(fig1, msg, figBool)

def top_genres(memberID):
    '''
    Function to produce top 4 books and how many times each was withdrawn by the
    member. It collects all logs and searches the database to find the genre for
    the book in the log. It then counts the genres in a dictionary and takes only
    the top 4.
    '''
    memberGenres = []
    memberLogs = database.search_table(memberID, 'logfile')

    for log in memberLogs: #loop to get genres from each log
        ID = log[0]
        bookInfo = database.search_table(ID, 'database')
        genre = bookInfo[0][1]
        memberGenres.append(genre)

    genreDict = {}
    for element in memberGenres: #loop counts each genre 
        genreDict[element] = memberGenres.count(element)

    top4Genres = sorted(genreDict, key = genreDict.get, reverse = True)[:4]
    top4Amount = []
    for element in top4Genres: #loop to get corresponding amount with genre
        amount = genreDict[element]
        top4Amount.append(amount) 
    
    return top4Genres, top4Amount


def popular_books(memberID):
    '''
    This Function gets the top 4 genres and finds all books in each via the
    database. It returns a list of books for each genre.
    '''
    genre1Books = []
    genre2Books = []
    genre3Books = []
    genre4Books = []
    top4Genres, top4Amount = top_genres(memberID)
  
    for genre in top4Genres: #loop to add books to each genre's list
        linesOfBooks = database.search_table(genre, 'database')
        for book in linesOfBooks:
            if book[1] == genre and genre == top4Genres[0]:
                genre1Books.append(book[2])
            elif book[1] == genre and genre == top4Genres[1]:
                genre2Books.append(book[2])
            elif book[1] == genre and genre == top4Genres[2]:
                genre3Books.append(book[2])
            elif book[1] == genre and genre == top4Genres[3]:
                genre4Books.append(book[2])

    genre1Books = remove_dupes(genre1Books)
    genre2Books = remove_dupes(genre2Books)
    genre3Books = remove_dupes(genre3Books)
    genre4Books = remove_dupes(genre4Books)

    return genre1Books, genre2Books, genre3Books, genre4Books


def remove_dupes(aList):
    '''
    This function takes a list and removes duplicate elements.
    '''
    return list(dict.fromkeys(aList))


def top_books(memberID):
    '''
    This function takes a memberID and gets the top 4 genres for a user, it
    then uses dictionaries to get 3 books from the top genre, 2 from the middle
    ones and 1 from the fourth to reccommend.
    '''
    genre1Books, genre2Books, genre3Books, genre4Books = popular_books(memberID)
      
    genre1Dict = dict()
    genre2Dict = dict()
    genre3Dict = dict()
    genre4Dict = dict()

    for book in genre1Books: #counts the logs for books from each top genre
        genre1Dict.update(database.count_logs(book))
    for book in genre2Books:
        genre2Dict.update(database.count_logs(book))
    for book in genre3Books:
        genre3Dict.update(database.count_logs(book))
    for book in genre4Books:
        genre4Dict.update(database.count_logs(book))

    count1 = Counter(genre1Dict) #counts most common books by same key 
    count2 = Counter(genre2Dict)
    count3 = Counter(genre3Dict)
    count4 = Counter(genre4Dict)

    genre1Most = count1.most_common(3) #cuts the dictionaries down accordingly
    genre2Most = count2.most_common(2)
    genre3Most = count3.most_common(1)
    genre4Most = count4.most_common(1)

    finalBookList = genre1Most + genre2Most + genre3Most + genre4Most
    titleList , amountList = zip(*finalBookList) #2 lists for matplotlib graph

    return(titleList, amountList)


#testing
if __name__ == '__main__':

    print(give_chart(''))
    #expected:(0, 'Error: please enter both details.', False)
    print(give_chart('j21S'))
    #expected:(0, "Error: The member's email must be all lower case \n
    #          All member IDs start with xz or xl", False)
    print(give_chart('xzhh'))
    #expected:(0, 'Error: Member has not\nwithdrawn books before.', False)

    fig1, msg, figBool = give_chart('xlaa')
    fig1.show()
    print(msg, figBool)
    #expected: 8 most reccomended books for xlaa: True
    #**graph in seperate window**

    #Testing top_genres:

    print(top_genres('xlaa'))
    #expected:(['Sci-Fi', 'Fantasy', 'Non-Fiction', 'Action'] [6, 4, 3, 3])

    #Testing popular_books:

    print(popular_books('xzcn'))
    #expected:(['Circe', 'Ninth House', 'Dune', 'Hyperion']
    #          ['Night Things', 'Carrie', 'The Haunting of Hill House', 'Ring']
    #          ['The Night Fire', 'Gone Girl', 'The Guest List']
    #          ['A Brief History Of Time', 'The God Delusion', 'Columbine'])

    #Testing remove_dupes:

    print(remove_dupes(['r','r','g','b','v','g','r']))
    #expected:['r','g','b','v']

    #Testing top_books:

    print(top_books('xzbv'))
    #expected:(('Circe', 'Dune', 'Ninth House', 'A Scanner Darkly',
    #           'The Hunger Games Trilogy', 'Ring', 'Life Of Pi'),
    #          (27, 22, 7, 15, 14, 21, 17))
