'''
This program acts as the main program. It displays the GUI on the screen and
all the elements within the GUI, and also houses the function for the buttons
which uses every other module.

Written by F118143
Completed on 15/12/2021
'''
from tkinter import * #importing tkinter module and ttk for notebook
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import booksearch
import bookcheckout
import bookreturn
import bookrecommend
    
root = Tk()
root.title('Library Manager')
root.geometry('800x450')
notebook = ttk.Notebook(root) #initialises notebook which I am using for tabs
notebook.pack()
#initialises the frames for the windows
search_frame = Frame(notebook, width=800, height=450, bg='white')
checkout_frame = Frame(notebook, width=800, height=450, bg='white')
return_frame = Frame(notebook, width=800, height=450, bg='white')
recommend_frame = Frame(notebook, width=800, height=450, bg='white')
#packs all the frames onto the screen so we can actually see them
search_frame.pack(fill='both', expand=1)
checkout_frame.pack(fill='both', expand=1)
return_frame.pack(fill='both', expand=1)
recommend_frame.pack(fill='both', expand=1)
#adds notebook tabs 
notebook.add(search_frame, text='Search Book')
notebook.add(checkout_frame, text='Checkout Book')
notebook.add(return_frame, text='Return Book')
notebook.add(recommend_frame, text='Recommend Book')
#creates canvas for all tabs
searchCanvas = Canvas(search_frame, width = 800, height = 450)
checkoutCanvas = Canvas(checkout_frame, width = 800, height = 450)
returnCanvas = Canvas(return_frame, width = 800, height = 450)
recommendCanvas = Canvas(recommend_frame, width = 800, height = 450)

#the functions below are for the button press on each tab
def menu_return():
    '''
    This function gets the input from the return tabs entry box and applies
    the return function in the return module to get an output.
    '''
    inp = str(returnEntryBox.get())
    out = bookreturn.return_book(inp)
    returnLabel.config(text = out, font = 'Arial 12')

def menu_search():
    '''
    This function gets the input from the search tabs entry box and applies
    the search function in the search module to get an output.
    '''
    inp = str(searchEntryBox.get())
    out = booksearch.get_books(inp)
    searchLabel.config(text = out, font = 'Arial 10')

def menu_checkout():
    '''
    This function gets the input from the checkout tabs entry boxes and applies
    the checkout function in the checkout module to get an output.
    '''
    inpMemberEmail = str(checkoutEntryBox1.get())
    inpID = str(checkoutEntryBox2.get())
    out = str(bookcheckout.checkout_book(inpID, inpMemberEmail))
    checkoutLabel.config(text = out, font = 'Arial 10')
    
def menu_recommend():
    '''
    This function gets the input from the recommend tabs entry box and applies
    the chart function in the recommend module to get an output.
    '''
    inp = str(recommendEntryBox.get())
    fig1, msg, figBool = bookrecommend.give_chart(inp)
    if figBool == True:
        recommendLabel2.config(text = '', font = 'Arial 10')
        graphCanvas = FigureCanvasTkAgg(fig1, master = recommend_frame)
        graphCanvas.draw()
        graphCanvas.get_tk_widget().place(x=20, y=130, width=760, height=280)
        recommendLabel1.config(text = msg, font = 'Arial 12')
    else:
        recommendLabel2.config(text = msg, font = 'Arial 10')
        

#places all the elements in the search tab (apart from output label)
searchCanvas.create_text(157, 25, text="Please Enter The Book Title:",
                         fill="black", font=('Arial 14'))
searchCanvas.pack()
searchEntryBox = Entry(search_frame)
searchEntryBox.place(x = 30, y = 60, width = 350, height = 25)
searchButton = Button(search_frame, text = 'Search', command = menu_search)
searchButton.place(x = 380, y = 105, width = 100, height = 40)
searchLabel = Label(search_frame, text = '')
searchLabel.place(x = 10, y = 165)

#places all the elements in the checkout tab (apart from output label)
checkoutCanvas.create_text(607, 25, text="Please Enter The Book ID:",
                           fill="black", font=('Arial 14'))
checkoutCanvas.create_text(157, 25, text="Please Enter The Member's Email:",
                           fill="black", font=('Arial 14'))
checkoutCanvas.pack()
checkoutEntryBox1 = Entry(checkout_frame)
checkoutEntryBox1.place(x = 30, y = 60, width = 350, height = 25)
checkoutEntryBox2 = Entry(checkout_frame)
checkoutEntryBox2.place(x = 500, y = 60, width = 100, height = 25)
checkoutButton = Button(checkout_frame, text = 'Checkout',
                        command = menu_checkout)
checkoutButton.place(x = 380, y = 105, width = 100, height = 40)
checkoutLabel = Label(checkout_frame, text = '')
checkoutLabel.place(x = 50, y = 200)

#places all the elements in the return tab (apart from output label)
returnCanvas.create_text(137, 25, text="Please Enter The Book ID:",
                         fill="black", font=('Arial 14'))
returnCanvas.pack()
returnEntryBox = Entry(return_frame)
returnEntryBox.place(x = 30, y = 60, width = 350, height = 25)
returnButton = Button(return_frame, text = 'Return', command = menu_return)
returnButton.place(x = 380, y = 105, width = 100, height = 40)
returnLabel = Label(return_frame, text = '')
returnLabel.place(x = 50, y = 200)

#places all the elements in the recommend tab (apart from output label)
recommendCanvas.create_text(157, 25, text="Please Enter The Member's Email:",
                            fill="black", font=('Arial 14'))
recommendCanvas.pack()
recommendEntryBox = Entry(recommend_frame)
recommendEntryBox.place(x = 30, y = 60, width = 350, height = 25)
recommendButton = Button(recommend_frame, text = 'Recommend',
                         command = menu_recommend)
recommendButton.place(x = 395, y = 50, width = 100, height = 40)
recommendLabel1 = Label(recommend_frame, text = '')
recommendLabel1.place(x = 50, y = 97)
recommendLabel2 = Label(recommend_frame, text = '')
recommendLabel2.place(x = 500, y = 45)

root.mainloop()
