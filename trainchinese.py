#!/usr/bin/env python3

import re
import sys
import json
import html.parser
import urllib.parse
import http.client

def getresults(query):
    domain = "www.trainchinese.com"
    urlTemmplate = "/v1/a_user/searchForWords.php?searchWord={}"
    url = urlTemmplate.format(urllib.parse.quote(query))

    client = http.client.HTTPConnection(domain)
    client.request("GET", url)
    response = client.getresponse()
    responseText = response.read().decode();

    regex = re.compile(r'sr_oneWord\((.+?)\)\+')
    matches = re.findall(regex, responseText)

    spanRegex = re.compile(r'<\/?span[^>]*>')

    results = []
    for match in matches:
        match = match.replace("'", "\"")
        match = "[" + match + "]"
        result = json.loads(match)
        name = result[2]
        name = re.sub(spanRegex, "", name)
        name = html.parser.HTMLParser().unescape(name)
        audio = "/v1/" +result[6][3:]
        results.append([name, audio])

    return results 

def downloadfile(url, path):
    domain = "www.trainchinese.com"
    client = http.client.HTTPConnection(domain)
    client.request("GET", url)
    response = client.getresponse()

    with open(path, "wb") as outputfile:
        outputfile.write(response.read())

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: {} <word>".format(sys.argv[0]))
        sys.exit(1)

    word = sys.argv[1]

    for (name, audio) in getresults(word):
        if name == word:
            downloadfile(audio, name + ".mp3")
            print("Done")
            sys.exit(0)

    print("Not found")
    sys.exit(1)
