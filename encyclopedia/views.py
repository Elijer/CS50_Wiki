from markdown2 import Markdown
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import render

from django import forms

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")
    # priority = forms.IntegerField(label="Priority", min_value = 1, max_value = 5)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    converted_content = convertToMarkdown(content)
    return render(request, "encyclopedia/entry.html", {
        "content": converted_content,
        "title": entry.capitalize(),
        "form": NewSearchForm()
    })

def search(request):
    if request.method == "GET":
        entry = request.GET['q']
        content = util.get_entry(entry)
        if content != None:
            return redirect(reverse("wiki:entry", args = [entry]))
        elif entry:
            bigList = util.list_entries()
            results = util.search_entries(bigList, entry)
            # return HttpResponse(results)
            if results:
                return render(request, "encyclopedia/search.html", {
                    "results": results,
                    "term": entry,
                    "form": NewSearchForm()
                })
            else:
                return HttpResponse("We got no leads on that search, sorry.")

            # return HttpResponse(bigList)
            #CSSDjangoGitHTMLHTTPPythonTerminal
            
"""             if results:
                #return HttpResponse(results)
                print(results)
                return render(request, "encyclopedia/search.html", {
                    "results": results,
                    "term": entry,
                    "form": NewSearchForm()
                }) """
            # else:
                # return HttpResponse("no good results for your search")
            #return HttpResponse("Hey dave!")
    # return HttpResponse("Hey dave!")

def convertToMarkdown(content):
    markdowner = Markdown()
    converted_content = markdowner.convert(content)
    return converted_content