# import libraries
from functions1 import *
from pandas_ods_reader import read_ods
###########################################################
odsfile = rel('../variables02.ods')
sheetname = 'foam'
df = read_ods(odsfile, sheetname)


[df_bc, df_prop, df_ctl] = create_df(df)
###########################################################

# creating directories and files
casedir = rel('../foam/laplacianFoam')

createDirsAndFiles(casedir, df_bc, df_prop, df_ctl)
