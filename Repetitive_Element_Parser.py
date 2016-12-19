import numpy as np
import pandas as pd
from ipywidgets import *
from IPython.display import display
from sqlalchemy import create_engine
import os
import argparse

#dependencies are imported above
#the following code specifies command-line interface

def valid_file(param):
    base, ext = os.path.splitext(param)
    if ext.lower() not in (['.xlsx']):
        raise argparse.ArgumentTypeError('File must have a .xlsx extension')
    return param
    
parser = argparse.ArgumentParser(prog="Repetitive Element Parser",
                                 description='input excel file and sheet number to parse and return rep-els from')
parser.add_argument("sheet", type=valid_file, help="input the filename \
                                                of an excel spreadsheet containing the expression data")
parser.add_argument("-sn", "--sheetnumber", default=0, action='store', type=int, help="input \
                                                                                    the sheetnumber of interest \
                                                                                    indexed at 0")
parser.add_argument("-ma", "--maplot", default=False, action='store_true', help="create an \
                                                                             ma_plot of the relevant elements")
parser.add_argument("--ERV", action='store_true', default=False)
parser.add_argument("--LTR", action='store_true', default=False)
parser.add_argument("--LINE", action='store_true', default=False)
parser.add_argument("--SINE", action='store_true', default=False)

results = parser.parse_args()

gene_list = pd.read_excel(results.sheet, sheetname=results.sheetnumber, header=0)

#defining the class of differential expression objects
class diff_expression_df:
  
    """This class defines the functionality associated with visualizing and parsing repetitive element expression
        data from a differential read counts program, such as DRDS. The RECO class represents a 'tidy' data container
        (i.e. one that has already been tidied up in various ways such that it fulfills the 'tidy data' requirements
        outlined by Wikham in the Journal of Statistical Software),
            in this case the data should be in a pandas dataframe, but series type object would also work."""
    
    def __init__(self, my_dataframe):
        
        #create an instance of the object
        self.my_dataframe = my_dataframe
        
        self.my_dataframe.fillna(0)
        
        #converting baseMean values to log10 for better visualization of the data
        self.my_dataframe["baseMean_log_10"] = \
        self.my_dataframe.apply(lambda row: np.log10(np.abs(row["baseMean"])+1), axis=1)
        
        #transfer dataframe to an sqlite database - this could be used for subsequent parsing to make it faster
        #and more memory efficient
        engine = create_engine('sqlite:///')
        self.my_dataframe_sql = self.my_dataframe.to_sql("new_database", con=engine, if_exists='replace')
        
        #families
        self.ERVL_fam = self.my_dataframe[my_dataframe["Family"]=='ERVL']

        #classes
        self.LINE_class = self.my_dataframe[self.my_dataframe["Type"]=='LINE']
        self.SINE_class = self.my_dataframe[self.my_dataframe["Type"]=='SINE']
        self.LTR_class = self.my_dataframe[self.my_dataframe["Type"]=='LTR']
        
    
    def __str__(self):
        
        return 
        """This class object represents a dataframe that will be parsed and sent to an SQLite database
        for further efficient parsing. The class object extends repetitive element parsing functionality to
        a standard differential expression output file that is converted into a pandas Dataframe object.
        
        The .__init__() method can be altered to parse the dataframe in any number of ways consistent with
        a pandas dataframe index.
        
        The '.ma_plot()' method returns a stereotypical MA-plot of the data, and is helpful for identifying
        repetitive elements of interest and comparing multiple MA-plots of different repetitive element
        classes and families. It takes zero or no arguments, arguments include 'all', 'LTR', 'ERVL', 'LINE',
        'SINE'."""
    
    
        
    def ma_plot(self, elements='all'): #how do I link up the elements argument to the user input from the widget?
        
    
        from bokeh.plotting import figure, output_file, output_notebook, show
        from bokeh.charts import Scatter
        from bokeh.layouts import row
        
        tooltips= [("Name", "@Name")]
        
        LTRs = Scatter(self.LTR_class, x="baseMean_log_10", y="log2FoldChange", title="LTR Expression",
                       xlabel="log 10 mean expression", ylabel="log 2 fold change", tooltips=tooltips, color='red')
            
        ERVLs = Scatter(self.ERVL_fam, x="baseMean_log_10", y="log2FoldChange", title="ERVL Expression",
                       xlabel="log 10 mean expression", ylabel="log 2 fold change", tooltips=tooltips, color='blue')

        LINEs = Scatter(self.LINE_class, x="baseMean_log_10", y="log2FoldChange", title="LINE Expression",
                       xlabel="log 10 mean expression", ylabel="log 2 fold change", tooltips=tooltips, color='purple')

        SINEs = Scatter(self.SINE_class, x="baseMean_log_10", y="log2FoldChange", title="SINE Expression",
                       xlabel="log 10 mean expression", ylabel="log 2 fold change", tooltips=tooltips, color='green')
        
        if elements==('all'): #need to figure out how to bump out of the conditionals below without having to rewite all of the code
            
            show(row(LTRs,ERVLs,LINEs,SINEs))
            output_notebook()
            
        elif elements==('LTR') or results.LTR==True:
            output_notebook()
            show(row(LTRs))
            
        elif elements==('ERVL') or results.ERV==True:
            output_notebook()
            show(row(ERVLs))
            
        elif elements==('LINE') or results.LINE==True:
            output_notebook()
            show(row(LINEs))
        elif elements==('SINE') or results.SINE==True:
            output_notebook()
            show(row(SINEs))
            
repetitive_elements = diff_expression_df(gene_list)

if results.maplot==True:
	return repetitive_elements.ma_plot()


#here I will make a class of repetitive elements that inherits functionality from the diff_exp_df class
#but that also contains its own functionality

class ERVL(diff_expression_df):
    

    def __init__(self, data):
        
        super(ERVL, self).__init__(data)
        
        self.ERVL_fam = data[data["Family"]=='ERVL']
        
        
    def __str__(self):
        """This class is an inherited class based up on the diff_expression_df class. It implements the same
        functionality and methods, but extends the parental functions by including an 'ervs_up' function."""
        
    
    def ERVL_up(self, log2FC=4):
        """Return a list of upregulated ERVS of log2FC > 4"""
        
        return self.ERVL_fam[self.ERVL_fam['log2FoldChange'] >= 3]
        