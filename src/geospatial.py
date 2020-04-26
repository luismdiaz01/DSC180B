import pandas as pd
from arcgis import *
import arcgis
from arcgis import GIS

def read_gis(item_id = '96c4fb36182f409a9b141f3bbaad6ab1', user = None, passw = None):
    gis = GIS(username=user, password=passw)
    flayer = gis.content.get(item_id)
    df = pd.DataFrame.spatial.from_layer(flayer.layers[0])
    return df

def pop_by_div(df, group = "PREC"):
    pop = df.groupby([group]) ['H7Z001','H7Z002','H7Z003','H7Z004','H7Z005','H7Z006','H7Z007','H7Z008','H7Z009','H7Z010'].sum().sort_index().reset_index()#.sort_values(ascending = False)
    pop['white_pop'] = pop['H7Z003']/ pop['H7Z001']
    pop['minority_pop'] = pop.drop([group,'H7Z001','H7Z002','H7Z003' ], axis = 1).sum(axis =1)/ pop['H7Z001']
    return pop