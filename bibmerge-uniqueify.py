import bibtexparser
import pandas as pd
import subprocess
from subprocess import check_output
import os
import re
import nltk 
import doi2pdf as d2p
import textanalysis as ta


def bib2csv(entries):
	df = pd.DataFrame(entries)
	df.to_csv("merged.csv", index=False)
	return

def temporalOverview(df):
	mostrecent = pd.to_numeric(df["year"]).max()
	earliest = pd.to_numeric(df["year"]).min()
	print("... spanning time range of", mostrecent-earliest,"years: from",earliest, "to",mostrecent)
		

	perYear = df["year"].value_counts()
	print("\nranked by number of entries:\n")
	print(perYear)
	
	print("\nranked by year:\n")
	print(perYear.sort_index())	

	return

def conferenceOverview(df):
	series = df["series"].value_counts()
	print("\nranked by conference:\n")
	print(series)

	return

# create new column of overarching conference (i.e., group all CHIs regardless of year) - works for ACM DL where series = <NAME> <YEAR AS 'XX> <OPTIONAL REST OF NAME> 
def confHat(df):
	df["confName"] = df["series"].apply(lambda row: splitName(row))
	#print(df["confName"])
	confNames = df["confName"].value_counts()
	print("\nranked by conference whole:\n")
	print(confNames)
	
	return

def splitName(name):
	if (pd.isna(name)):
		return "--"
	# split by: optional "´" char, then 2-4 digits:
	confNoYear =  re.split("’?\d{2,4}", name)
	confNoYear =  "".join(confNoYear)
	return confNoYear



if __name__== "__main__":

	# make sure a filepath argument has been added:
	#if (len(sys.argv) != 2):
	#	print("... need a filepath appended to this command, to indicate a folder containing *.bib files.")
	#	quit()

	# firstarg = sys.argv[1]
	
	path = subprocess.Popen("pwd", stdout=subprocess.PIPE) # returns output and return code
	path = path.communicate()[0]
	path = path.decode("utf-8")
	print("... searching for bibs in: \n\n", path, "\n")

	# gather bibfiles:
	countbibs = 0
	bibFiles = []
	with os.scandir() as i:
		for entry in i:
			if entry.is_file():
				fileEnding = entry.name.split(".")
				fileEnding = fileEnding[len(fileEnding)-1] 
				
				if (fileEnding == "bib"):
					countbibs += 1
					bibFiles.append(entry.name)
	print("... found ",countbibs, "bib files:")
	print(bibFiles, "\n")
	
	if (bibFiles == 0): 
		print("...quitting.")
		quit()

	# set parser to recognize common strings like "nov"
	parser = bibtexparser.bparser.BibTexParser(common_strings=True)

	# merge bibfiles
	print("counting the bibfiles")
	for bib in bibFiles:
		with open(bib, "r") as bpfile:
			bpdb = bibtexparser.load(bpfile, parser = parser)
			print(bib, ":", len(bpdb.entries))
	print("... with a total of ", len(bpdb.entries), "bib entries.")

	# save as merged csv:	
	#bib2csv(bpdb.entries)

	pandaDF = pd.DataFrame(bpdb.entries)	
	print(pandaDF.columns.values)

	# temporal overview
	temporalOverview(pandaDF)

	# conference overview - by conference series vs. grouped by conference regardless of year
	conferenceOverview(pandaDF)
	confHat(pandaDF)

	print(pandaDF[["confName","booktitle","doi"]])
	
	print("\n... creating merged CSV file")
	pandaDF.index += 1
	pandaDF.to_csv("merged.csv")

	pandaDF["titleLower"] = pandaDF.apply(lambda row: row.title.lower(), axis=1)
	print(pandaDF[["title","titleLower"]])
 	
	print("\n checking for DUPLICATES in currently most conservative measure: title regardless of capitalization AND year")
	searchBy = ["titleLower", "year"] # ["title", "year"]
	anyDuplicates = pandaDF.duplicated(searchBy).any()
	theDuplicates = pandaDF[pandaDF.duplicated(searchBy)]
	if anyDuplicates:
		print("found some:")
		print(theDuplicates[["year","title","author"]].to_string())
		
		print("\n... creating second CSV without duplicates.")
	else:
		print("found none.")

	pandaDFunique = pandaDF.drop_duplicates(subset = searchBy, keep = "first").reset_index(drop = True)
	pandaDFunique.index += 1
	pandaDFunique.to_csv("merged-no-duplicates-conservative.csv")
	

	searchByPotentials = ["titleLower"]
	anyDuplicates = pandaDFunique.duplicated(searchByPotentials).any()
	potentialDuplicates = pandaDFunique[pandaDFunique.duplicated(searchByPotentials, keep = False)] # keep = false: mark ALL occurrences, not just any after first
	if anyDuplicates:
		print("\n... also found some more potential duplicates for manual checking:")
		print(potentialDuplicates[["year", "title", "author"]])
		potentialDuplicates.to_csv("identifiedAsMorePotentialDuplicates.csv")



	
	

