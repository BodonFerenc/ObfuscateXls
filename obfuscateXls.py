'''Obfuscates and converts family tree xls file.

Legacy family tree project available at http://freshmeat.sourceforge.net/projects/familytree_cgi/ 
accepts family tree data in xls. It might be useful to pass over you family tree data for 
e.g. data science and machine learning tasks. For privacy reasons you would like to replace sensitive information
with some cryptic string.
'''

import numpy as np
import pandas as pd
import calendar
import hashlib

from functools import partial
import argparse

import random
import string

def __getYear(d) -> int:
    """Gets the year part from a dateframe cell"""
    if not type(d).__name__ in ['str', 'int']:
        return np.NaN
    return d if type(d).__name__ == 'int' else int(d.split('/')[-1])

def __getMonth(d) -> str:
    """Gets the month part (if exists) from a dateframe cell"""
    if not type(d).__name__ == 'str':
        return np.NaN    
    a= d.split('/')
    return calendar.month_name[int(a[-2])]

def __getDay(d) -> int:
    """Gets the day part (if exists) from a dateframe cell"""
    if not type(d).__name__ == 'str':
        return np.NaN    
    a= d.split('/')
    return np.NaN if (len(a) < 2) or a[0] == '' else int(a[0])

def __obfuscateString(s: str, nonce: str):
    """Obfuscates a string by generating its hashcode.

    Hashcode generation is a deterministic process. 
    To avoid being able to decode an obfuscated string arbitraty random string, called nonce,
    can be added.

    See also: https://en.wikipedia.org/wiki/Cryptographic_nonce    
    """
    return str(hashlib.sha1(str.encode(s + nonce)).hexdigest())

def obfuscate(df, nonce=""):
    """Returns an obfuscated family tree stored in a pandas dataframe"""
    t = df.copy()
    t['gender']= np.where(t['gender'] == 1, 'female', 'male')
    t['status']= np.where(np.isnan(t['is living?']), '', np.where(t['is living?'] == 1, 'Living', 'Deceased'))

    t['year of birth']= t.apply(lambda row: __getYear(row['date of birth']), axis=1)
    t['month of birth']= t.apply(lambda row: __getMonth(row['date of birth']), axis=1)
    t['month of birth']= t['month of birth'].astype('category')
    t['day of birth']= t.apply(lambda row: __getDay(row['date of birth']), axis=1)

    t['year of death']= t.apply(lambda row: __getYear(row['date of death']), axis=1)
    t['month of death']= t.apply(lambda row: __getMonth(row['date of death']), axis=1)
    t['month of death']= t['month of death'].astype('category')
    t['day of death']= t.apply(lambda row: __getDay(row['date of death']), axis=1)

    t= t.drop(columns=['prefix', 'suffix', 'gender', 'date of birth', 'date of death', 
                   'is living?', 'schools', 'work places', 'places of living', 'general'])

    obfFn = partial(__obfuscateString, nonce=nonce)

    t['ID']=list(map(obfFn, t.index.values))
    t.set_index('ID', inplace=True)

    ## null handling requires a differrent approach
    t['father\'s ID']= t.loc[t['father\'s ID'].notna(), 'father\'s ID'].apply(obfFn)
    t['mother\'s ID']= t.loc[t['mother\'s ID'].notna(), 'mother\'s ID'].apply(obfFn)

    t['last name']=list(map(obfFn, t['last name'].values))
    t['webpage']= t.loc[t['webpage'].notna(), 'webpage'].apply(obfFn)
    t['email']= t.loc[t['email'].notna(), 'email'].apply(obfFn)                   

    return t

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="input family tree file in xls format")
    parser.add_argument("output_file", help="output file either xls or csv")
    parser.add_argument("--nonce", help="nonce used obfuscate (encrypt) strings like surnames")
    args = parser.parse_args()

    nonce = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(6)) if args.nonce == None else args.nonce
    df= pd.read_excel(args.input_file, index_col=0)
    t = obfuscate(df, nonce)

    extension = args.output_file[-4:]
    if extension == ".csv":
        t.to_csv(args.output_file)
    elif extension == ".xls":
        t.to_excel(args.output_file)
    else:
        raise NotImplementedError("Unknown output extension " + extension)

if __name__ == "__main__":
    main()