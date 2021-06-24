from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from . import util
from django.core.files.storage import default_storage
from django import forms
from random import randint

class CreatePageForm(forms.Form):
    """docstring for create_page"""
    title = forms.CharField(label='title', max_length=100,required=True)
    content = forms.CharField( required=True,
              widget=forms.Textarea(attrs={"style":"height:200px",'placeholder': 'content'}))


class EditPageForm(forms.Form):
    """docstring for create_page"""
    content = forms.CharField(label='md content',
            required=True,widget=forms.Textarea(attrs={"style":"height:200px"}))        

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
       

def view_page(request,entry):
	if default_storage.exists(f"encyclopedia/templates/encyclopedia/{entry}.html"):
		return render(request,f"encyclopedia/{entry}.html", {
			"title":entry, "content": util.parse(entry),"edit":True}
			)
	elif (util.get_entry(entry)):
		util.parse(entry)
		return render(request,f"encyclopedia/{entry}.html", {
			"title":entry, "content": util.parse(entry),"edit":True}
			)
	else :
		return render(request,f"encyclopedia/error.html",{
			"title": "Error"})


def search(request):
    """
    Returns a list of all names of encyclopedia entries containing a key word,
    I the key ord matches a page name it redirects to that page
    """

    if request.method == "POST":
        entries= util.list_entries()
        key = request.POST.get('q')
        results=[]
        for entry in entries:
            if key == entry:
                return HttpResponseRedirect(reverse("encyclopedia:view_page", args=(entry,)))
            elif key !="" and key in entry:
                results.append(entry)
        return render(request,f"encyclopedia/search.html",{
        "title": "Results",
        "results":results
        })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    	
    

def create_page(request):
    """
    create an entry
    """
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if default_storage.exists(f"entries/{title}.md"):
                form._errors['title'] = [f"Entry ({title}) already exists"]
                return render(request, f"encyclopedia/create.html", {
                "form": form
            })

            content= form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("encyclopedia:view_page", args=(title,)))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
                "form": CreatePageForm()
            })


def edit(request,entry):
    """
    edit an entry
    """
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(entry,form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("encyclopedia:view_page", args=(entry,)))
    initial_content={"content":util.get_entry(entry)}
    form = EditPageForm(initial_content)
    return render(request, "encyclopedia/edit.html", {
                "form": form,"entry":entry,"title":f"Edit"
            })

def random(request):
    """
    return a random entry
    """
    entries= util.list_entries()
    number = randint(0,len(entries)-1)
    title = entries[number]
    return HttpResponseRedirect(reverse("encyclopedia:view_page",args=(title,)))
     # HttpResponse(view_page(request,entries[number]))

    
    
