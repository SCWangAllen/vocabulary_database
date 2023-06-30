from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from .models import Word,get_word_info,insert_to_notion,filter_or_insert
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
import re
import json
# import enchant
# eng_dictionary = enchant.Dict("en_US")


def add_word(english_word, ):
    word, created = Word.objects.get_or_create(
        english_word=english_word,
    )
    return word, created


# 在資料庫中刪除某個單字的資料
def delete_word(english_word):
    try:
        word = Word.objects.get(english_word=english_word)
        word.delete()
    except Word.DoesNotExist:
        print(f'Word "{english_word}" does not exist in the database.')


# Create your views here.
def index(request):
    return render(request,'cambridge/index.html')

# 一開始這樣寫，每次重新整理很煩，稍做調整
def app(request:WSGIRequest):
    if request.method == 'GET':
        return render(request, 'cambridge/app.html', {'keyword': '','word_info':[]})
    if request.method == 'POST':
        try :
            insert=request.POST['save_note']
        except :
            insert=False
        search_query = request.POST['search_query']
        if not re.match("^[A-Za-z]*$", search_query):
            info = [{'definition': '不是全英文', 'translation': '不是全英文', 'examples': []}]
        elif insert==False:
            print('show the result')
            info=get_word_info(search_query)

        else:
            print('insert to notion')
            try:
                info = get_word_info(search_query)
                filter_or_insert(keyword=search_query,word_info=info.get('definition'),title=info.get('word'))
                return render(request, 'cambridge/app.html', {'keyword': search_query,'word_info':info.get('definition')})
            except: 
                info = [{'definition': '單字有誤,無法儲存', 'translation': '單字有誤,無法儲存', 'examples': []}]
                return render(request, 'cambridge/app.html', {'keyword': search_query,'word_info':info})
        
    

def search_result(request, search_query):
    info = request.session.get('search_result', [])
    return render(request, 'cambridge/app.html', {'keyword': search_query, 'word_info': info})

# 留給自己製作的Extension做的，因此先忽略
@csrf_exempt
def for_extension(request):
    # Parse JSON data from request body
    data = json.loads(request.body)
    text = data.get('text')
    url = data.get('url')
    if not re.match("^[A-Za-z]*$", text):
            info = [{'definition': '無效的單詞', 'translation': '無效的單詞', 'examples': []}]
            return JsonResponse({'status': 'not a valid word'})
    try:
        info=get_word_info(text)
        filter_or_insert(keyword=text,url=url,word_info=info.get('definition'),title=info.get('word'))
        return JsonResponse({'status': 'Update Sucess'})
    except  :
        return JsonResponse({'status': 'failed'})
