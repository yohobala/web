import shutil

from django.shortcuts import render
from django.http import HttpResponse

import re
#解压文件
import rarfile

from PIL import Image
import pytesseract



def index(request):

    print(request.method)
    if request.method == 'POST':
        text = request.FILES.get('cardText')
        print(text.name)
        path = 'static/getCardPassword/' + text.name
        with open(path, 'wb') as f:
            for content in text.chunks():
                f.write(content)
        print(text)
        # image = Image.open('test.png')
        # content = pytesseract.image_to_string(image, lang='chi_sim')  # 解析图片
        matchObj = re.search(r'[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}',content)
        print(matchObj.group())
        return HttpResponse(matchObj.group())

    return render(request, 'getCardPassword/getCardPassword.html')




