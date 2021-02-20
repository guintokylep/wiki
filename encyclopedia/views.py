from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util
from markdown2 import Markdown

def index(request):
    request.session["flag"] = "add"

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "POST":
        contents = request.POST["contents"]
        flag = request.session.get("flag")
        
        if flag == "add":
            title = request.POST["title"]
        else:
            title = request.session.get("title")

        if title != "":
            progress = util.save_entry(title, contents, flag)

            if flag == "add" and progress == "existing":
                return render(request, "encyclopedia/createNewPage.html", {
                    "message": "File is already exist.",
                    "title": title,
                    "contents": contents
                })
            return HttpResponseRedirect(reverse("wikiContents", args=(title,)))
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

    request.session["flag"] = "add"
    return render(request, "encyclopedia/createNewPage.html")

def update(request, title):
    contents = util.get_entry(title)
    request.session["flag"] = "edit"
    request.session["title"] = title
    
    return render(request, "encyclopedia/editPage.html",{
        "title": title,
        "contents": contents
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
        "wikiDisplay": wikiDisplay,
        "entry": search
    })

def randomPage(request):
    randomPage = random.choice(tuple(util.list_entries()))

    return searchLogic(request, randomPage)


