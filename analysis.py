# CS 251
# Spring 2019
# Eli Decker
# Project 4

import csv
import sys
import data
import numpy as np
import random
import scipy.stats
import scipy.cluster.vq as vq

"""All analysis functions will take lists of strings (column headers) 
to specify what (numeric) data to analyze. """

def data_range(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and returns a list of 
    2-element lists with the minimum and maximum values for each column. 
    The function is required to work only on numeric data types."""
    colRange = []
    temp = dataObj.get_specific_col_data(colHeaders)
    colRange.append(np.min(temp, axis=0))
    colRange.append(np.max(temp, axis=0))
    return colRange

def mean(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and returns a list of the 
    mean values for each column. Use the built-in numpy functions to execute this calculation."""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.mean(temp, axis=0)

def stdev(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and returns a list 
    of the standard deviation for each specified column. 
    Use the built-in numpy functions to execute this calculation."""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.std(temp, axis=0)

def normalize_columns_separately(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and returns a matrix with each 
    column normalized so its minimum value is mapped to zero and its maximum value is mapped to 1."""
    temp = dataObj.get_specific_col_data(colHeaders)
    return (temp - np.min(temp, axis=0)) / (np.max(temp, axis=0) - np.min(temp, axis=0))

def normalize_columns_together(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns a matrix with each entry normalized so that 
    the minimum value (of all the data in this set of columns) is 
    mapped to zero and its maximum value is mapped to 1."""
    temp = dataObj.get_specific_col_data(colHeaders)
    return (temp - np.min(temp)) / (np.max(temp) - np.min(temp))

# ------EXTENSION METHODS BELOW------

def sum_cols(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns the sum of each column"""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.sum(temp, axis=0)

def sum_rows(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns the sum of each row"""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.sum(temp, axis=1)

def sum_matrix(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns the sum of the whole matrix"""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.sum(temp)

def range_diff(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and returns a list of 
    difference between the max and min values for each column."""
    colRange = []
    temp = dataObj.get_specific_col_data(colHeaders)
    colRange.append(np.max(temp, axis=0)-np.min(temp, axis=0))
    return colRange

def transpose(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns the matrix transposed"""
    temp = dataObj.get_specific_col_data(colHeaders)
    return temp.getT()

def sort(colHeaders, dataObj):
    """Takes in a list of column headers and the Data object and 
    returns each column sorted from min at the top to max on the bottom"""
    temp = dataObj.get_specific_col_data(colHeaders)
    return np.sort(temp, axis=0)

# ------ Project 5 below -------------

def single_linear_regression(data_obj, ind_var, dep_var):
    # First, get the requested columns of data from your Data object. 
    # It is easiest to get both columns of data at once, with your dependent variable in the first column 
    # and your independent variable in the second.
    twoCols = data_obj.get_specific_col_data([ind_var,dep_var])

    # Second, use the scipy.stats.linregress (import scipy.stats) function to calculate 
    # the linear regression of the independent and dependent variables. 
    # The linear regression must occur in original data space, not the normalized data space. 
    # Store all of the outputs of the linregress function. You may want to have a separate variable 
    # for each of the returned outputs: slope, y-intercept, r-value, p-value, and standard error. 
    # See the linregress Documentation
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(twoCols)

    # Return a tuple containing all of the outputs of of linregress plus the min and max of both 
    # the dependent and independent variables.
    return slope, intercept, r_value, p_value, std_err, np.min(twoCols, axis=0), np.max(twoCols, axis=0)

def linear_regression(data_obj, ind_var, dep_var):
    # assign to y the column of data for the dependent variable
    y = data_obj.get_specific_col_data([dep_var])
    # assign to A the columns of data for the independent variables
    A = data_obj.get_specific_col_data(ind_var)
    # add a column of 1's to A to represent the constant term in the 
    #    regression equation.  Remember, this is just y = mx + b (even 
    #    if m and x are vectors).
    ones = np.ones((A.shape[0],1))
    A = np.hstack((A, ones))

    # assign to AAinv the result of calling numpy.linalg.inv( np.dot(A.T, A))
    #    The matrix A.T * A is the covariancde matrix of the independent
    #    data, and we will use it for computing the standard error of the 
    #    linear regression fit below.
    AAinv = np.linalg.inv( np.dot(A.T, A))

    # assign to x the result of calling numpy.linalg.lstsq( A, y )
    #    This solves the equation y = Ab, where A is a matrix of the 
    #    independent data, b is the set of unknowns as a column vector, 
    #    and y is the dependent column of data.  The return value x 
    #    contains the solution for b.
    x = np.linalg.lstsq( A, y , rcond=-1)

    # assign to b the first element of x.
    #    This is the solution that provides the best fit regression
    b = x[0]
    # assign to N the number of data points (rows in y)
    N = y.shape[0]
    # assign to C the number of coefficients (rows in b)
    C = b.shape[0]
    # assign to df_e the value N-C, 
    #    This is the number of degrees of freedom of the error
    df_e = N-C
    # assign to df_r the value C-1
    #    This is the number of degrees of freedom of the model fit
    #    It means if you have C-1 of the values of b you can find the last one.
    df_r = C-1

    # assign to error, the error of the model prediction.  Do this by 
    #    taking the difference between the value to be predicted and
    #    the prediction. These are the vertical differences between the
    #    regression line and the data.
    #    y - numpy.dot(A, b)
    error = y - np.dot(A, b)

    # assign to sse, the sum squared error, which is the sum of the
    #    squares of the errors computed in the prior step, divided by the
    #    number of degrees of freedom of the error.  The result is a 1x1 matrix.
    #    numpy.dot(error.T, error) / df_e
    sse = np.dot(error.T, error) / df_e

    # assign to stderr, the standard error, which is the square root
    #    of the diagonals of the sum-squared error multiplied by the
    #    inverse covariance matrix of the data. This will be a Cx1 vector.
    #    numpy.sqrt( numpy.diagonal( sse[0, 0] * AAinv ) )
    stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv ) )

    # assign to t, the t-statistic for each independent variable by dividing 
    #    each coefficient of the fit by the standard error.
    #    t = b.T / stderr
    t = b.T / stderr

    # assign to p, the probability of the coefficient indicating a
    #    random relationship (slope = 0). To do this we use the 
    #    cumulative distribution function of the student-t distribution.  
    #    Multiply by 2 to get the 2-sided tail.
    #    2*(1 - scipy.stats.t.cdf(abs(t), df_e))
    p = 2*(1 - scipy.stats.t.cdf(abs(t), df_e))

    # assign to r2, the r^2 coefficient indicating the quality of the fit.
    #    1 - error.var() / y.var()
    r2 = 1 - error.var() / y.var()

    # Return the values of the fit (b), the sum-squared error, the
    #     R^2 fit quality, the t-statistic, and the probability of a
    #     random relationship.
    return b, sse, r2, t, p

def pca(d, headers, normalize=True):
    """The function should take in a list of column headers and return a PCAData object 
    with the projected data, eigenvectors, eigenvalues, source data means, and source column headers stored in it."""

    # assign to A the desired data. Use either normalize_columns_separately 
    #   or get_data, depending on the value of the normalize argument.
    if normalize:
        A = normalize_columns_separately(headers, d)
    else:
        A = d.get_specific_col_data(headers)
  
    # assign to m the mean values of the columns of A
    m = np.mean(A,axis=0)

    # assign to D the difference matrix A - m
    D = A - m

    # assign to U, S, V the result of running np.svd on D, with full_matrices=False
    U,S,V = np.linalg.svd(D, full_matrices=False)

    # the eigenvalues of cov(A) are the squares of the singular values (S matrix)
    #   divided by the degrees of freedom (N-1). The values are sorted.
    evals = S**2/(D.shape[0]-1)

    # project the data onto the eigenvectors. Treat V as a transformation 
    #   matrix and right-multiply it by D transpose. The eigenvectors of A 
    #   are the rows of V. The eigenvectors match the order of the eigenvalues.
    pdata = V * D.T
    evecs = V

    # create and return a PCA data object with the headers, projected data, 
    # eigenvectors, eigenvalues, and mean vector.
    pcad = data.PCAData( pdata.T, evecs, evals, m, headers )
    return pcad

def kmeans_numpy( d, headers, K, whiten = True):
    '''Takes in a Data object, a set of headers, and the number of clusters to create
    Computes and returns the codebook, codes, and representation error.
    '''
    
    # assign to A the result of getting the data from your Data object
    A = d.get_specific_col_data(headers)
    # assign to W the result of calling vq.whiten on A
    W = vq.whiten(A)

    # assign to codebook, bookerror the result of calling vq.kmeans with W and K
    codebook, bookerror = vq.kmeans(W, K)
    # assign to codes, error the result of calling vq.vq with W and the codebook
    codes, error = vq.vq(W, codebook)

    # return codebook, codes, and error
    return codebook, codes, error

def kmeans( d, headers, K, whiten = True):
    '''Takes in a Data object, a set of headers, and the number of clusters to create
    Computes and returns the codebook, codes and representation errors. 
    '''
    # assign to A the result getting the data given the headers
    if type(headers) == str:
        headers = [headers]
    A=d.get_specific_col_data(headers)

    # if whiten is True
      # assign to W the result of calling vq.whiten on the data
    if whiten == True:
        W = vq.whiten(A)
    # else
      # assign to W the matrix A
    else:
        W = A

    # assign to codebook the result of calling kmeans_init with W and K
    codebook = kmeans_init(W, K)

    # assign to codebook, codes, errors, the result of calling kmeans_algorithm with W and codebook        
    codebook, codes, errors = kmeans_algorithm(W, codebook)
    clusterData = data.ClusterData( d, codebook, K, codes, errors, headers )
    # return the codebook, codes, and representation error
    return clusterData


    
def kmeans_init(A, K):
    """ Selects K random rows from the data matrix A and returns them as a matrix
    """
    # Hint: generate a list of indices then shuffle it and pick K
    # Hint: Probably want to check for error cases (e.g. # data points < K)
    randomList = list(range(0, A.shape[0]-1))
    np.random.shuffle(randomList)
    if A.shape[0] - 1 < K:
        K = 2
    kmeans = random.sample(randomList, K)
    kmeans = A[kmeans,:]

    return np.matrix(kmeans)


def kmeans_classify(A, codebook):
    '''# Given a data matrix A and a set of means in the codebook
    # Returns a matrix of the id of the closest mean to each point
    # Returns a matrix of the sum-squared distance between the closest mean and each point
    '''
    # loop over each row - k of code book. Code book is k rows and D columns
    # use np.square
    # for loop over k


    # Hint: you can compute the difference between all of the means and data point i using: codebook - A[i,:]
    # Hint: look at the numpy functions square and sqrt
    # Hint: look at the numpy functions argmin and min
    ids1 = []
    distances1 = []
    for i in range(A.shape[0]):
        diff = codebook - A[i,:]
        ide = np.sqrt(np.sum(np.square(diff), axis=1))
        distances1.append([np.min(ide)])
        ids1.append([np.argmin(ide)])

        ids = np.matrix(ids1)
        distances = np.matrix(distances1)
    return ids, distances

# Given a data matrix A and a set of K initial means, compute the optimal
# cluster means for the data and an ID and an error for each data point
def kmeans_algorithm(A, means):
    # set up some useful constants
    MIN_CHANGE = 1e-7     # might want to make this an optional argument
    MAX_ITERATIONS = 100  # might want to make this an optional argument
    D = means.shape[1]    # number of dimensions
    K = means.shape[0]    # number of clusters
    N = A.shape[0]        # number of data points

    # iterate no more than MAX_ITERATIONS
    for i in range(MAX_ITERATIONS):

        # calculate the codes by calling kemans_classify
        codes, distances = kmeans_classify(A, means)
        # codes[j,0] is the id of the closest mean to point j

        # initialize newmeans to a zero matrix identical in size to means
        newmeans = np.zeros_like(means)
        # Hint: look up the numpy function zeros_like
        # Meaning: the new means given the cluster ids for each point

        # initialize a K x 1 matrix counts to zeros
        counts = np.zeros((K, 1))
        # Hint: use the numpy zeros function
        # Meaning: counts will store how many points get assigned to each mean

        # for the number of data points
        for j in range(N):
            # add to the closest mean (row codes[j,0] of newmeans) the jth row of A
            # codes[j,0]
            newmeans[codes[j,0],:] = newmeans[codes[j,0],:] + A[j,:]
            # add one to the corresponding count for the closest mean
            counts[codes[j,0],0] += 1

        # finish calculating the means, taking into account possible zero counts
        #for the number of clusters K
        for j in range(K):
            # if counts is not zero, divide the mean by its count
            if counts[j,0] != 0:
                newmeans[j,:] = newmeans[j,:]/counts[j,0]
            # else pick a random data point to be the new cluster mean
            else:
                newmeans[j,:] = A[random.randint(0,A.shape[0]), :]
                

        # test if the change is small enough and exit if it is
        diff = np.sum(np.square(means - newmeans))
        means = newmeans
        if diff < MIN_CHANGE:
            break

    # call kmeans_classify one more time with the final means
    codes, errors = kmeans_classify( A, means )

    # return the means, codes, and errors
    return (means, codes, errors)

def kmeans_quality( errors, K):
    # Compute the sum squared error
    # print(errors**2)
    sse = np.sum(np.square(errors))
    # numpy log2 function to calculate the statistic with the following equation.
    N = errors.shape[0]
    MDL = sse + (K/2)*np.log2(N)
    return MDL


def main(argv):
    if len(argv) < 2:
        printf("Usage: python %s <data file>")
        exit(-1)

    # read some data
    data_obj = data.Data( argv[1] )
    ind_header = argv[2]
    ind_header2 = argv[3]
    dep_header = argv[4]

    # call the analysis function
    results = linear_regression( data_obj, [ind_header, ind_header2], dep_header)

    # m0 = 0.984, m1 = 2.088, b = -0.035, sse = 0.002,
    # R2 = 0.996, t = [8.6, 18.9, -0.88], p = [5.6e-5, 2.9e-7, 0.405]
    # print out the results
    # print("Model:    y = %.4fx + %.4f" % (results[0], results[1]) )
    print("m0: %.3f   " % (results[0][0]), "m1: %.3f   " % (results[0][1]), 
            "b: %.3f   " % (results[0][2]), "sse: %.3f   " % (results[1]) )
    print("R2: %.3f   " % (results[2]), "t: [%.3f, %.3f, %.3f] " % ((results[3][0,0]), (results[3][0,1]), (results[3][0,2])), 
            "p: [%.3g, %.3g, %.3g] " % ((results[4][0,0]), (results[4][0,1]), (results[4][0,2])) )

    return


if __name__ == "__main__":
    main(sys.argv)

