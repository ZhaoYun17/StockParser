# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 13:16:14 2014

@author: Po
"""
# stockList = A list of Dictionaries. Dictionary contains details of a single stock
# total = total of the stock
# get.def_temp = defensive stock total
# get.totalTemp = Total profile sum


import csv
from urllib2 import urlopen
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from Tkinter import *

#input a cvs file
#returns a list containing Stock which is in a class of it's own
#key=Name of the stock
#value= tuple of (website to pull info from, unit of stock owned)


stockList=[]



class Stock(object):
    # input a tuple containing (Stock name, webpage to track stock value, total unit that you bought)
    # return a dictionary object with functions like getTotalValue, which returns the total value of that stock you have (unit * value per share)
    def __init__(self,title,website,unit):
        self.title=title
        self.website=website
        self.unit=unit
        self.price=self.getPrice()
        self.totalValue=self.getTotalValue()
    
    def __repr__(self):
        return """
        {}
        Units: {}
        PPS: {}
        Total: {}
        Referring from site:{}
        """.format(self.title,self.unit ,self.price, self.totalValue, self.website)
        
    def getTitle(self):
        return self.title
        
    def getWebsite(self):
        return self.website
    
    def getUnit(self):
        return self.unit
    
    def getPrice(self):
        # This is the webcrawler used to get the value from website, it works for now.
        htmlFile=urlopen(self.website)
        htmlFileReader=htmlFile.read()
        MagicWord='<label id="MainContent_lbQuoteLast" class="QouteLast">'
        #MagicWord is the xml text leading toward the price quote
        start_index=htmlFileReader.find(MagicWord)+len(MagicWord)
        return htmlFileReader[start_index:start_index+5]
        
    def getTotalValue(self):
        return float(self.price)*float(self.unit)

        
        
# Open csv, from it input (Stock name, webpage to track stock value, total unit that you bought) to set up the 'Stock' class.
with open('Po Profile.csv','rb') as PoProfile:
    PoProfileText=csv.reader(PoProfile)
    next(PoProfileText) #skip the stupid header
    for row in PoProfileText:
        stockList.append(Stock(row[0],row[1],row[2])) #This line prepared the stockList
        
# I use this line to check the stockList        
#print stockList



#2ND PART, PARSING THE DICTIONARY WE CREATED IN PART 1
'''
My new method of using class method kinda make this 2 function obsolete

def findTitle(htmlText):
    #give a stock website, return the stock name
    start_tag="<title>"
    end_tag="</title>"
    start_index=htmlText.find(start_tag)+len(start_tag)
    end_index=htmlText.find(end_tag)
    return htmlText[start_index:end_index].strip()


def findPrice(htmlText):
    #give a stock website, return the stock price
    MagicWord='<label id="MainContent_lbQuoteLast" class="QouteLast">'
    #MagicWord is the xml text leading toward the price quote
    start_index=htmlText.find(MagicWord)+len(MagicWord)
    return htmlText[start_index:start_index+5]

  



These line was use to test the parsing of the html

my_address = "http://www.malaysiastock.biz/Corporate-Infomation.aspx?type=A&value=M&source=M&securityCode=1155"
html_page = urlopen(my_address)

html_text = html_page.read()


print findTitle(html_text),findPrice(html_text)

'''

total=0 #Total amount in the form of stock.
labels=[] # List containing all the stock name
value=[] # List containing a stock's total value, in the same order as labels as we are using it to build a pie chart

# Calculating the "total" for the entire profile, and building variable 'labels' and 'value' for pie chart building
for stock in stockList:
    total+=stock.totalValue #prepare sum
    labels+=[stock.title] #prepare label for pie chart
    value+=[stock.totalValue] #prepare the value of pie chart

#plt.pie(value, labels=labels,
#            autopct='%1.1f%%', shadow=True)



def ori_run():
    # This funciton is what I use originally to run the whole file, before using function "GUI()".
    # Just skip this part unless you are looking for some history lesson.
    total=0
    labels=[]
    value=[]
    for stock in stockList:
        total+=stock.totalValue #prepare sum
        labels+=[stock.title] #prepare label for pie chart
        value+=[stock.totalValue] #prepare the value of pie chart
    
    plt.pie(value, labels=labels,
            autopct='%1.1f%%', shadow=True)
    # I still don't undertand how this line work, I just substitute my own value in.
        
    print stockList
    print "The total in this profile :" + str(total)
    
    plt.show()

    raw_input("The End [Press Enter to Exit]")
    
#ori_run()

def GUI():
    # This is it guys! This is the entire GUI code, make for Tkinter.

    # Calling the GUI and give it a title
    window=Tk()
    window.title("Po's Investment Profile")
    
    # First Frame=numberFrame, grid setting.
    numberFrame=Frame(window)
    numberFrame.grid()
    
    # The first row would, naturally, be use to as labels
    Label(numberFrame, text="Stock", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=1)
    Label(numberFrame, text = "Price Per Share", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=2)
    Label(numberFrame, text = "Units", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=3)
    Label(numberFrame, text = "Total", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=4)
    Label(numberFrame, text = "% in Profile", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=5)
    
    # I came up with the ingenious idea to create a currentRow variable and change it to move grid to pack labels in.
    # I am sure others do it too or even have better ways but I am still very proud of myself. hehe.
    currentRow=1
    
    # Now we are packing Title, Price, Unit, TotalValue and calculate the ratio of each stock to the entire value of the profile.
    # Good thing that we create a special class for the stock, don't cha think?
    for stock in stockList:
        currentRow +=1 #so we can set the row in a new row
        Label(numberFrame, text = stock.getTitle(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=1)
        Label(numberFrame, text = stock.getPrice(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=2)
        Label(numberFrame, text = stock.getUnit(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=3)
        Label(numberFrame, text = stock.getTotalValue(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=4)
        Label(numberFrame, text = "{0:.2f}%".format(stock.getTotalValue()/total*100), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=5)
    
    
    # Time to move another row down~
    currentRow+=1
    
    # And the total is:
    Label(numberFrame,text ="Total =>",fg="blue", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=3)
    Label(numberFrame,text = total, fg="blue", font=("Symbol", 12), padx=5,pady=5).grid(row=currentRow,column=4)
    
    #PIE CHART STARTS HERE
    # To be honest with you, I have no idea on any of the below, I know we pack a canvas into TKinter, and.. well, thanks stackoverflow,
    # I just trial and error with other's code and.. It works!! I couldn't care less about the logic , I am busy dancing on my chair!
    f = Figure(figsize=(5,4), dpi=80)    
    a=f.add_subplot(111)
    a.pie(value, labels=labels,
            autopct='%1.1f%%', shadow=True)
    
    canvas = FigureCanvasTkAgg(f, master=window)
    canvas.get_tk_widget().grid(row=1,column=0, columnspan = 3)
    
    #ADDING A NEW FRAME TO SEPARATE THE PIE CHART WITH NEW STUFF    
    ratioFrame=Frame(window)
    ratioFrame.grid()
    
    currentRow=1
    
    # Label the defensive asset
    Label(ratioFrame, text="DEF Asset=", font=("Helvetica", 12), fg="black", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=1)
    
    # Need a wrapper to handle error message for tkinter, no idea why but the normal Try and except don't work on Tkinter.
    # Got this from stackoverflow, work like charm.
    """ TASK: Make a pop up! I donno how to make a pop up!!"""
    class safe: # the decorator
      def __init__(self, function):
        self.function = function
    
      def __call__(self, *args):
        try:
          return self.function(*args)
        except Exception, e:
          # make a popup here with your exception information.
          # might want to use traceback module to parse the exception info
          print "Error: %s" % (e)
          print "insert something valid!"
          defense.config(text="Insert number please!")
          offense.config(text="Insert number please!")
          totalSum.config(text="Insert number please!")    
    
    @safe
    def get(self):
        # get value from the entry_cel down there, calculate the percentage and returns the value
        #I tried try and except here, it didn't work, need to use the wrapper @safe
        def_temp = float(entry_cel.get())
        # calculate converted temperature and place it in label
        def_percent = def_temp/(def_temp+total)*100
        off_percent = total/(def_temp+total)*100
        totalTemp= total+def_temp
        
        defense.config(text="{0:.2f}%".format(def_percent))
        offense.config(text="{0:.2f}%".format(off_percent))
        totalSum.config(text="{0:.2f}".format(totalTemp))
        
    # Entry cell is a bad name, should prolly change it to something like Def_asset_input_cel:
    # Anyways it is an entry box for inputting defensive asset value
    entry_cel = Entry(ratioFrame, width=7)
    entry_cel.grid(row=currentRow,column=2)
    # This line lets me press "Enter" to run function get()
    entry_cel.bind('<Return>', get)
    
    
    currentRow+=1
    
    # Packing those SWEET calculation in
    Label(ratioFrame, text="DEF Asset=>", font=("Helvetica", 12), fg="blue", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=1)
    Label(ratioFrame, text="<=Stock Asset", font=("Helvetica", 12), fg="blue", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=4)
    
    defense=Label(ratioFrame, text="-", font=("Times", 12), fg="black", relief=SUNKEN, padx=5,pady=5)
    defense.grid(row=currentRow,column=2)
    offense=Label(ratioFrame, text="-", font=("Times", 12), fg="black", relief=SUNKEN, padx=5,pady=5)
    offense.grid(row=currentRow,column=3)
    
    currentRow+=1    
    
    # Calculating the total value of the profile, $$$$
    Label(ratioFrame, text="Profile Value=", font=("Helvetica", 12), fg="black", padx=5,pady=5).grid(row=currentRow,column=2)
    totalSum=Label(ratioFrame, text="$$$", font=("Helvetica", 12), fg="black", padx=5,pady=5)
    totalSum.grid(row=currentRow,column=3)
    
    
    
    
    
    
        
    
    
    

    
    
    
    window.mainloop()


GUI()