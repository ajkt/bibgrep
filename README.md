> python ./bibgrep.py

Requires: *.bib files 


Features 
- creates a merged *.csv file from the *.bib files
- console output of temporal overview (time range of selected bib entries, number of entries per year)
- console output of conference overview (works for ACM DL where "series" takes the form of "<CONFERENCE> <YEAR> <OPTIONAL ADDITION>", e.g., "CHI ´19" or "CHI 2019" or "CHI `19 EA") and most common conferences in selected bib entries regardless of year
- creates a pdf directory and scrapes PDFs from the ACM DL based on the selected bib entries' DOIs, with randomized delays for polite scraping (may only work until end of June while the DL is open, or within eduroam) 


