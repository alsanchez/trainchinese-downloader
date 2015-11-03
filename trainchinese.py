#!/usr/bin/env python3

import re
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
        print(result)
        name = result[2]
        name = re.sub(spanRegex, "", name)
        name = html.parser.HTMLParser().unescape(name)
        audio = "http://www.trainchinese.com/v1/" +result[6][3:]
        results.append([name, audio])

    return results 

if __name__ == "__main__":
    for (name, audio) in getresults("六"):
        print("{}\t{}".format(name, audio))

