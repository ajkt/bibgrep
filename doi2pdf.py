import requests
import time
import random
import os



def doi2pdf(doi):
	print("... for",doi)
	
	prefix = "https://dl.acm.org/doi/pdf/"
	suffix = "?download=true"

	url = prefix + doi + suffix
	print("... trying URL:", url)

	r = requests.get(url, stream=True)
	with open("pdfs/%s.pdf" % doi.replace("/","--"), 'wb') as f:
		f.write(r.content)
	return

def scrapeFromDOIs(doilist):

	print(doilist)
	
	try: 
		os.stat("pdfs")
	except:
		os.mkdir("pdfs")

	count = 1
	for doi in doilist:
		
		# file already exists
		if (os.path.isfile("pdfs/" + doi.replace("/", "--") + ".pdf")):
			continue	

		# file doesn't exist yet
		print("... downloading", doi)
		doi2pdf(doi)
		count += 1
		
		delay = random.randrange(15,60)
		print("... that was" + count + "/" + len(doilist) + ". now waiting", delay, "seconds")	
		time.sleep(delay)

	count -= 1
	if (count == 0):
		print("... all bib files already downloaded")
	else:
		print("...done downloading", count, "pdfs")	

	return


