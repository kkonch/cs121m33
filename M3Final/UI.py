from tkinter import *
from tokenizer import tokenize

# import all files we worked on
from searchIndex import *
from time_inverted_index import *
import urllib.request
import urllib.error


# sample backenddddd
class Backend:
    def __init__(self, urlL):
        self.urlList = urlL
    def get_links(self, query):
        # put tokens here
        start_time = time.time()
        new_list=[]
        result = booleanSearch(query, self.urlList)
        print("--- %s seconds ---" % (time.time() - start_time))
        for link in result:
            try:
                response = urllib.request.urlopen(link)
                new_list.append(link)
                # if response.getcode() == 404:
                #     print("Error, bad request")
                #     result.remove(link)
                # Check other conditions here and decide whether to keep the link   
            except:
                print(link, " not valid")
        # for link in result:
        #     try:
        #         response = urllib.request.urlopen(link)
        #         print("done")
        #         if response.getcode() == 400:
        #             print("Error, bad request")
        #         # if "redmiles.ics.uci.edu" in link or "https://redmiles.ics.uci.edu/publication/" in link or link.endswith(".php"):
        #         #     result.remove(link)
        #     except urllib.error.HTTPError as e:
        #         print(e)
        return new_list[:10]

class SearchUI:
    
    def __init__(self, master, urlL):
        #self.urlList = urlL
        self.master = master
        master.geometry("600x350")
        master.title("Document Search")
        self.tokens=[]
        self.l = Label(master, text="What would you like to search?") 
        self.inputtxt = Text(master, height=3, width=60, bg="light yellow", fg="black") 
        self.display = Button(master, width=15, height=5, text="Input", command=self.take_input) 
        self.lstBox = Listbox(master, height=10, width=60, bg='#000', fg='#ff0')

        self.l.pack(pady=(10, 5)) 
        self.inputtxt.pack(pady=5) 
        self.display.pack(pady=5) 
        self.lstBox.pack(pady=5) 
        
        self.backend = Backend(urlL)  

    def take_input(self): 
        input_text = self.inputtxt.get("1.0", "end-1c") 
        # self.tokens = sorted(input_text.split())
        for tok in input_text.split():
            tok=tokenize(tok)
            self.tokens.extend(tok)
        self.tokens = sorted(self.tokens)

        if len(self.tokens) >= 1:  # Check if input is not empty
            links = self.backend.get_links(self.tokens) # get links from backend
            self.update_listbox(links) # update the listbox w the links

    def update_listbox(self, links):
        self.lstBox.delete(0, END)  # init empty list box
        for link in links: # add to listbox
            self.lstBox.insert(END, link)  

if __name__ == "__main__":
    with open('URLINDEX.txt', 'r') as f:
        thisLine = f.readline()
        f.close()
    URL_List = thisLine[:-1].split('\t')
    
    root = Tk()
    app = SearchUI(root, urlL=URL_List)
    root.mainloop()

    # getting the query as an alphabetized list: 
        # ex: input  =  "master of software engineering"
        #  -> tokens = ['engineering', 'master', 'of', 'software']
    # print("Tokens:", app.tokens)

