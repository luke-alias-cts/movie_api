from django.shortcuts import render, HttpResponse
import json
import urllib.request
import pprint
# import os
from django.conf import settings


# Create your views here.
def index(request):
    return HttpResponse("Movie world")


def search(request):
    if request.method == 'GET':
        client_id = settings.NAVER_CLIENT_ID
        client_secret = settings.NAVER_CLIENT_SECRET
# 환경변수에 다가 id따로 저장해서 settings.py에 몰아넣어 관리함
        q = request.GET.get('q')  # html에 변수 붙이는거 쉽게 하기 위해
        encText = urllib.parse.quote("{}".format(q))  # 검색어 형식은 str로
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText  # json 결과
        # request라는 변수가 다르게 쓰이기 떄문에 변경함
        movie_api_request = urllib.request.Request(url)
        movie_api_request.add_header("X-NAVER-Client-Id", client_id)
        movie_api_request.add_header("X-NAVER-Client-Secret", client_secret)
        response = urllib.request.urlopen(movie_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            # result 변수 만들어서 json 파일 읽고
            # 그 결과를 items 변수에 집어 넣고 그걸 템플릿에 띄울 수 있게
            items = result.get('items')
            # print(result)  # request 출력

            context = {
                'items': items
            }
            return render(request, 'movie/search.html', context=context)
