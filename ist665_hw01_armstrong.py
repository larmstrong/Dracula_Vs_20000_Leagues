# IST 664 - Natural Language Processing
# Assignment 01
# Leonard Armstrong


#--------------------------------------------------------------------------------------------------
# Library Imports
import config

import nltk
import pandas as pd 
import pathlib as pl
import tabulate


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
comparison_catalog = corpus_catalog.query(query_str).copy()

# Read the text for the subset of files of interest, storing the text and the length of the text
# back into the comparison corpus
comparison_catalog.loc[:, 'Text'] = ''
comparison_catalog.loc[:, 'Length'] = 0
for k,rec in comparison_catalog.iterrows() :
    with open(rec['FilePath'], "r") as f :
        txt = f.read()
        comparison_catalog.loc[k, 'Text'] = txt
        comparison_catalog.loc[k, "Length"] = len(txt)
        f.close()

#--------------------------------------------------------------------------------------------------
# Tokenize the comparison docs
comparison_catalog.loc[:, 'Tokens'] = None
for k, rec in comparison_catalog.iterrows():
    toks = nltk.word_tokenize(comparison_catalog.loc[k, 'Text'])
    # Normalize the tokens to lowercase.
    toks = [w.lower() for w in toks]
    # Save the token list
    comparison_catalog.at[k, 'Tokens'] = toks
    # Save the # of tokens in the list.
    comparison_catalog.at[k, 'NTokens'] = len(toks)

# Display the 'simple' data elements in the catalog.
cols = comparison_catalog.columns.tolist()
cols.remove('Text')
cols.remove('Tokens')
print(tabulate.tabulate(comparison_catalog.loc[:,cols], cols, tablefmt='fancy_grid'))
