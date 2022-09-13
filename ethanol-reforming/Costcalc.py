# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 17:00:22 2022

@author: erikg
"""
import numpy as np
import pandas as pd

def importdata():
    all_data = pd.read_csv('C:/Users/erikg/Documents/GitHub/ml-catalysis-1/ethanol-reforming/ElementPrices.csv')
    add_data = pd.read_csv('ElementProps.csv')
    prices = all_data[['Z', 'USD/kg', 'USD/L']]
    props = add_data[['Number', 'Symbol', 'Name', 'Mass']]
    return prices, props

def mergedata(prices, props):
    price_dict = prices.to_dict()
    props_dict = props.to_dict()
    Data = {'Z': [], 'Symbol': [], 'Name': [], 'Mass': [], 'USD/kg': [], 'USD/L': []}
    numbers= set(price_dict['Z']) & set(props_dict['Number'])
    for n in numbers:
        if n>0:
            Data['Z'].append(n)
            Data['Symbol'].append(str(props[props['Number']==n]['Symbol'].values[0]))
            Data['Mass'].append(props[props['Number']==n]['Mass'].values[0])
            Data['Name'].append(str(props[props['Number']==n]['Name'].values[0]))
            Data['USD/kg'].append(prices[prices['Z']==n]['USD/kg'].values[0])
            Data['USD/L'].append(prices[prices['Z']==n]['USD/L'].values[0])
    return pd.DataFrame(Data)

def Names2Elements(Names, atominfo, n_layers=3):
    """
    Note: Only works for tri-layers
    Parameters
    ----------
    Names : TYPE
        DESCRIPTION.
    atominfo : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    Elements = np.zeros((len(Names),n_layers))
    for i, name in enumerate(Names[:,0]):
        "remove facet"
        find_Element = lambda sym : Find_Element(sym, atominfo)
        name=name[:-5]
        if name.find('-') == -1:
            element=find_Element(name)
            if element.size>0:#pure element
                for j in range(n_layers):
                    Elements[i,j]= element
            if len(name)==6:
                el1 = find_Element(name[:2])
                n1 = name[2]
                el2 = find_Element(name[3:5])
                n2 = name[5]
                print(n2)
                if (el1.size > 0) & (el2.size > 0) & n1.isdigit()& n2.isdigit():
                    n1 = int(n1)
                    n2 = int(n2)
                    if n1+n2==n_layers:
                        for j in range(n1):
                            Elements[i,j]=el1
                        for j in range(n2):
                            Elements[i,n1+j]=el2
        else:#n-layer in at-at-at notation
            names = name.split('-')
            for j, name in enumerate(names):
                element=find_Element(name)
                if element.size > 0:
                    Elements[i, j]= element
    return Elements
            
def Find_Element(Symbol, atominfo):
    mask = atominfo[:,1]==Symbol
    return atominfo[mask,0]
    
    
    
def expand_database(database, prices):
    Names = database[['Surface']].values
    ElementsContained = Names2Elements(Names, np.array(prices[['Z', 'Symbol']].values))
    return ElementsContained
    
def Work():
    prices, props = importdata()
    add_data = mergedata(prices, props)
    database = pd.read_csv('database-dft.csv')
    E = expand_database(database, add_data)
    return E
E = Work()
    
