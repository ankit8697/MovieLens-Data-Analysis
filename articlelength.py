# Adapted from code found at
# http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python

import urllib.parse
import urllib.request
import urllib.error


def articleLength(articles):
    
    
    
    for article in articles:
        # If a Wikipedia article has a character that gets in the way of being part
        # of a webpage URL, transform it appropriately
        quotedArticle = urllib.parse.quote(article)
        
        # If something fails when reading the Wikipedia page, the title is likely
        # bad.
        try:
            # This block of text opens up a web connection, convinces Wikipedia that
            # it is a real browser trying to grab the data (otherwise, Wikipedia
            # refuses to hand it over), and reads a strong of data containing the
            # web page
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
            resource = opener.open("http://en.wikipedia.org/wiki/" + quotedArticle)
            data = resource.read()
            resource.close()
            
            # Print the name of the article, and size in bytes. This includes all
            # kind of other cruft that Wikipedia articles have, but it's at least an
            # easy to way to count and compare.
            print(article+':', len(data))
            
        except urllib.error.HTTPError:
            print("Could not find title",article)



