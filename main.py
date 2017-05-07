import urllib
import re
from bs4 import BeautifulSoup
import sys

# collect all URLs/Links that we find into a list
# We need one URL to start with (taken from arguement given in Terminal/Command Line)
links = [sys.argv[1]]

# collect the email addresses we find into this list
emails = []

# count how many links we try in variable i
i = 0

# keep searching forever (until we command it to stop)
while True:
	while True:
		try:
			page = urllib.urlopen(links[i]).read()
			break
		except IOError:
			i = i + 1
		except UnicodeError:
			i = i + 1


	soup = BeautifulSoup (page, 'lxml')


	new_emails = []


	# find all emails on page

	new_emails.extend(	re.findall('([0-9a-zA-Z]+@[0-9a-zA-Z\.]+\.com?)', soup.prettify()))
	new_emails.extend(	re.findall('([0-9a-zA-Z]+@[0-9a-zA-Z\.]+\.net?)', soup.prettify()))
	new_emails.extend(	re.findall('([0-9a-zA-Z]+@[0-9a-zA-Z\.]+\.edu?)', soup.prettify()))
	new_emails.extend(	re.findall('([0-9a-zA-Z]+@[0-9a-zA-Z\.]+\.org?)', soup.prettify()))

	# remove duplicates by coercing to set, then back to list
	new_emails = list(set(new_emails))

	# write all emails into document 'emails' and to list also called emails
	file = open('emails', 'a')
	for email in new_emails:
		if email not in emails:
			file.write(email +'\t\t\t' + links[i] + '\n')
			emails.append(email)
			print email
	file.close()


	# collect all URLs/links so that we can scrape them in future loops
	for tag in soup.find_all('a', href = True):
		if tag['href'].startswith('http://') or tag['href'].startswith('web'):
			links.append(tag['href'])

	# OPTIONAL: remove the bottomr half of URLs/Links in links list after every ten pages scraped (or attempted to scrape)
	#if i % 10 == 0:
		#links = links[:-int((1/2)*len(links))]

	


	i = i + 1





