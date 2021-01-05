import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
import brainfuck
from tkinter.colorchooser import *
from tkinter.scrolledtext import ScrolledText

class Main(Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Untitled - Vulgar")
        self.geometry('800x600')
        self.menuBar = Menu(self)
        self.FileMenu = Menu(self.menuBar, tearoff = 0)
        self.EditMenu = Menu(self.menuBar, tearoff = 0)
        self.RunMenu = Menu(self.menuBar, tearoff = 0)
        self.HelpMenu = Menu(self.menuBar, tearoff = 0)
        self.ConfigMenu = Menu(self.menuBar, tearoff = 0)
        self.window_title = "Code "
        self.tabControl = ttk.Notebook(self)
        self.tab1 = Frame(self.tabControl)
        self.tab2 = Frame(self.tabControl)
        self.tabControl.add(self.tab1, text = self.window_title)
        self.tabControl.add(self.tab2, text = "Console")
        self.tabControl.pack(expand = 1, fill = BOTH)
        self.line_num = Canvas(self.tab1, width = 50, bg = "black")
        self.textArea = ScrolledText(self.tab1,background = "black", foreground = "white", insertbackground = "white", wrap = WORD, width = 93, height = 90)
        self.View = ScrolledText(self.tab2, background = "black", foreground = "white", insertbackground = "white", wrap = WORD, width = 93, height = 90)
        self.scroll = Scrollbar(self.textArea)
        self.file = None
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.FileMenu.add_command(label = "New File         Ctrl+N", command = self.newFile)
        self.FileMenu.add_command(label = "Open...            Ctrl+O", command = self.openFile)
        self.FileMenu.add_command(label = "Save              Ctrl+S", command = self.saveFile)
        self.FileMenu.add_command(label = "Save As...        Ctrl+Shift+S", command = self.SaveAs)
        self.FileMenu.add_command(label = "Exit              Ctrl+Q", command = self._quit_)
        
        self.HelpMenu.add_command(label = "About ", command = self.ShowAbout)
        self.HelpMenu.add_command(label = "How to use", command = None)
        
        self.EditMenu.add_command(label = "undo      Ctrl+Z", command = self.undo)
        self.EditMenu.add_command(label = "redo      Ctrl+Y", command = self.redo)
        self.EditMenu.add_command(label = "Copy      Ctrl+C", command = self.copy)
        self.EditMenu.add_command(label = "Cut         Ctrl+X", command = self.cut)
        self.EditMenu.add_command(label = "Paste      Ctrl+V", command = self.paste)
        self.EditMenu.add_command(label = "Select All  Ctrl+A", command = None)

        self.ConfigMenu.add_command(label = "Set background color", command = self.Setbg)
        self.ConfigMenu.add_command(label = "Set text color", command = self.Setfg)
        self.ConfigMenu.add_command(label = "Set cursor color", command = self.SetCurs)
        self.RunMenu.add_command(label = "Run code       F5", command = self.Run)

        self.menuBar.add_cascade(label = "File", menu = self.FileMenu)
        self.menuBar.add_cascade(label = "Edit", menu = self.EditMenu)
        self.menuBar.add_cascade(label = "Run", menu = self.RunMenu)
        self.menuBar.add_cascade(label = "Configure IDE", menu = self.ConfigMenu)
        self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)
        self.config(menu = self.menuBar)
        self.line_num.pack(side=LEFT, fill = Y)
        #self.textArea.pack(side = RIGHT, fill = "both")
        self.textArea.place(x = 35)
        self.bind("<F5>", lambda x:self.Run())

        self.textArea.bind('<Return>', lambda x:self.update_line_nums(x))
        #bind update_line_nums to textArea here
        self.View.pack()
        self.text = "Vulgar - console >>>"
        self.View.insert(0.0, self.text)
        self.View.config(state = DISABLED)
        self.update_line_nums()

    def _quit_(self):
        if askokcancel("Exit", "Are you sure you want to quit?"):
            self.self.destroy()

    def update_line_nums(self, *args):
        i = str(float(self.textArea.index('end'))-1)
        dline = self.textArea.dlineinfo(i)
        y = dline[1]
        linenum= int(i.split('.')[0])
        text = self.line_num.create_text(25, y+18 if args else y, anchor = "nw", text = linenum+1 if args else linenum, fill = "#fff", font = ('Helvetica', 12))
        bbox = self.line_num.bbox(text)
        coord = self.line_num.coords(text)
        self.line_num.coords(text, 35-(bbox[2]-bbox[0]), coord[1])
        i = self.textArea.index('{0}+1line'.format(i))

    def delete_line_nums(self, *args):
        ...
            
    def get_end_linenumber(text):
        """Utility to get the last line's number in a Tk text widget."""
        return int(float(text.index('end-1c')))

    def ShowAbout(self):showinfo ("Vulgar", "made for sake of coding practice")

    def openFile(self):
        self.file = askopenfilename(defaultextension = " .txt", filetypes = [("All Files", "*.*"), ("Text Documents" , "*.txt"), ("Brainfuck files", "*.bf")])
        if self.file == " ":
            self.file = None
        else:
            self.self.title (os.path.basename(self.file) + " - Vulgar")
            self.textArea.delete(1.0, END)
            try:
                file = open(self.file, "r")
                self.textArea.insert(1.0, file.read())
                file.close()
            except Exception as e:
                showerror("An Error Occured", e)
        self.update_line_nums()
 
    def newFile(self):
        self.self.title("Untitled - Vulgar")
        self.file = None
        self.textArea.delete(1.0, END)

    def saveFile(self):
        if self.file == None:
            self.file = asksaveasfilename (initialfile = 'Untitled.bf', defaultextension = " .bf", filetypes = [("All Files", "*.*"), ("Text Documents", "* .txt"), ("Brainfuck files", "*.bf")])
            if self.file == " ":
                self.file == None
            else:
                file = open(self.file, "w+")
                file.write(self.textArea.get(1.0, END))
                file.close()
                self.self.title(os.path.basename(self.file) + " - Vulgar")
        else:
            file = open(self.file, "w+")
            file.write(self.textArea.get(1.0, END))
            file.close()
        self.update_line_nums()

    def SaveAs(self):
        self.file = asksaveasfilename (initialfile = 'Untitled.bf', defaultextension = " .bf", filetypes = [("All Files", "*.*"), ("Text Documents", "* .txt"), ("Brainfuck files", "*.bf", "*.b")])
        if self.file == " ":
            pass
        else:
            file = open(self.file, "w+")
            file.write(self.textArea.get(1.0, END))
            file.close()
            self.self.title(os.path.basename(self.file) + " - Vulgar")

    def undo(self):
        try:
            self.textArea.event_generate("<<Undo>>")
            self.update_line_nums()
            return "break"
        except Exception as e: showinfo("An Error Occured",e)

    def redo(self, event=None):
        try:
            self.textArea.event_generate("<<Redo>>")
            self.update_line_nums()
            return "break"
        except Exception as e: showinfo("An Error Occured", e)
    
    def cut(self):
        try:
            self.textArea.event.generate("<<Cut>>")
        except Exception as e:
            showerror("An Error Occured", e)
        self.update_line_nums()
    def copy(self):
        try:
            self.textArea.event.generate("<<Copy>>")
        except Exception as e:showerror("An Error Occured", e)

    def paste(self):
        try:
            self.textArea.event.generate("<<Paste>>")
        except Exception as e:showerror("An Error Occured", e)
        self.update_line_nums()

    def Setbg(self):
        useless, color = askcolor(title = "choose a background color")
        self.textArea.config(background = color)
        self.update_line_nums()
    
    def Setfg(self):
        useless, color = askcolor(title= "choose your text color")
        self.textArea.config(foreground = color)
        self.update_line_nums()

    def SetCurs(self):
        useless, color = askcolor(title = "choose your cursor's color")
        self.textArea.config(insertbackground = color)
        self.update_line_nums()
                
    def Run(self):
        code = self.textArea.get(0.0, END)
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '"', "'", '{', "}", '|', "/", "\ "]
        for i in code:
            if i.isdigit() or i.isalpha() is True or i in symbols:
                self.s = i 
                if self.s:
                    self.idx = '1.0'
                while 1:
                    self.idx = self.textArea.search(self.s, self.idx, nocase = 1, stopindex = END)
                    if not self.idx:break
                    self.lastidx = '%s+%dc' % (self.idx, len(self.s))
                    self.textArea.tag_add('found', self.idx, self.lastidx)
                    self.idx = self.lastidx
                self.textArea.tag_config('found', background = 'red')
                showerror("Error", "invalid syntax")
                self.textArea.tag_config('found', background = None)

        self.tabControl.select(self.tab2)
        output = brainfuck.evaluate(code)
        self.View.config(state = NORMAL)
        self.View.insert(END, str(output))#don't know why but it prints the output to your python shell instead 
        self.View.delete(0.0, END)
        self.View.insert(0.0, self.text)
        
        self.View.config(state = DISABLED)

if __name__=='__main__':
    Main().mainloop()

