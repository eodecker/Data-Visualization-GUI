# CS 251
# Spring 2019
# Eli Decker
# Project 4

import display
import tkinter as tk
import numpy as np

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

class EntryBox(Dialog):
    # You will need to override the body method and create the Entry widget there, 
    # using a StringVar object to handle setting and getting the text from the Entry widget.

    def __init__(self, parent, dataObject, title = None):
        self.minimum = 1
        self.maximum = 10
        self.hitCancel = True
        self.x = None
        self.y = None
        self.z = None
        self.colorOption = "Black"
        self.sizeOption = 10
        self.data = dataObject
        self.headers = self.data.get_headers()

        self.dataCols = []

        self.colorMenu = None
        self.xMenu = None
        self.yMenu = None
        self.zMenu = None
        self.sizeMenu = None
        self.colors = ["black", "blue", "red", "green"]
        self.sizes = ["5", "10", "15", "20", "25"]

        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)


        xLabel = tk.Label(frame, text="X", width=20)
        yLabel = tk.Label(frame, text="Y", width=20)
        zLabel = tk.Label(frame, text="Z", width=20)
        sizeLabel = tk.Label(frame2, text="Size", width=20)
        colorLabel = tk.Label(frame2, text="Color", width=20)

        self.colorMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)
        self.xMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.yMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.zMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.sizeMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)

        xLabel.pack(side=tk.TOP, pady=5)
        self.xMenu.pack(side=tk.TOP, padx=5)
        yLabel.pack(side=tk.TOP, pady=5)
        self.yMenu.pack(side=tk.TOP, padx=5)
        zLabel.pack(side=tk.TOP, pady=5)
        self.zMenu.pack(side=tk.TOP, padx=5)

        frame2.pack(side=tk.RIGHT)
        sizeLabel.pack(side=tk.TOP, pady=5)
        self.sizeMenu.pack(side=tk.TOP, padx=5)
        colorLabel.pack(side=tk.TOP, pady=5)
        self.colorMenu.pack(side=tk.TOP, padx=5)

        #color options
        
        # for color in self.colors:
        #     self.colorMenu.insert(tk.END, color)

        # for size in self.sizes:
        #     self.sizeMenu.insert(tk.END, size)
        
        for header in self.headers:
            self.xMenu.insert(tk.END, header)
            self.yMenu.insert(tk.END, header)
            self.zMenu.insert(tk.END, header)
            self.colorMenu.insert(tk.END, header)
            self.sizeMenu.insert(tk.END, header)


    def apply(self):
        xSelection = self.xMenu.curselection()
        if len(xSelection) > 0:
            self.dataCols.append(self.headers[xSelection[0]])
        ySelection = self.yMenu.curselection()
        if len(ySelection) > 0:
            self.dataCols.append(self.headers[ySelection[0]])
        zSelection = self.zMenu.curselection()
        if len(zSelection) > 0:
            self.dataCols.append(self.headers[zSelection[0]])
        else:
            self.dataCols.append(None)


        colorSelection = self.colorMenu.curselection()
        if len(colorSelection) > 0:
            self.dataCols.append(self.headers[colorSelection[0]])
        else:
            self.dataCols.append(None)
        sizeSelection = self.sizeMenu.curselection()
        if len(sizeSelection) > 0:
            self.dataCols.append(self.headers[sizeSelection[0]])
        else:
            self.dataCols.append(None)

    def getdataCols(self):
        return self.dataCols


            
    # returns number of points
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    def getColor(self):
        return self.colorOption
    def getSize(self):
        return self.sizeOption

    # tells whether user hit cancel button
    def userCancelled(self):
        if self.hitCancel:
            self.numPoints = 100
            return True
        else:
            self.numPoints = 100
            return False
class LinRegEntry(Dialog):
    # You will need to override the body method and create the Entry widget there, 
    # using a StringVar object to handle setting and getting the text from the Entry widget.

    def __init__(self, parent, dataObject, title = None):
        self.minimum = 1
        self.maximum = 10
        self.hitCancel = True
        self.x = None
        self.y = None
        self.colorOption = "Black"
        self.sizeOption = 10
        self.data = dataObject
        self.headers = self.data.get_headers()

        self.dataCols = []

        self.colorMenu = None
        self.xMenu = None
        self.yMenu = None
        self.sizeMenu = None
        self.colors = ["black", "blue", "red", "green"]
        self.sizes = ["5", "10", "15", "20", "25"]

        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)

        xLabel = tk.Label(frame, text="X", width=20)
        yLabel = tk.Label(frame, text="Y", width=20)

        self.xMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.yMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)

        xLabel.pack(side=tk.TOP, pady=5)
        self.xMenu.pack(side=tk.TOP, padx=5)
        yLabel.pack(side=tk.TOP, pady=5)
        self.yMenu.pack(side=tk.TOP, padx=5)
        
        for header in self.headers:
            self.xMenu.insert(tk.END, header)
            self.yMenu.insert(tk.END, header)


    def apply(self):
        xSelection = self.xMenu.curselection()
        if len(xSelection) > 0:
            self.dataCols.append(self.headers[xSelection[0]])
        ySelection = self.yMenu.curselection()
        if len(ySelection) > 0:
            self.dataCols.append(self.headers[ySelection[0]])


    def getdataCols(self):
        return self.dataCols
            
    # returns number of points
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getColor(self):
        return self.colorOption
    def getSize(self):
        return self.sizeOption

    # tells whether user hit cancel button
    def userCancelled(self):
        if self.hitCancel:
            self.numPoints = 100
            return True
        else:
            self.numPoints = 100
            return False
class PCAdialog(Dialog):
    def __init__(self, parent, dataObject, title = None):
        self.data = dataObject
        self.headers = self.data.get_headers()

        self.dataCols = []
        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)

        label = tk.Label(frame, text="Choose Headers for PCA Analysis", width=30)

        self.headerList = tk.Listbox( frame, selectmode=tk.MULTIPLE, exportselection=0)

        label.pack(side=tk.TOP, pady=5)
        self.headerList.pack(side=tk.TOP, padx=5)
        
        for header in self.headers:
            self.headerList.insert(tk.END, header)


    def apply(self):
        selection = self.headerList.curselection()
        if len(selection) > 0:
            for item in selection:
                self.dataCols.append(self.headers[item])

    def getdataCols(self):
        return self.dataCols

class PCAtable(Dialog):
    def __init__(self, parent, dataObject, title = None):
        self.data = dataObject
        self.headers = self.data.get_headers()
        self.pcadata = self.data.get_specific_col_data(self.headers)
        self.evec = self.data.get_eigenvectors()
        self.eval = self.data.get_eigenvalues()
        evalsum = np.sum(self.eval)
        counter = 0
        self.cumulativeList = []
        for item in self.eval:
            temp = item/evalsum
            counter = counter + temp
            self.cumulativeList.append(counter)

        Dialog.__init__(self, parent)

    def body(self, master):
        print("**********")
        print(self.evec)
        print("*****-------*****")
        print(self.eval)
        print(self.data.get_original_headers())
        # length = self.evec.shape[0]
        length = self.data.get_num_points()
        width = self.evec.shape[0]+1
        standardLabels = ["E-vec", "E-val", "Cumulative"]
        topLabels = standardLabels + self.data.get_original_headers()
        for i in range(self.evec.shape[0]): #Rows
            c = tk.Label(master, text="%s" % (self.headers[i]))
            c.grid(row=i+1,column=0)

            # val = tk.Label(master, text="%f" % (self.eval.item((i, j))))
            for j in range(len(topLabels)): #Columns
                label = tk.Label(master, text="%s" % (topLabels[j]))
                if j > 2:
                    b = tk.Label(master, text="%f" % (self.evec.item((i, j-3))))
                    b.grid(row=i+1, column=j)
                label.grid(row=0, column=j)
            vals = tk.Label(master, text="%f" % (self.eval.item((i))))
            vals.grid(row=i+1, column=1)
            cumulative = tk.Label(master, text="%f" % (self.cumulativeList[i]))
            cumulative.grid(row=i+1, column=2)


class PCAdialogPlot(Dialog):
    def __init__(self, parent, dataObject, title = None):
        self.data = dataObject
        self.headers = self.data.get_headers()

        self.dataCols = []
        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)


        xLabel = tk.Label(frame, text="X", width=20)
        yLabel = tk.Label(frame, text="Y", width=20)
        zLabel = tk.Label(frame, text="Z", width=20)
        sizeLabel = tk.Label(frame2, text="Size", width=20)
        colorLabel = tk.Label(frame2, text="Color", width=20)

        self.colorMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)
        self.xMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.yMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.zMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.sizeMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)

        xLabel.pack(side=tk.TOP, pady=5)
        self.xMenu.pack(side=tk.TOP, padx=5)
        yLabel.pack(side=tk.TOP, pady=5)
        self.yMenu.pack(side=tk.TOP, padx=5)
        zLabel.pack(side=tk.TOP, pady=5)
        self.zMenu.pack(side=tk.TOP, padx=5)

        frame2.pack(side=tk.RIGHT)
        sizeLabel.pack(side=tk.TOP, pady=5)
        self.sizeMenu.pack(side=tk.TOP, padx=5)
        colorLabel.pack(side=tk.TOP, pady=5)
        self.colorMenu.pack(side=tk.TOP, padx=5)

        #color options
        
        # for color in self.colors:
        #     self.colorMenu.insert(tk.END, color)

        # for size in self.sizes:
        #     self.sizeMenu.insert(tk.END, size)
        
        for header in self.headers:
            self.xMenu.insert(tk.END, header)
            self.yMenu.insert(tk.END, header)
            self.zMenu.insert(tk.END, header)
            self.colorMenu.insert(tk.END, header)
            self.sizeMenu.insert(tk.END, header)


    def apply(self):
        xSelection = self.xMenu.curselection()
        if len(xSelection) > 0:
            self.dataCols.append(self.headers[xSelection[0]])
        ySelection = self.yMenu.curselection()
        if len(ySelection) > 0:
            self.dataCols.append(self.headers[ySelection[0]])
        zSelection = self.zMenu.curselection()
        if len(zSelection) > 0:
            self.dataCols.append(self.headers[zSelection[0]])
        else:
            self.dataCols.append(None)


        colorSelection = self.colorMenu.curselection()
        if len(colorSelection) > 0:
            self.dataCols.append(self.headers[colorSelection[0]])
        else:
            self.dataCols.append(None)
        sizeSelection = self.sizeMenu.curselection()
        if len(sizeSelection) > 0:
            self.dataCols.append(self.headers[sizeSelection[0]])
        else:
            self.dataCols.append(None)

    def getdataCols(self):
        return self.dataCols

class ClusterDialog(Dialog):
    def __init__(self, parent, dataObject, title = None):
        self.data = dataObject
        self.headers = self.data.get_headers()

        self.dataCols = []
        self.numClusters = 0
        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)

        label = tk.Label(frame, text="Choose Headers for Cluster Analysis", width=30)

        self.headerList = tk.Listbox( frame, selectmode=tk.MULTIPLE, exportselection=0)

        label.pack(side=tk.TOP, pady=5)
        self.headerList.pack(side=tk.TOP, padx=5)
        
        for header in self.headers:
            self.headerList.insert(tk.END, header)

        tk.Label(frame, text="How Many Clusters Do You Want?", width=30).pack(side=tk.TOP, pady=5)
        self.numClustersEntry = tk.Entry(frame)
        self.numClustersEntry.pack(side=tk.TOP, pady=5)

    def apply(self):
        selection = self.headerList.curselection()
        if len(selection) > 0:
            for item in selection:
                self.dataCols.append(self.headers[item])
        if self.numClustersEntry != None:
            self.numClusters = self.numClustersEntry.get()

    def getdataCols(self):
        return self.dataCols
    def getNumClusters(self):
        return self.numClusters


class ClusterDialogPlot(Dialog):
    def __init__(self, parent, dataObject, title = None):
        self.data = dataObject
        self.headers = self.data.get_original_headers()

        self.dataCols = []
        Dialog.__init__(self, parent)

    def body(self, master):
        frame = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame.pack(side=tk.LEFT)


        xLabel = tk.Label(frame, text="X", width=20)
        yLabel = tk.Label(frame, text="Y", width=20)
        zLabel = tk.Label(frame, text="Z", width=20)
        sizeLabel = tk.Label(frame2, text="Size", width=20)
        colorLabel = tk.Label(frame2, text="Color", width=20)

        self.colorMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)
        self.xMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.yMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.zMenu = tk.Listbox( frame, selectmode=tk.SINGLE, exportselection=0)
        self.sizeMenu = tk.Listbox( frame2, selectmode=tk.SINGLE, exportselection=0)

        xLabel.pack(side=tk.TOP, pady=5)
        self.xMenu.pack(side=tk.TOP, padx=5)
        yLabel.pack(side=tk.TOP, pady=5)
        self.yMenu.pack(side=tk.TOP, padx=5)
        zLabel.pack(side=tk.TOP, pady=5)
        self.zMenu.pack(side=tk.TOP, padx=5)

        frame2.pack(side=tk.RIGHT)
        sizeLabel.pack(side=tk.TOP, pady=5)
        self.sizeMenu.pack(side=tk.TOP, padx=5)
        colorLabel.pack(side=tk.TOP, pady=5)
        self.colorMenu.pack(side=tk.TOP, padx=5)

        #color options
        
        # for color in self.colors:
        #     self.colorMenu.insert(tk.END, color)

        # for size in self.sizes:
        #     self.sizeMenu.insert(tk.END, size)
        
        for header in self.headers:
            self.xMenu.insert(tk.END, header)
            self.yMenu.insert(tk.END, header)
            self.zMenu.insert(tk.END, header)
            self.colorMenu.insert(tk.END, header)
            self.sizeMenu.insert(tk.END, header)


    def apply(self):
        xSelection = self.xMenu.curselection()
        if len(xSelection) > 0:
            self.dataCols.append(self.headers[xSelection[0]])
        ySelection = self.yMenu.curselection()
        if len(ySelection) > 0:
            self.dataCols.append(self.headers[ySelection[0]])
        zSelection = self.zMenu.curselection()
        if len(zSelection) > 0:
            self.dataCols.append(self.headers[zSelection[0]])
        else:
            self.dataCols.append(None)


        colorSelection = self.colorMenu.curselection()
        if len(colorSelection) > 0:
            self.dataCols.append(self.headers[colorSelection[0]])
        else:
            self.dataCols.append(None)
        sizeSelection = self.sizeMenu.curselection()
        if len(sizeSelection) > 0:
            self.dataCols.append(self.headers[sizeSelection[0]])
        else:
            self.dataCols.append(None)

    def getdataCols(self):
        return self.dataCols