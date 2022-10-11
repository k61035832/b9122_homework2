from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
covid_related = []

maxNumUrl = 500; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl and len(covid_related) < 10:
    try:
        curr_url = urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue

    soup = BeautifulSoup(webpage)
    web_str = str(soup).lower()

    if 'covid' in web_str:
        covid_related.append(curr_url)

    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        dot_position = seed_url.rfind('.')

        if seed_url[0:dot_position] in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)
        # else:
        #     print("######", childUrl)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))

print("List of URLs that contains covid:")
for url in covid_related:
    print(url)
