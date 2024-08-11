from django.shortcuts import render

from . import util
from markdown2 import Markdown
import random

def convert_md_html(title):
    filename = util.get_entry(title)
    markdowner = Markdown()
    if filename != None:
        return markdowner.convert(filename)
    else:
        return None
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(req, title):
    html = convert_md_html(title)
    if html == None:
        return render(req, "encyclopedia/error.html", {
            "title": "Page Not Found",
            "statusCode": 404,
            "message": f"{title} Not Found"
        })
    else:
        return render(req, "encyclopedia/page.html", {
            "title": title,
            "body": html
        })
        
def search(req):
    if req.method == "POST":
        search_input = req.POST["q"]
        html = convert_md_html(search_input)
        
        if html is not None:
            return render(req, "encyclopedia/page.html", {
            "title": search_input,
            "body": html
        })
        else:
            all_entries = util.list_entries()
            result = []
            
            for entry in all_entries:
                if search_input.lower() in entry.lower():
                    result.append(entry)
                
            if not result:
                return render(req, "encyclopedia/error.html", {
                    "title": "No Results",
                    "statusCode": 404,
                    "message": f"{search_input} Not Found"
                })
                
            return render(req, "encyclopedia/search.html", {
                        "entries": result
                    })
            
def create_page(req):
    if req.method == "GET":
        return render(req, "encyclopedia/create.html", {
            "title": "Create A New Page",
            
        })
    else:
        title = req.POST["title"]
        content = req.POST["content"]
        isExist = util.get_entry(title)
        if isExist is not None:
            return render(req, "encyclopedia/error.html", {
                    "title": "Title Is already exist",
                    "statusCode": 400,
                    "message": f"{title} Is Already Exist"
                })
        else:
            util.save_entry(title, content)
            html = convert_md_html(title)
            return render(req, "encyclopedia/page.html", {
            "title": title,
            "body": html
        })
    
def edit_page(req):
    if req.method == "POST":
        title = req.POST["title"]
        content = util.get_entry(title)
        return render(req, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
        
def save_edit(req):
    if req.method == "POST":
        title = req.POST["title"]
        content = req.POST["content"]
        util.save_entry(title, content)
        html = convert_md_html(title)
        return render(req, "encyclopedia/page.html", {
        "title": title,
        "body": html
        })
        
def random_page(req):
    allEntries = util.list_entries()
    result = random.choice(allEntries)
    html = convert_md_html(result)
    return render(req, "encyclopedia/page.html", {
        "title": result,
        "body": html
        })