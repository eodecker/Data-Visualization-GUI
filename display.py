# CS 251
# Spring 2019
# Eli Decker
# Project 4

import tkinter as tk
import math
import random
import numpy as np
import view
import os

import data
from tkinter import filedialog
import dialog
import analysis
from PIL import ImageGrab

import datetime as dt


# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        self.normalizeCheckBox = tk.IntVar()

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("Viewing Axes")

        # set the maximum size of the window for resizing
        self.root.maxsize( 1024, 768 )

        # bring the window to the front
        self.root.lift()

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the objects on the Canvas
        self.buildCanvas()

        # set up the key bindings
        self.setBindings()


        self.baseClick1 = None # used to keep track of mouse movement
        self.baseClick2 = None # used to keep track of mouse movement
        self.baseClick3 = None # used to keep track of mouse movement
        self.button2Clone = None
        self.tempExtent = None

        # Create a View object and set up the default parameters
        self.view = view.View()

        #create field to hold a list that contains the actual graphics line objects that instantiate them on the screen
        self.lines = []
        self.xaxis = None
        self.yaxis = None
        self.zaxis = None

        # Create the axes fields and build the axes
        self.axes = np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])
        # set up the application state
        self.objects = []
        self.dataColor = "Black"
        self.dataSize = 5
        self.data = None
        self.spatialMatrix = None
        self.dialogBox = None
        self.labels = []
        self.means = None
        self.buildAxes()

        # -------- Project 5 stuff ---------
        # the graphical objects associated with a linear regression (i.e. one or more tk Line objects)
        self.linRegression_objects = []
        # the endpoints of the regression line in normalized data space (e.g. a numpy matrix or a 2-D list).
        self.linReg_endpoints = None
        self.regLineTextString = ""
        self.pcaDialog = None
        self.pcaMenu = None
        self.PCAselection = None
        self.pcaDict = {}
        self.fn = None
        self.pcaDialogPlot = None

        self.clusterColors = None
        self.codes = None
        self.index = 0
        self.stopButton = False
        self.columnName = None
        

    def buildMenus(self):
        
        # create a new menu
        self.menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = self.menu)

        # create a variable to hold the individual menus
        self.menulist = []

        # create a file menu
        filemenu = tk.Menu( self.menu )
        self.menu.add_cascade( label = "File", menu = filemenu )
        self.menulist.append(filemenu)


        # menu text for the elements
        menutext = [ [ 'Open...  \xE2\x8C\x98-O', '-', 'Quit  \xE2\x8C\x98-Q' ] ]

        # menu callback functions
        menucmd = [ [self.handleOpen, None, self.handleQuit]  ]
        
        # build the menu elements and callbacks
        for i in range( len( self.menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    self.menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    self.menulist[i].add_separator()

    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
        return

    # build a frame and put controls in it
    def buildControls(self):

        # make a control frame
        self.cntlframe = tk.Frame(self.root)
        self.cntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # make a cmd 1 button in the frame
        self.buttons = []
        self.buttons.append( ( 'plotData', tk.Button( self.cntlframe, text="Plot Data", command=self.handlePlotData, width=10 ) ) )
        self.buttons.append( ( 'clear', tk.Button( self.cntlframe, text="Clear Data", command=self.handleClear, width=10 ) ) )
        self.buttons.append( ( 'linReg', tk.Button( self.cntlframe, text="Linear \n Regression", command=self.handleLinearRegression, width=10 ) ) )
        self.buttons.append( ( 'imgCapture', tk.Button( self.cntlframe, text="Take Picture", command=self.handleImageCapture, width=10 ) ) )
        self.buttons.append( ( 'PCA', tk.Button( self.cntlframe, text="PCA Analysis", command=self.handlePCA, width=10 ) ) )
        self.buttons.append( ( 'Cluster Analysis', tk.Button( self.cntlframe, text="Cluster Analysis", command=self.handleCluster, width=10 ) ) )
        self.buttons.append( ('checkbox',tk.Checkbutton(self.cntlframe, text="Normalize", variable=self.normalizeCheckBox) ) )
        self.buttons.append( ('runSim',tk.Button(self.cntlframe, text="Run \n Simulation", command=self.handleSimulation, width=10, foreground="Green") ) )
        self.buttons.append( ('stop',tk.Button(self.cntlframe, text="Stop \n Simulation", command=self.handleStop, width=10, foreground="Red") ) )
        self.buttons.append( ('resume',tk.Button(self.cntlframe, text="Resume \n Simulation", command=self.resumeAnimation, width=10) ) )
        self.buttons.append( ( 'reset', tk.Button( self.cntlframe, text="Reset View", command=self.handleResetButton, width=10 ) ) )


        self.buttons[-1][1].pack(side=tk.TOP)  # default side is top
        self.buttons[0][1].pack(side=tk.TOP)
        self.buttons[1][1].pack(side=tk.TOP)
        self.buttons[2][1].pack(side=tk.TOP)
        self.buttons[3][1].pack(side=tk.TOP)
        self.buttons[4][1].pack(side=tk.TOP)
        self.buttons[5][1].pack(side=tk.TOP)
        self.buttons[6][1].pack(side=tk.TOP)
        self.buttons[7][1].pack(side=tk.TOP)
        self.buttons[8][1].pack(side=tk.TOP)
        self.buttons[9][1].pack(side=tk.TOP)

        return

    # create the axis line objects in their default location
    def buildAxes(self):
        vtm = self.view.build()
        pts = (vtm * self.axes.T).T
        #create the line objects
        self.xaxis = self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1])
        self.yaxis = self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1])
        self.zaxis = self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1])

        self.xaxislabel = self.canvas.create_text(pts[1,0],pts[1,1],text="X (unassigned)")
        self.yaxislabel = self.canvas.create_text(pts[3,0],pts[3,1],text="Y (unassigned)")
        self.zaxislabel = self.canvas.create_text(pts[5,0],pts[5,1],text="Z (unassigned)")


        self.canvas.itemconfig(self.xaxis, fill="blue") # change color
        self.canvas.itemconfig(self.yaxis, fill="red") # change color
        self.canvas.itemconfig(self.zaxis, fill="green") # change color
        
        # add the lines to the list of lines
        self.lines.append(self.xaxis)
        self.lines.append(self.yaxis)
        self.lines.append(self.zaxis)

        self.labels.append(self.xaxislabel)
        self.labels.append(self.yaxislabel)
        self.labels.append(self.zaxislabel)


     # modify the endpoints of the axes to their new location
    def updateAxes(self):
        # build the VTM
        vtm = self.view.build()
        # multiply the axis endpoints by the VTM
        pts = (vtm * self.axes.T).T
        self.labels.clear()

        self.canvas.itemconfig(self.xaxislabel, text=self.handleChooseAxes()[0])
        self.canvas.itemconfig(self.yaxislabel, text=self.handleChooseAxes()[1])
        if len(self.handleChooseAxes()) > 2:
            self.canvas.itemconfig(self.zaxislabel, text=self.handleChooseAxes()[2])
        self.labels.append(self.xaxislabel)
        self.labels.append(self.yaxislabel)
        self.labels.append(self.zaxislabel)

        for i in range(len(self.lines)):
            self.canvas.coords(self.lines[i], pts[2*i, 0], pts[2*i,1], pts[(2*i)+1,0],pts[(2*i)+1,1])
            self.canvas.coords(self.labels[i], pts[(2*i)+1,0],pts[(2*i)+1,1])

        self.updatePoints()
        if self.linRegression_objects != []:
            self.updateFits()




    def setBindings(self):
        self.canvas.bind( '<Button-1>', self.handleButton1 )
        self.canvas.bind( '<Button-2>', self.handleButton2 )
        self.canvas.bind( '<Shift-Button-1>', self.handleMark )
        self.canvas.bind( '<Button-3>', self.handleButton3)
        self.canvas.bind( '<Control-Button-1>', self.handleButton2 )
        self.canvas.bind( '<Option-Button-1>', self.handleButton3 )
        self.canvas.bind( '<B1-Motion>', self.handleButton1Motion )
        self.canvas.bind( '<B2-Motion>', self.handleButton2Motion )
        self.canvas.bind( '<Control-B1-Motion>', self.handleButton2Motion )
        self.canvas.bind( '<Option-B1-Motion>', self.handleButton3Motion )
        
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Command-o>', self.handleOpen )
        self.canvas.bind( '<Configure>', self.handleResize )
        return

    def handleResize(self, event=None):
        # You can handle resize events here
        pass

    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()

    def handleResetButton(self):
        print('handling reset button')
        self.view.reset()
        self.updateAxes()

    def handleButton1(self, event):
        self.baseClick1 = (event.x, event.y)
        # for obj in self.objects:
        #     loc = self.canvas.coords(obj)
        #     #if the click happens within the dimensions of a data point
        #     if ( loc[0] < event.x < loc[2] ) and ( loc[1] < event.y < loc[3] ):
        #         self.objects.remove(obj)
        #         self.canvas.delete(obj)
        #         print( 'Deleted point at: %d %d' % (event.x, event.y))

    # handles right click
    def handleButton2(self, event):
        self.baseClick2 = (event.x, event.y)
        self.button2Clone = self.view.clone()
    # marks a data point
    def handleMark(self, event):
        pass
        # for obj in self.objects:
        #     loc = self.canvas.coords(obj)
        #     #if the click happens within the dimensions of a data point
        #     if ( loc[0] < event.x < loc[2] ) and ( loc[1] < event.y < loc[3] ):
        #         self.canvas.itemconfig(obj, fill="orange") # change color
        #         print( 'Marked point at: %d %d' % (event.x, event.y))

    # scaling
    def handleButton3(self, event):
        """Button 3 motion should implement scaling. The scaling behavior should act like a vertical lever. 
        The button 3 click should store a base click point that does not change while the user holds down the mouse button. 
        It should also store the value of the extent in the view space when the user clicked. 
        This is the original extent. Make sure you create a copy and not a reference 
        to the extent value (you could use the View clone function)."""
        self.baseClick3 = (event.x, event.y)
        clone = self.view.clone()
        self.tempExtent = clone.extent

    # translation
    def handleButton1Motion(self, event):
        # Calculate the differential motion since the last time the function was called
        diff = ( event.x - self.baseClick1[0], event.y - self.baseClick1[1] )
        # Divide the differential motion (dx, dy) by the screen size (view X, view Y)
        diff = (diff[0] / self.view.screen[0]), (diff[1] / self.view.screen[1])

        # Multiply the horizontal and vertical motion by the horizontal and vertical extents.
        # Put the result in delta0 and delta1
        delta0 = diff[0] * self.view.extent[0]
        delta1 = diff[1] * self.view.extent[1]
        # The VRP should be updated by delta0 * U + delta1 * VUP (this is a vector equation)
        self.view.vrp += delta0 * self.view.u + delta1 * self.view.vup
        self.baseClick1 = (event.x, event.y)

        # call updateAxes()
        self.updateAxes()

        
        
    
        
    
    def handleButton2Motion(self, event):
        """Within the button2motion function, first calculate delta0 and delta1 as the pixel motion differences
        in x and y divided by a constant (e.g. 200) and multiplied by pi (math.pi). 
        Think of it as how many pixels the user must move the mouse to execute a 180 degree rotation. """
        w = min(self.view.screen)
        dx = float(event.x - self.baseClick2[0]) / (0.5 * w)*np.pi
        dy = float(event.y - self.baseClick2[1]) / (0.5 * w)*np.pi
        self.view = self.button2Clone.clone()
        self.view.rotateVRC(-dx, dy)

        self.updateAxes()

    def handleButton3Motion( self, event):
        """The button 3 motion should convert the distance between the base click and the current mouse position 
        into a scale factor. Keep the scale factor between 0.1 and 3.0. You can then multiply the original extent
        by the factor and put it into the View object. Then call updateAxes(). 
        Do not modify the original extent while the mouse is in motion."""

        # calculate the difference
        diff = float(( event.y - self.baseClick3[1] ) / self.root.winfo_screenheight())
        scaleRate = 1.0
        scaleFactor = (1 + scaleRate*diff )
        scaleFactor = np.max([scaleFactor, 0.1])
        scaleFactor = np.min([scaleFactor, 3.0])
        self.view.extent = []
        for item in self.tempExtent:
            self.view.extent.append(item*scaleFactor)
        
        self.updateAxes()

    # ---------------- Project 4 stuff below ---------------------
    def handleClear(self):
        print("Clearing Data")
        self.clearData()


    def clearData(self, event=None):
        for obj in self.objects:
            self.canvas.delete(obj)
        self.objects.clear()

    def handleChooseAxes(self):
        if self.dialogBox != None:
            return self.dialogBox.getdataCols()
        else:
            return self.pcaDialogPlot.getdataCols()

    def handleOpen( self, event ):
        """Uses the tkFileDialog module to let the user select the csv file they want to open."""
        self.fn = filedialog.askopenfilename( parent=self.root, 
            title='Choose a data file', initialdir='.' )
        # Make a Data object to read and hold the file's data. You will need to keep this around for plotting,
        # so the Data object needs to be a field of your Display class. For now, your program needs to support 
        # having only one data file open at a time.
        self.data = data.Data( self.fn )

    def handlePlotData(self):
        """Enables the user to select which columns of data to plot on which axes and then builds the data."""
        self.dialogBox = dialog.EntryBox(self.root, self.data)
        headers = self.handleChooseAxes()
        self.buildPoints(headers)

    def buildColors(self, headers):
        pass
        # should return a list of colors
        # get norm data
        # map data color
        # color[i] = (1 - data[i]*C0 + data[i]*C1)

    def buildSizes(self, headers):
        pass
        # should return a list of colors
        # get norm data
        # map data color
        # color[i] = (1 - data[i]*C0 + data[i]*C1)


    def buildPoints(self, headers):
        """Builds the data"""

        #the x,y,z mappings
        cols = headers[0:3]

        # Delete any existing canvas objects used for plotting data. Delete them from the canvas 
        # and set your list of data graphics objects to the empty list.
        self.clearData()
        # Get the spatial (x, y, z) columns specified by the argument headers to plot. 
        # Use your normalize_columns_separately function in analysis. 
        # If you are selecting only 2 columns to plot, add a column of 0's (z-value) and 
        # a column of 1's (homogeneous coordinate) to the data. If you are selecting 3 columns to plot, 
        # add a column of 1's (homogeneous coordinate). Each data point is now represented as a 
        # 4-column row in the spatial data matrix. Make sure this data is stored in a field of the display class. 
        # Do not change this matrix until the user clicks on plotData again.
        
        if cols[2] != None:
            normalizedMatrix = analysis.normalize_columns_separately(cols, self.data)
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, ones))
        elif cols[2] == None:
            normalizedMatrix = analysis.normalize_columns_separately(cols[0:2], self.data)
            zeros = np.zeros((normalizedMatrix.shape[0],1))
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))

        #color of data points
        if headers[3] != None:
            self.dataColor = analysis.normalize_columns_separately([headers[3]], self.data)
        else:
            self.dataColor = np.ones((normalizedMatrix.shape[0],1))
        #size of the data points
        if headers[4] != None:
            self.dataSize = analysis.normalize_columns_separately([headers[4]], self.data)
        else:
            self.dataSize = np.ones((normalizedMatrix.shape[0],1))

        # Calculate the VTM using the current view object.
        vtm = self.view.build()

        # Transform the data using the VTM (the following assumes each data point is a row).
        pts = (vtm *self.spatialMatrix.T).T
        self.means = pts.mean(axis=0)

        # Create the canvas graphics objects, ovals/squares/crosses/points, 
        # for each data point using the X and Y (first two columns) of your transformed points. 
        # Be sure to save a reference to each data point object drawn on the screen (e.g. in self.objects). 
        # Letting the user specify the type of graphics object (circle, square, cross) to use in the plot is a nice extension.
        for i in range(0,pts.shape[0]):
            dx = 5 * self.dataSize[i,0]
            pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                fill = "#%02x%02x%02x" % (int(255*self.dataColor[i,0]), 0, int(255*(1-self.dataColor[i,0]))), outline='' )

            self.objects.append(pt)

    def updatePoints(self):
        self.clearData()

        vtm = self.view.build()

        pts = (vtm *self.spatialMatrix.T).T
        self.means = pts.mean(axis=0)

        for i in range(0,pts.shape[0]):
            dx = 5 * self.dataSize[i,0]
            if self.clusterColors != None:
                pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                        fill = self.clusterColors[self.codes[i,0]], outline='' )
            else:
                pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                        fill = "#%02x%02x%02x" % (int(255*self.dataColor[i,0]), 0, int(255*(1-self.dataColor[i,0]))), outline='' )

            self.objects.append(pt)

    # -------Project 5 Stuff ----------
    def clearModels(self):
        for obj in self.linRegression_objects:
            self.canvas.delete(obj)
        self.linRegression_objects.clear()

    def handleLinearRegression(self):
        self.dialogBox = dialog.LinRegEntry(self.root, self.data)
        self.clearData()
        self.clearModels()
        self.view.reset()
        self.buildLinearRegression()
        self.updateAxes()
    
    def updateFits(self):
        # build the VTM
        vtm = self.view.build()
        # multiply the axis endpoints by the VTM
        endPts = (vtm * self.linReg_endpoints.T).T
        self.clearModels()

        regLine = self.canvas.create_line(endPts[0,0],endPts[0,1],endPts[1,0],endPts[1,1])
        self.canvas.itemconfig(regLine, fill="cyan") # change color
        regLineText = self.canvas.create_text(endPts[1,0],endPts[1,1],text=self.regLineTextString)

        self.linRegression_objects.append(regLine)
        self.linRegression_objects.append(regLineText)

    def buildLinearRegression(self):
        """Builds a linear regression line based on the two variables user selected from dialog box
        """
        colChoices = self.dialogBox.getdataCols()
        # for choice in choices:
        # 	values = self.data.get_specific_col_data(choice)
        # analysis.normalize_columns_separately(choices, self.data)
        normalizedMatrix = analysis.normalize_columns_separately(colChoices, self.data)
        zeros = np.zeros((normalizedMatrix.shape[0],1))
        ones = np.ones((normalizedMatrix.shape[0],1))
        self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))
        # Build the vtm, multiply it by the data points, and then create the ovals to plot the data on the screen. 
        # This should make a 2-D plot of the two variables, with the independent variable along the x-axis. 
        vtm = self.view.build()
        pts = (vtm *self.spatialMatrix.T).T

        self.dataSize = np.ones((normalizedMatrix.shape[0],1))
        self.dataColor = np.ones((normalizedMatrix.shape[0],1))

        for i in range(0,pts.shape[0]):
            dx = 5 * self.dataSize[i,0]
            pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                    fill = "#%02x%02x%02x" % (int(255*self.dataColor[i,0]), 0, int(255*(1-self.dataColor[i,0]))), outline='' )

            self.objects.append(pt)

        results = analysis.single_linear_regression( self.data, colChoices[0], colChoices[1])
        m = results[0]
        b = results[1]
        rval = results[2]
        xmin = results[5][0,0]
        xmax = results[6][0,0]
        ymin = results[5][0,1]
        ymax = results[6][0,1]
        y1 = ((xmin * m + b) - ymin)/(ymax - ymin)
        y2 = ((xmax * m + b) - ymin)/(ymax - ymin)
        # In normalized space, the x values of the endpoints will be 0.0 and 1.0
        x1 = 0.0
        x2 = 1.0
        self.linReg_endpoints = np.matrix([[x1,y1,0,1],[x2,y2,0,1]])
        endPts = (vtm * self.linReg_endpoints.T).T
        #create the line objects
        regLine = self.canvas.create_line(endPts[0,0],endPts[0,1],endPts[1,0],endPts[1,1])
        self.canvas.itemconfig(regLine, fill="cyan") # change color
        self.regLineTextString = "Slope: "+str(m) + "\n Intercept: "+str(b) + "\n R-value: " + str(rval)
        regLineText = self.canvas.create_text(endPts[1,0],pts[1,1],text=self.regLineTextString)
        self.linRegression_objects.append(regLine)
        self.linRegression_objects.append(regLineText)

    def handleImageCapture(self):
        x=100
        y=100
        x1=1500
        y1=1100
        ImageGrab.grab().crop((x,y,x1,y1)).save("testImage.ppm")

    def handlePCA(self):
        '''action button for performing PCA analysis on data'''
        print("PCA Analysis Button Clicked")
        self.pcaDialog = dialog.PCAdialog(self.root, self.data)
        chosenHeaders = self.pcaDialog.getdataCols()
        pcaName = "%s%s" % (os.path.basename(self.fn), chosenHeaders)
        print(self.normalizeCheckBox.get())
        if self.normalizeCheckBox.get() == 1:
            pcadata = analysis.pca( self.data, chosenHeaders, True)
        else:
            pcadata = analysis.pca( self.data, chosenHeaders, False)

        if self.pcaMenu == None:
            self.pcaMenu = tk.Listbox( self.cntlframe, selectmode=tk.SINGLE, exportselection=0)
            self.pcaMenu.pack(side=tk.TOP, padx=5)
            self.pcaMenu.insert(tk.END, pcaName)
            self.pcaDict[pcaName] = pcadata

            tk.Button( self.cntlframe, text="Delete PCA Analysis", command=self.deletePCAanalysis, width=20 ).pack(side=tk.BOTTOM, padx=5)
            tk.Button( self.cntlframe, text="Show PCA Table", command= lambda: self.showPCAtable(pcadata), width=20 ).pack(side=tk.BOTTOM, padx=5)
            tk.Button( self.cntlframe, text="Plot Analysis (PCA / Cluster)", command=self.handlePlotPCA, width=20 ).pack(side=tk.BOTTOM, padx=5)
        else:
            self.pcaMenu.insert(tk.END, pcaName)
            self.pcaDict[pcaName] = pcadata

        self.PCAselection = self.pcaMenu.curselection()
        return pcadata

    def handleCluster(self):
        '''action button for performing PCA analysis on data'''
        print("Cluster Analysis Button Clicked")
        self.clusterDialog = dialog.ClusterDialog(self.root, self.data)
        chosenHeaders = self.clusterDialog.getdataCols()
        numClusters = int(self.clusterDialog.getNumClusters())
        clusterName = "%s%s" % (os.path.basename(self.fn), chosenHeaders)
        if self.normalizeCheckBox.get() == 1:
            clusterdata = analysis.kmeans( self.data, chosenHeaders, numClusters, True)
        else:
            clusterdata = analysis.kmeans( self.data, chosenHeaders, numClusters, False)

        if self.pcaMenu == None:
            self.pcaMenu = tk.Listbox( self.cntlframe, selectmode=tk.SINGLE, exportselection=0)
            self.pcaMenu.pack(side=tk.TOP, padx=5)
            self.pcaMenu.insert(tk.END, clusterName)
            self.pcaDict[clusterName] = clusterdata

            tk.Button( self.cntlframe, text="Delete PCA Analysis", command=self.deletePCAanalysis, width=20 ).pack(side=tk.BOTTOM, padx=5)
            tk.Button( self.cntlframe, text="Show PCA Table", command= lambda: self.showPCAtable(clusterdata), width=20 ).pack(side=tk.BOTTOM, padx=5)
            tk.Button( self.cntlframe, text="Plot Analysis (PCA / Cluster)", command=self.handlePlotCluster, width=20 ).pack(side=tk.BOTTOM, padx=5)
        else:
            self.pcaMenu.insert(tk.END, clusterName)
            self.pcaDict[clusterName] = clusterdata

        self.PCAselection = self.pcaMenu.curselection()
        print(analysis.kmeans_quality(clusterdata.get_errors(), clusterdata.get_K()) )
        # return clusterdata

    def deletePCAanalysis(self):
        if self.PCAselection != None:
            self.pcaMenu.delete(tk.ANCHOR)

    def showPCAtable(self, dataObj):
        if self.PCAselection != None:
            name = self.pcaMenu.get(tk.ACTIVE)
            pcaD = self.pcaDict[name]
            self.pcaDialog = dialog.PCAtable(self.root, pcaD)

    def handlePlotPCA(self):
        if self.PCAselection != None:
            name = self.pcaMenu.get(tk.ACTIVE)
            pcaD = self.pcaDict[name]

            self.pcaDialogPlot = dialog.PCAdialogPlot(self.root, pcaD)
            self.headers = self.pcaDialogPlot.getdataCols()

            # pcaD.get_headers()
            self.plotPCA(pcaD)

    def handlePlotCluster(self):
        if self.PCAselection != None:
            name = self.pcaMenu.get(tk.ACTIVE)
            pcaD = self.pcaDict[name]

            self.pcaDialogPlot = dialog.ClusterDialogPlot(self.root, pcaD)
            self.headers = self.pcaDialogPlot.getdataCols()

            # pcaD.get_headers()
            self.plotCluster(pcaD)

    def plotPCA(self, pcaDataObj):
        headers = self.headers
        cols = self.headers[0:3]

        if cols[2] != None:
            normalizedMatrix = analysis.normalize_columns_separately(cols, pcaDataObj)
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, ones))
        elif cols[2] == None:
            normalizedMatrix = analysis.normalize_columns_separately(cols[0:2], pcaDataObj)
            zeros = np.zeros((normalizedMatrix.shape[0],1))
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))

        #color of data points
        if headers[3] != None:
            self.dataColor = analysis.normalize_columns_separately([headers[3]], pcaDataObj)
        else:
            self.dataColor = np.ones((normalizedMatrix.shape[0],1))
        #size of the data points
        if headers[4] != None:
            self.dataSize = analysis.normalize_columns_separately([headers[4]], pcaDataObj)
        else:
            self.dataSize = np.ones((normalizedMatrix.shape[0],1))

        vtm = self.view.build()

        # Transform the data using the VTM (the following assumes each data point is a row).
        pts = (vtm *self.spatialMatrix.T).T

        # Create the canvas graphics objects, ovals/squares/crosses/points, 
        # for each data point using the X and Y (first two columns) of your transformed points. 
        # Be sure to save a reference to each data point object drawn on the screen (e.g. in self.objects). 
        # Letting the user specify the type of graphics object (circle, square, cross) to use in the plot is a nice extension.
        for i in range(0,pts.shape[0]):
            dx = 5 * self.dataSize[i,0]
            pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                        fill = "#%02x%02x%02x" % (int(255*self.dataColor[i,0]), 0, int(255*(1-self.dataColor[i,0]))), outline='' )

            self.objects.append(pt)

    def plotCluster(self, clusterDataObj):
        colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', 
                    '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', 
                    '#000075', '#808080', '#000000']
        headers = self.headers
        cols = self.headers[0:3]

        if cols[2] != None:
            normalizedMatrix = analysis.normalize_columns_separately(cols, clusterDataObj)
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, ones))
        elif cols[2] == None:
            normalizedMatrix = analysis.normalize_columns_separately(cols[0:2], clusterDataObj)
            zeros = np.zeros((normalizedMatrix.shape[0],1))
            ones = np.ones((normalizedMatrix.shape[0],1))
            self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))

        #color of data points
        if headers[3] != None:
            self.dataColor = analysis.normalize_columns_separately([headers[3]], clusterDataObj)
        else:
            self.dataColor = np.ones((normalizedMatrix.shape[0],1))
        #size of the data points
        if headers[4] != None:
            self.dataSize = analysis.normalize_columns_separately([headers[4]], clusterDataObj)
        else:
            self.dataSize = np.ones((normalizedMatrix.shape[0],1))

        vtm = self.view.build()

        # Transform the data using the VTM (the following assumes each data point is a row).
        pts = (vtm *self.spatialMatrix.T).T

        # Create the canvas graphics objects, ovals/squares/crosses/points, 
        # for each data point using the X and Y (first two columns) of your transformed points. 
        # Be sure to save a reference to each data point object drawn on the screen (e.g. in self.objects). 
        # Letting the user specify the type of graphics object (circle, square, cross) to use in the plot is a nice extension.
        k = clusterDataObj.get_K()
        random.shuffle(colors)
        self.clusterColors = colors[0:k]
        self.codes = clusterDataObj.get_codes()

        for i in range(0,pts.shape[0]):
            dx = 5 * self.dataSize[i,0]
            pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                        fill = self.clusterColors[self.codes[i,0]], outline='' )

            self.objects.append(pt)


    def handleSimulation(self):

        print("Running Simulation")

        colors = ["#800000", "#f58231", "#4363d8", "#3cb44b"]
        chosenHeaders = self.data.get_headers()
        xyColumns = chosenHeaders[0:2]
        animatedColumns = chosenHeaders[3:]

        numClusters = 4

        clusterDataObj = analysis.kmeans( self.data, animatedColumns[0], numClusters, True)
        self.columnName = self.canvas.create_text(200, 450 ,text="Column: %s" % (animatedColumns[0]))

        self.headers = clusterDataObj.get_original_headers()

        normalizedMatrix = analysis.normalize_columns_separately(xyColumns, self.data)
        zeros = np.zeros((normalizedMatrix.shape[0],1))
        ones = np.ones((normalizedMatrix.shape[0],1))
        self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))


        vtm = self.view.build()
        pts = (vtm *self.spatialMatrix.T).T

        self.index = 0

        nextTick = dt.datetime.now() + dt.timedelta(seconds=5)
        self.root.after(100, self.animatePoints, animatedColumns, numClusters, colors, pts, nextTick)

    def animatePoints(self, animatedColumns, numClusters, colors, pts, nextTick):
        self.clearData()

        clusterDataObj = analysis.kmeans( self.data, animatedColumns[self.index], numClusters, True)
        self.canvas.itemconfig(self.columnName, text="Column: %s" % (animatedColumns[self.index]))

        k = clusterDataObj.get_K()
        random.shuffle(colors)
        self.clusterColors = colors[0:k]
        self.codes = clusterDataObj.get_codes()

        for i in range(0,pts.shape[0]):
            dx = 8
            pt = self.canvas.create_oval( pts[i,0]-int(dx), pts[i,1]-int(dx), pts[i,0]+int(dx), pts[i,1]+int(dx),
                                        fill = self.clusterColors[self.codes[i,0]], outline='' )

            self.objects.append(pt)
        
        self.index += 1
        if self.index == len(animatedColumns):
            return None
        now = dt.datetime.now()
        delay = (nextTick - now).total_seconds() * 1000
        nextTick += dt.timedelta(seconds=5)
        if self.stopButton:
            self.stopButton = False
            print("Stop Button Pressed")
            return None

        else:
            self.root.after(5, self.animatePoints, animatedColumns, numClusters, colors, pts, nextTick)

    def resumeAnimation(self):
        print("Resuming Simulation")

        colors = ["#800000", "#f58231", "#4363d8", "#3cb44b"]
        chosenHeaders = self.data.get_headers()
        xyColumns = chosenHeaders[0:2]
        animatedColumns = chosenHeaders[3:]

        numClusters = 4

        clusterDataObj = analysis.kmeans( self.data, animatedColumns[0], numClusters, True)
        self.canvas.itemconfig(self.columnName, text="Column: %s" % (animatedColumns[self.index]))

        self.headers = clusterDataObj.get_original_headers()

        normalizedMatrix = analysis.normalize_columns_separately(xyColumns, self.data)
        zeros = np.zeros((normalizedMatrix.shape[0],1))
        ones = np.ones((normalizedMatrix.shape[0],1))
        self.spatialMatrix = np.hstack((normalizedMatrix, zeros, ones))


        vtm = self.view.build()

        pts = (vtm *self.spatialMatrix.T).T

        nextTick = dt.datetime.now() + dt.timedelta(seconds=5)
        self.root.after(5, self.animatePoints, animatedColumns, numClusters, colors, pts, nextTick)

    def handleStop(self):
        self.stopButton = True

    def main(self):
        print('Entering main loop')
        self.root.mainloop()

if __name__ == "__main__":
    dapp = DisplayApp(700, 500)
    dapp.main()
