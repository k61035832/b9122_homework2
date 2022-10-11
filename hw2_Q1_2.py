from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"
seed_url_prefix = 'https://www.sec.gov/news/press-release/'

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
charges_related = []

maxNumUrl = 500; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl and len(charges_related) < 20:
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

    # don't add the seed url
    if curr_url != seed_url and 'charges' in web_str:
        charges_related.append((curr_url, soup))

    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url_prefix in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)
        # else:
        #     print("######", childUrl)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))

print("List of URLs that contains charges:")
for url,soup in charges_related:
    print(url, soup.text)
