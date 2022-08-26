from django.shortcuts import render
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random, string

# Create your views here.
def home(request):
    return render(request,'home.html')

def createShortURL(request):
    char_url = ''
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST) #Pass on the data from current request
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            random_chars_list = list(string.ascii_letters)
            random_chars = ''
            for i in range(6):
                random_chars += random.choice(random_chars_list)
            while len(ShortURL.objects.filter(short_url=random_chars)) != 0:
                for i in range(6):
                    random_chars += random.choice(random_chars_list)
            date = datetime.now()
            s = ShortURL(original_url = original_website, short_url=random_chars,
                        time_date_created = date)            
            s.save()
            return render(request,'url-created.html',{'chars':random_chars})
    else:
        form = CreateNewShortURL()
        context = {'form':form}
        return render(request,'create.html',context)


def redirect(request,url):
    current_obj = ShortURL.objects.filter(short_url=url)
    if len(current_obj) <= 0:
        return render(request, 'page-not-found.html')
    context = {
        'obj':current_obj[0]
    }
    return render(request,'redirect.html',context)

