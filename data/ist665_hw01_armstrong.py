
# IST 664 - Natural Language Processing
# Assignment 01
# Leonard Armstrong


#--------------------------------------------------------------------------------------------------
# Library Imports

import config

import nltk
import pandas as pd 
import pathlib as pl


#--------------------------------------------------------------------------------------------------
# Load Corpus Data
# Our corpus may (does) have more than the required two documents. So we use configurations to 

# Create a path to the data/corpus catalog file. This file is a CSV that contains title, author,
# genre, year of publication and location of the text for every document in the available corpus.
corpus_catalog_fpath = pl.Path(config.CORPUS_DPATH_REL, config.CORPUS_DIRECTORY_FNAME)

# Read the corpus catalog
corpus_catalog = pd.read_csv(corpus_catalog_fpath, index_col='Key')

# Create the full file paths to the selected documents
corpus_catalog['FilePath'] = [pl.Path(config.CORPUS_DPATH_REL, f) for f in corpus_catalog.FileName]

# Subset the corpus to just the items to be compared.
query_str = f'Key in ("{config.DOC1_KEY}", "{config.DOC2_KEY}")'
comparison_catalog = corpus_catalog.query(qstring)

# Read the text for the subset of files of interest, storing the text and the length of the text
# back into the comparison corpus
for k,rec in comparison_catalog.iterrows() :
    with open(rec['FilePath'], "r") as f :
        txt = f.read()
        comparison_catalog.at[k, 'Text'] = txt
        comparison_catalog.at[k, "Length"] = len(txt)
        f.close()


#--------------------------------------------------------------------------------------------------
# Tokenize the comparison docs

