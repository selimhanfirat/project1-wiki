from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.urls import reverse
import markdown2
from random import choice
from . import util


template_name = "encyclopedia/article.html"

def index(request):
    entries = util.list_entries()  # Retrieve the list of entries
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

    
import re

def new_page(request):
    if request.method == "POST":
        content = request.POST.get("content")
        article_name = request.POST.get("article_name").strip()

        # Check if the article name is empty or contains only special characters
        if not article_name or re.match(r'^\W+$', article_name):
            error_message = "Invalid article name"
            return render(request, "encyclopedia/new_page.html", {"error_message": error_message})

        util.save_entry(article_name, content)
        new_page_url = reverse('article', kwargs={'article_name': article_name})
        return HttpResponseRedirect(new_page_url)
    
    return render(request, "encyclopedia/new_page.html")


def article(request, article_name):
    content = util.get_entry(article_name)
    if content == None:
        raise Http404("Page not found")
    
    return render(request, template_name, {
        "article_content": markdown2.markdown(content),
        "article_name": article_name   
    })
    
def random(request):
    article_name = choice(util.list_entries())
    content = util.get_entry(article_name)
    return render(request, template_name, {
        "article_content": markdown2.markdown(content),
        "article_name": article_name   
    })
    
def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        searched = searched.strip()
        if searched in util.list_entries():
            return HttpResponseRedirect(reverse('article', kwargs={'article_name': searched}))
        else: 
            search_results = list()
            for entry in util.list_entries():
                if searched.lower() in entry.lower():
                    search_results.append(entry)
            return render(request, "encyclopedia/search_results.html", {
                "search_results": search_results
            })
    else:
        return render(request, "encyclopedia/cindex.html", {
        "entries": util.list_entries()
    })

def edit_article(request, article_name):
    if request.method == "POST":
        return render(request, "encyclopedia/edit_page.html",{
            "article_name": article_name,
            "content": util.get_entry(article_name)})

def save_edited_article(request, article_name):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(article_name, content)
        return HttpResponseRedirect(reverse('article', kwargs={'article_name': article_name}))
    else:
        # Handle GET request or other methods
        return HttpResponseBadRequest("Invalid request")

