"""
This script organizes a latex bibliography alphabetically and checks for duplicates.
It changes bib lables to firstAuthorLastName_year_firstTwoWordsOfTitle 

Requires: 
    Python 3
    pybtex 2.0.1
"""

from pybtex.database.input import bibtex
from pybtex.database import BibliographyData, Entry
import string

#bib_data.entries.keys()
#print bib_data.entries['ruckenstein-diffusion'].fields['title']
#Predicting the Diffusion Coefficient in Supercritical Fluids


def bibLoader(filePath):
    """
    This function loads the Bibliography and returns a list of bib tex entries
    """
    parser = bibtex.Parser()
    bib_data = parser.parse_file(filePath)
    return bib_data


def bib_fixLables(inBib):
    for x in range(1, 2):
        pass
    

def bibCleanUp(inBib, toLower=True, fixLables=True, checkDuplicates=True, alphabetize=True):
    """
    This file cleans up the bib as needed
    toLower: converts all field labels to lower case - RECOMMENDED
    fixLables: Turns all labels to firstAuthorLastName_year_firstTwoWordsOfTitle 
    """

    for key, entry in inBib.entries.items():
        print(''.join(''.join(inBib.entries[key].persons['author'][0].last_names).split()).translate({ ord(c): None for c in "\{/},:'-.\"" }) + #Gets the first author's last name
                                    str(inBib.entries[key].fields['year']).translate({ ord(c): None for c in "\{/},:'-.\"" }) + # Gets the year of the paper
                                    ''.join(string.capwords(inBib.entries[key].fields['title'].translate({ ord(c): None for c in "\{/},:'-.\"" }).strip().lower()).split()[:2] # Gets first two words of the paper
                                ), entry)

    if fixLables:
        fixed_entry_lables = ((''.join(''.join(inBib.entries[key].persons['author'][0].last_names).split()).translate({ ord(c): None for c in "\{/},:'-.\"()" }) + #Gets the first author's last name
                                    str(inBib.entries[key].fields['year']).translate({ ord(c): None for c in "\{/},:'-.\"()" }) + # Gets the year of the paper
                                    ''.join(string.capwords(inBib.entries[key].fields['title'].translate({ ord(c): None for c in "\{/},:'-.\"()" }).strip().lower()).split()[:2] # Gets first two words of the paper
                                ), entry) for key, entry in inBib.entries.items())
        inBib = BibliographyData(
            entries=fixed_entry_lables,
            preamble=inBib._preamble,
            wanted_entries=inBib.wanted_entries,
            min_crossrefs=inBib.min_crossrefs,
        )



    if toLower: 
        inBib = inBib.lower()

    if checkDuplicates:
        pass

    if alphabetize:
        sorted_keys = sorted(inBib.entries)
        sorted_bib_entries = ((key, inBib.entries[key]) for key in sorted_keys)
        inBib = BibliographyData(
            entries=sorted_bib_entries,
            preamble=inBib._preamble,
            wanted_entries=inBib.wanted_entries,
            min_crossrefs=inBib.min_crossrefs,
        )
    
    for key in inBib.entries.keys(): print(key)

    return inBib

def bibPrinter(inBib, outFile):
    """
    This function prints a bibtex file to the given input file
    """
    inBib.to_file(outFile, bib_format='bibtex')



if __name__ == "__main__":
    
    my_bib = bibLoader('endres_bib_living.bib')
    new_bib = bibCleanUp(my_bib, toLower=False, fixLables=True, alphabetize=True)
    bibPrinter(new_bib, 'endres_bib_living.bib')

