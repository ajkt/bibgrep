Some tools that help to partially automate literature reviews based on the ACM digital library.

> python ./bibgrep.py

Requires: *.bib files 


Features 
- creates a merged *.csv file from the *.bib files
- console output of temporal overview (time range of selected bib entries, number of entries per year)
- console output of conference overview (works for ACM DL where "series" takes the form of "<CONFERENCE> <YEAR> <OPTIONAL ADDITION>", e.g., "CHI ´19" or "CHI 2019" or "CHI `19 EA") and most common conferences in selected bib entries regardless of year
- calls on doi2pdf.py and textanalysis.py, see below

> doi2pdf.py

Features:
Creates a pdf directory and scrapes PDFs from the ACM DL based on the selected bib entries' DOIs, with randomized delays for polite scraping (may only work until end of June while the DL is open, or within eduroam).

> textanalysis.py

Features:
Raw text extraction from PDF, keeping content order despite two-column structure and separating ligatures. (Every now and then - i.e., 1 / 366 in my test) it can't deal with a PDF if it contains super fancy glyphs though ...).
Called as standalone: goes through all *.txt files in pdfs folder and creates a new *.csv containing all keyword occurrences (nltk concordances) for two keywords. 

> bibmerge-uniqueify.py

Features:
Merges all bib files in the local space and creates a merged CSV file of the bib entries. Then checks for duplicates using a first more conservative measure (by title regardless of capitalization and by year), as databases don't always populate the DOI / ID / URL columns in the same way) and creates a second merged CSV without these duplicates. Also creates another CSV to identify additional potential duplicates for manual checking based on a less conservative measure (here: title regardless of capitalization, but ignoring year).
