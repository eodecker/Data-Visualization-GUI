# CS 251
# Spring 2019
# Eli Decker
# Project 4

import csv
import numpy as np



class Data:
    """ create a class to handle Data"""

    def __init__(self, filename = None):

        # create and initialize fields for the class
        self.headers = []
        self.numHeadList = []
        self.header2col ={}
        self.typesCHECK = []

        self.types = []
        self.num_dimensions = 0
        self.num_points = 0
        self.row = 0
        self.value = 0
        self.finalData = []

        # if filename is not None
            # call self.read(filename)
        if (filename != None):
            self.read(filename)

    
    def read(self, filename):
        """ method for reading in the data from a file """
        lines = []
        rawData = []
        file = open(filename, "rU")
        csv_reader = csv.reader( file )
        for line in csv_reader:
            lines.append(line)
            for item in range(len(line)):
                line[item] = line[item].replace(" ","")
        self.headers = lines[0]
        self.types = lines[1]
        rawData = lines[2:]
        for row in rawData:
            newRow = []
            for i in range(len(row)):
                if self.types[i] != 'numeric':
                    continue
                else:
                    newRow.append(float((row[i].strip())))
            self.finalData.append(newRow)
        self.data = np.matrix(self.finalData)

        for i in range(len(self.types)):
            if self.types[i] == 'numeric':
                self.numHeadList.append(self.headers[i])
        i = 0
        for header in self.numHeadList:
            self.header2col[header] = i
            i += 1

        return self.data

    def write(self, filename, headers=None):
        ''' enables you to write out a selected set of headers to a specified file.
        take in a filename and an optional list of the headers of 
        the columns to write to the file
        '''
        f= open(filename,"w+")

        if headers != None:
            data = self.get_specific_col_data(headers)
        else:
            data = self.get_specific_col_data(self.get_headers())
            f.write(self.get_headers())
            f.write(self.get_types())
        f.write(self.get_specific_col_data(data))
        f.close()



    def add_column(self, colData):
        ''' adds a column to the data set '''
        


            
    
    def get_headers(self): 
        """returns a list of all of the headers."""
        return self.numHeadList


    
    def get_types(self): 
        """returns a list of all of the types."""
        return self.types

    def get_num_dimensions(self): 
        """returns the number of columns.   """
        dimensions = self.data.shape
        return dimensions[1]

    def get_num_points(self): 
        """returns the number of points/rows in the data set."""
        dimensions = self.data.shape
        return dimensions[0]

    def get_row( self, rowIndex ): 
        """returns the specified row as a NumPy matrix."""
        return self.data[rowIndex,:]

    def get_value( self, header, rowIndex ):
        """returns the specified value in the given column."""
        return self.data[rowIndex, self.header2col[header]]

    
    def get_specific_col_data( self, columns):
        """Takes in a list of columns headers and returns a Numpy matrix 
        with the data for all rows but just the specified columns."""
        headers = []
        for i in range(len(columns)):
            headers.append(self.header2col[columns[i]])
        return self.data[:,headers]

    def __str__ (self):
        num_cols = self.get_num_dimensions()
        num_rows = self.get_num_points()
        values = []
        string = ''
        for head in self.get_headers():
            values.append(self.header2col[head])
            string += '\t' + head
        for i in range(0,num_rows):
            string += '\n'
            for j in range(0, num_cols):
                string += '\t' + str(self.data[i, j])
        return string

class PCAData(Data):

    def __init__(self, dataObj, eVectors, eValues, dataMeans, dataHeaders):
        self.data = dataObj
        self.eigenVectors = eVectors
        self.eigenValues = eValues
        self.meanDataValues = dataMeans
        self.originalHeaders = dataHeaders

        self.numHeadList = []
        self.types = []
        counter = 0
        for i in range(0,len(self.originalHeaders)):
            self.numHeadList.append("PCA%d" % (counter))
            self.types.append("numeric")
            counter+=1

        self.header2col = {}
        i = 0
        for header in self.numHeadList:
            self.header2col[header] = i
            i += 1

    def get_eigenvalues(self):
        """returns a copy of the eigenvalues as a single-row numpy matrix."""
        return self.eigenValues

    def get_eigenvectors(self):
        """returns a copy of the eigenvectors as a numpy matrix with the eigenvectors as rows."""
        return self.eigenVectors

    def get_original_means(self):
        """ returns the means for each column in the original data as a single row numpy matrix."""
        return self.meanDataValues

    def get_original_headers(self):
        """ returns a copy of the list of the headers from the original data used to generate the projected data."""
        return self.originalHeaders

class ClusterData(Data):

    def __init__(self, dataObj, codebook, K, codes, errors, dataHeaders):
        self.codebook = codebook
        self.data = dataObj.get_specific_col_data(dataHeaders)
        self.K = K
        self.codes = codes
        self.errors = errors
        self.originalHeaders = dataHeaders

        self.numHeadList = []
        self.types = []
        counter = 0
        for i in range(len(self.originalHeaders)):
            self.numHeadList.append(self.originalHeaders[i])
            self.types.append("numeric")
            counter+=1

        self.header2col = {}
        i = 0
        for header in self.numHeadList:
            self.header2col[header] = i
            i += 1

    def get_K(self):
        return self.K

    def get_codes(self):
        return self.codes

    def get_data(self):
        return self.data

    def get_codebook(self):
        """ returns the means for each column in the original data as a single row numpy matrix."""
        return self.codebook

    def get_errors(self):
        """ returns errors"""
        return self.errors

    def get_original_headers(self):
        """ returns a copy of the list of the headers from the original data used to generate the projected data."""
        return self.originalHeaders


