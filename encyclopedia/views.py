from django.shortcuts import render
import markdown2

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def create(request):
    return render(request, "encyclopedia/createNewPage.html")

def createPage(request):
    if request.method == "POST":
        title = request.POST["title"]
        contents = request.POST["contents"]
        if title != "" and contents != "":
            util.save_entry(title, contents)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikiContents(request, wikiContents):
    return searchLogic(request, wikiContents)

def search(request):
    search = ""
    if request.method == "POST":
        search = request.POST["q"]
        limit = 0
        filenames = util.list_entries()

        matches = []
        # use for case-sensitive valuess
        matches = list(filter(lambda searching : search.lower() in searching.lower(), filenames))
        
        # if more than 1 matches, it will increase the limit
        # else if partial match, will return as list
        if len(matches) > 1:
            limit = 1
        else:
            matches = []
            for match in filenames:
                if search.upper() in match.upper():
                    if not search.upper().__eq__(match.upper()):
                        matches.append(match)

        # return more than 1 search values or as list           
        if len(matches) > limit :
            return render(request, "encyclopedia/searchResult.html", {
                "entries": matches
            })
    #return exact search value
    return searchLogic(request, search)

#function for displaying 1 search value and its contents
def searchLogic(request, search):
    markdowner = Markdown()

    wikiDisplay = util.get_entry(search)

    if wikiDisplay != None:
        wikiDisplay = markdowner.convert(wikiDisplay)

    return render(request, "encyclopedia/wikiDisplay.html", {
        "wikiDisplay": wikiDisplay
    })

