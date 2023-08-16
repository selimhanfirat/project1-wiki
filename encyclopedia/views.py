from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
import markdown2
from . import util

template_name = "encyclopedia/article.html"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def new_page(request):
    if request.method == "POST":
        content = request.POST.get("content")
        article_name = request.POST.get("article_name").strip()  # Remove whitespace
        util.save_entry(content, article_name)
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