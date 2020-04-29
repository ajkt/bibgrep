import nltk
import PyPDF2
import subprocess
import unicodedata
import html2text
import os
import pandas as pd
import numpy



# For specific PDF file: extracts raw text (despite two-column structure and ligatures; the latter are separated)
# via three steps (by-product files are cleaned up at the end):
# 1) pdf converted to html with columns & ligatures kept intact via pdf2htmlEX
# !!! requires that pdf2htmlEX is available as a command line tool !!!
# 2) this is normalized to separate ligature glyphs
# 3) raw text extraction from normalized html
#
# Alternatives that didn't work quite right:
# - PyPDF2's pdffilereader: had issues with multiple columns
# - pdftotext -raw: dealt with two columns but still had ligature issues
# - commandline pdftohtml -i -c and html2text: ligature issues
#
def pdf2text(pdfFile):
	print(pdfFile)

	try:
		PyPDF2.PdfFileReader(open(pdfFile, "rb"))
	except PyPDF2.utils.PdfReadError:
		print("INVALID PDF - SOMETHING WENT WRONG WHEN DOWNLOADING THIS PDF!")
		return -1
	

	htmlFileName = pdfFile.replace(".pdf", ".html")
	
	# convert to HTML (keeping two columns & ligatures):
	return_value = subprocess.call("pdf2htmlEX --decompose-ligature 1  --tounicode 1 --optimize-text 1 --embed-external-font 0 --debug 1 " + pdfFile + " " + htmlFileName, shell=True)
	if return_value == 0:
		print("converted to html: "+htmlFileName)
	else: 
		print("SOMETHING WENT WRONG IN CONVERTING PDF TO HTML")
		return -1
	#if sth goes wrong, add: --debug 1

	
	# normalize to separate the ligature glyphs:
	htmlfile = open(htmlFileName, "r", encoding = "utf-8", errors = "ignore")
	thehtml = htmlfile.read()
	htmlfile.close()
	separatedLigatures = unicodedata.normalize("NFKD", thehtml)
	normalizedFileName = htmlFileName.replace(".html", "-normalized.html")
	normalizedHTML = open(normalizedFileName, "w")
	normalizedHTML.write(separatedLigatures)
	normalizedHTML.close()
	print("normalized: "+normalizedFileName)

	# extract raw text
	normalizedHTML = open(normalizedFileName, "r", encoding = "utf-8", errors = "ignore")
	html_with_text = normalizedHTML.read()

	h = html2text.HTML2Text()
	h.ignore_links = True
	h.ignore_images = True
	
	rawtext = h.handle(html_with_text)
	normalizedHTML.close()
	print(rawtext)
	textFile = pdfFile.replace(".pdf", ".txt")
	file = open(textFile, "w")
	file.write(rawtext)
	file.close()	
	print("extracted text: " + textFile)
	
	# clean up: remove htmlFileName and normalizedFileName
	os.remove(htmlFileName)
	os.remove(normalizedFileName)	

	return


def extractText():
	countConverted = 0
	countIgnored = 0
	countError = 0
	
	errorFiles = []
	
	print("... beginning text extraction")
	for file in os.listdir("pdfs/"):
		if file.endswith(".pdf"):
			convertedFileName = "pdfs/" + file.replace(".pdf",".txt")
			if os.path.exists(convertedFileName):
				print("ignoring " + file + " b/c text has already been extracted")
				countIgnored += 1
			else:
				#print("found pdf that hasn't been extracted yet: "+file)
				return_value = pdf2text("pdfs/" + file)

				if return_value == -1:
					countError += 1
					errorFiles.append(file)
				else:
					countConverted += 1
			
	print("raw text extracted from " + str(countConverted) + " PDFs.")
	print("Ignored: " + str(countIgnored))
	print("Errors: " + str(countError))
	print("Errors in files: ")
	print(errorFiles)
	return

def concordanceInFile(keyword, nltkText):	
	concordlist = nltkText.concordance_list(keyword, width=400)	
	print(concordlist)
	# print(type(concordlist))
	#for line in concordlist:
		#print("line")
		#print(line)
		#print("PRINTABLE")
		#print(line[-1])
		
	return concordlist


def nltktextify(textFileName):
	
	textFile = open(textFileName, "r")
	text = textFile.read()
	textFile.close()

	tokens = nltk.word_tokenize(text.lower())
	nltkText = nltk.Text(tokens)
	return nltkText

def commonContextsInFile(keyword, nltkText):

	nltkText.common_contexts(keyword)
	
	return

def grabConcords(concordlist):
	mergedConcords = []
	for line in concordlist:
		mergedConcords.append(line[-1])
	return mergedConcords
	

def perText(file):

	return

def summariseTxts(keywordList):

	# build an overview, for each text: #occurrences of each keyword, concordance of each occurrence, length of text overall, ....

	#for now: two keywords
	columnNames = ["txt", "tokens", "kw1", "kw1Occurrences", "kw1Concordances", "kw2", "kw2Occurrences", "kw2Concordances"]
	overviewDF = pd.DataFrame(columns=columnNames)

	count = 0

	files = os.listdir("pdfs")
	for f in files:
		if not f.endswith(".txt"):
			continue
		else:
			print("found txt:")
			print(f)
		
			testFile = "pdfs/" + f
			thistext = nltktextify(testFile)
			print(len(thistext.tokens))	
			
			concordlistone = concordanceInFile(keywordList[0], thistext)	
			concordlisttwo = concordanceInFile(keywordList[1], thistext)

			mergedConcords = grabConcords(concordlistone)	

			row = []
			row.append(testFile)
			row.append(len(thistext.tokens))
			row.append(keywordList[0])
			row.append(len(mergedConcords))
			row.append(mergedConcords)

			row.append(keywordList[1])
			mergedConcords = grabConcords(concordlisttwo)
			row.append(len(mergedConcords))	
			row.append(mergedConcords)
	
			print(row)
	
			rowDF = pd.DataFrame([row], columns = columnNames)
			print(rowDF)

			overviewDF = overviewDF.append(rowDF, ignore_index=True)

	print(overviewDF)
	overviewDF.to_csv("teeest.csv")

	return
	


# main for testing
if __name__ == "__main__":

	# nltk.download("punkt")

	keywordone = "testone"
	keywordtwo = "testtwo"

	# testFile = "test"
	# thistext = nltktextify(testFile)
	# print(len(thistext.tokens))	

	#commonContextsInFile([keywordone, keywordtwo], thistext)
	#thistext.similar(keywordone)
	#thistext.dispersion_plot([keywordone])	

	#frequentified = nltk.FreqDist(thistext)
	#print(frequentified.most_common(15))

	
	# Build an overview, for each text:
	summariseTxts([keywordone, keywordtwo])



