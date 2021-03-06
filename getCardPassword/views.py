import shutil

from django.shortcuts import render
from django.http import HttpResponse

import re
#解压文件
import rarfile



def index(request):
    print(request.method)
    if request.method == 'POST':
        text = request.POST.get('cardText')
        print(text)
        matchObj = re.search(r'[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}',text)
        print(matchObj.group())
        return HttpResponse(matchObj.group())

    return render(request, 'getCardPassword/getCardPassword.html')




