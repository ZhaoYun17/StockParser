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
        htmlFile=urlopen(self.website)
        htmlFileReader=htmlFile.read()
        MagicWord='<label id="MainContent_lbQuoteLast" class="QouteLast">'
        #MagicWord is the xml text leading toward the price quote
        start_index=htmlFileReader.find(MagicWord)+len(MagicWord)
        return htmlFileReader[start_index:start_index+5]
        
    def getTotalValue(self):
        return float(self.price)*float(self.unit)

        
        
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

total=0
labels=[]
value=[]
for stock in stockList:
    total+=stock.totalValue #prepare sum
    labels+=[stock.title] #prepare label for pie chart
    value+=[stock.totalValue] #prepare the value of pie chart

#plt.pie(value, labels=labels,
#            autopct='%1.1f%%', shadow=True)



def ori_run():
    total=0
    labels=[]
    value=[]
    for stock in stockList:
        total+=stock.totalValue #prepare sum
        labels+=[stock.title] #prepare label for pie chart
        value+=[stock.totalValue] #prepare the value of pie chart
    
    plt.pie(value, labels=labels,
            autopct='%1.1f%%', shadow=True)
    
        
    print stockList
    print "The total in this profile :" + str(total)
    
    plt.show()

    raw_input("The End [Press Enter to Exit]")
    
#ori_run()

def GUI():
    window=Tk()
    window.title("Po's Investment Profile")
    
    numberFrame=Frame(window)
    numberFrame.grid()
    
    Label(numberFrame, text="Stock", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=1)
    Label(numberFrame, text = "Price Per Share", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=2)
    Label(numberFrame,text = "Units", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=3)
    Label(numberFrame,text = "Total", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=4)
    Label(numberFrame,text = "% in Profile", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=1,column=5)
    
    currentRow=1
    for stock in stockList:
        currentRow +=1 #so we can set the row in a new row
        Label(numberFrame, text=stock.getTitle(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=1)
        Label(numberFrame, text = stock.getPrice(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=2)
        Label(numberFrame,text = stock.getUnit(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=3)
        Label(numberFrame,text = stock.getTotalValue(), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=4)
        Label(numberFrame,text = "{0:.2f}%".format(stock.getTotalValue()/total*100), font=("Times", 12), padx=5,pady=5).grid(row=currentRow,column=5)
    
    
    currentRow+=1
    Label(numberFrame,text ="Total =>",fg="blue", font=("Helvetica", 12), relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=3)
    Label(numberFrame,text = total, fg="blue", font=("Symbol", 12), padx=5,pady=5).grid(row=currentRow,column=4)
    
    #PIE CHART STARTS HERE
    
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
    
    Label(ratioFrame, text="DEF Asset=", font=("Helvetica", 12), fg="black", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=1)
    
    
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
          defense.config(text="INVALID")
          offense.config(text="OKU")
          totalSum.config(text="CACAT")    
    
    @safe
    def get(self):
        def_temp = float(entry_cel.get())
        try: # calculate converted temperature and place it in label
            #print def_temp
            #print type(def_temp)
            
            #print type(total)
            #print total

            #print def_temp/(def_temp+total)*100
            def_percent = def_temp/(def_temp+total)*100
            off_percent = total/(def_temp+total)*100
            totalTemp= total+def_temp
            
            #print type(def_percent)
            #print type(off_percent)
            #print def_percent
            #print off_percent
            #print type(defense)
            #print type(offense)
            defense.config(text="{0:.2f}%".format(def_percent))
            offense.config(text="{0:.2f}%".format(off_percent))
            totalSum.config(text="{0:.2f}".format(totalTemp))
            
        except ValueError: #user entered non-numberic temperature
        #   entry_cel.config(text="invalid")
        #   print "insert something valid!"
            pass
        
    
    entry_cel = Entry(ratioFrame, width=7)
    entry_cel.grid(row=currentRow,column=2)
    entry_cel.bind('<Return>', get)
    
    
    currentRow+=1
    
    Label(ratioFrame, text="DEF Asset=>", font=("Helvetica", 12), fg="blue", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=1)
    Label(ratioFrame, text="<=Stock Asset", font=("Helvetica", 12), fg="blue", relief=RIDGE, padx=5,pady=5).grid(row=currentRow,column=4)
    
    defense=Label(ratioFrame, text="-", font=("Times", 12), fg="black", relief=SUNKEN, padx=5,pady=5)
    defense.grid(row=currentRow,column=2)
    offense=Label(ratioFrame, text="-", font=("Times", 12), fg="black", relief=SUNKEN, padx=5,pady=5)
    offense.grid(row=currentRow,column=3)
    
    currentRow+=1    
    
    Label(ratioFrame, text="Profile Value=", font=("Helvetica", 12), fg="black", padx=5,pady=5).grid(row=currentRow,column=2)
    totalSum=Label(ratioFrame, text="$$$", font=("Helvetica", 12), fg="black", padx=5,pady=5)
    totalSum.grid(row=currentRow,column=3)
    
    
    
    
    
    
        
    
    
    

    
    
    
    window.mainloop()


GUI()