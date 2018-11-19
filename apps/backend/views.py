from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from apps.backend.utils import verification
from apps.backend.utils import validation_img
from apps.repertory import models
from apps.utils import XSSfilter
from django.db import transaction
from io import BytesIO
import random
import json
import re
import time
import os

class login(View):
    @method_decorator(verification.auth_login)
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        status = {'state': '200', 'error': None, 'data': None}
        # 200登陆成功，303验证码错误，404用户名格式错误，405密码格式错误（为空，或带有非法字符），406用户名和密码格式都错误，505用户名或密码错误
        check_code = request.POST.get('identify_code', None)
        if request.session.get('checkCode', 'emmmmmmmmm').lower() != check_code.lower():
            status['state'] = '303'
            status['error'] = '验证码错误'
            return HttpResponse(json.dumps(status) )

        # 验证用户名和密码的格式
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # print(username,password)
        if len(username) == 0 or re.search('[\$#@+&!*?/\\\\]', username):
            if len(password) == 0 or re.search('[\$#@+&!*?/\\\\]', password):
                status['state'] = '406'
                print('both')
                return HttpResponse(json.dumps(status))
            else:
                status['state'] = '404'
                print('user')
                return HttpResponse(json.dumps(status))
        else:
            if len(password) == 0 or re.search('[\$#@+&!*?/\\\\]', password):
                status['state'] = '405'
                print('pwd')
                return HttpResponse(json.dumps(status))

        user_obj = models.userInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            status['state'] = '505'
            return HttpResponse(json.dumps(status))

        request.session['user'] = user_obj.username
        request.session['isLogin'] = True
        status['state'] = '200'
        status['data'] = "/manage/articles/"

        nosign = request.POST.get('nosign', 'no')
        if nosign == 'yes':
            request.session.set_expiry( 604800 )
        return HttpResponse(json.dumps(status) )

def checkCode(request):
    if request.method == 'GET':
        img = validation_img.check_code()
        check_img, check_code = img.create_img()
        stream = BytesIO()
        check_img.save(stream, 'JPEG')
        request.session['checkCode'] = check_code
        return HttpResponse(stream.getvalue())

class backendArticles(View):
    @method_decorator(verification.auth)
    def get(self, request, page):
        page = int(page) if page != '' else 1
        article_info = models.articleInfo.objects.all()
        count = len(article_info)

        result, remain = divmod(count, 12)
        page_count = result+1 if remain != 0 else result

        if page_count >= 3:
            if page < 2:
                page_inner_str = ''
                for i in range(1, 4):
                    if page == i:
                        page_inner_str += '<li class="page-item active"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
                    else:
                        page_inner_str += '<li class="page-item"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
            elif page > page_count-1:
                page_inner_str = ''
                for i in range(page_count-2, page_count+1):
                    if page == i:
                        page_inner_str += '<li class="page-item active"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
                    else:
                        page_inner_str += '<li class="page-item"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
            else:
                page_inner_str = ''
                for i in range(page-1, page+2):
                    if page == i:
                        page_inner_str += '<li class="page-item active"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
                    else:
                        page_inner_str += '<li class="page-item"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
        else:
            page_inner_str = ''
            for i in range(1, page_count+1):
                if page == i:
                    page_inner_str += '<li class="page-item active"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
                else:
                    page_inner_str += '<li class="page-item"><a class="page-link" href="/manage/articles/' + str(i) + '">' + str(i) + '</a></li>'
        page_front_str = '''
        <nav aria-label="Page navigation">
                    <ul class="pagination" style="margin-bottom: 0;">
                        <li class="page-item">
                            <a class="page-link" href="/manage/articles/" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                                <span class="sr-only">Previous</span>
                            </a>
                        </li>
        '''
        page_back_str = '''
        <li class="page-item">
                            <a class="page-link" href="/manage/articles/''' + str(page_count) + '''" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                                <span class="sr-only">Next</span>
                            </a>
                        </li>
                    </ul>
                </nav>
        '''
        article_info = article_info[(page-1)*12: page*12]
        return render(request, "article_manage.html", {'article': article_info, 'page': page_front_str+page_inner_str+page_back_str})

def articleDelete(request):
    if request.method == 'POST':
        status = {'state': True, 'data': None, 'error': None}
        id = request.POST.get('article_id')

        models.articleContent.objects.filter(article_id_id=id).delete()
        models.articleInfo.objects.filter(id=id).delete()

        return HttpResponse(json.dumps(status) )

def articlesEdit(request, id):
    if request.method == 'GET':
        article_info = models.articleInfo.objects.filter(id=id).first()
        article_content = models.articleContent.objects.filter(article_id_id=id).first()
        labels = models.label.objects.all()
        return render(request, 'article_edit.html', {'article_info': article_info, 'article_content': article_content, 'labels': labels} )

    elif request.method == 'POST':
        res = {'state': 200, 'data': None, 'error': None}
        # 301标题为空，302内容为空, 303标签为空，200提交成功
        title = request.POST.get('title')
        content = request.POST.get('content')
        label = request.POST.get('label')
        if re.match("^ *$", title):
            res['state'] = 301
            return HttpResponse(json.dumps(res) )
        if len(title) > 30:
            res['state'] = 3011
            return HttpResponse(json.dumps(res))
        filter_obj = XSSfilter.articleFilter()
        content, text = filter_obj.filter(content)
        if re.match("^ *$", text):
            res['state'] = 302
            return HttpResponse(json.dumps(res))
        if re.match("^ *$", label):
            res['state'] = 303
            return HttpResponse(json.dumps(res))
        # 插入数据，标题 标签 摘要
        with transaction.atomic():
            article_obj = models.articleInfo.objects.filter(id=id).first()
            article_obj.article_name = title
            article_obj.label_id = label
            article_obj.abstract = text[0:100]
            article_obj.save()
            article_content_obj = models.articleContent.objects.filter(article_id_id=id).update(article_content=content)
        res['state'] = 200
        return HttpResponse(json.dumps(res))

class backendLabel(View):
    @method_decorator(verification.auth)
    def get(self, request):
        return render(request, "label_manage.html")

class backendPublish(View):
    @method_decorator(verification.auth)
    def get(self, request):
        labels = models.label.objects.all()
        return render(request, "article_publish.html",{'label': labels})
    @method_decorator(verification.auth)
    def post(self, request):
        res = {'state': 200, 'data': None, 'error': None}
        # 301标题为空，302内容为空, 303标签为空，200提交成功, 3011标题过长
        title = request.POST.get('title')
        content = request.POST.get('content')
        label = request.POST.get('label')
        if re.match("^ *$", title):
            res['state'] = 301
            return HttpResponse(json.dumps(res) )
        if len(title) > 30:
            res['state'] = 3011
            return HttpResponse(json.dumps(res))
        filter_obj = XSSfilter.articleFilter()
        content, text = filter_obj.filter(content)
        if re.match("^ *$", text):
            res['state'] = 302
            return HttpResponse(json.dumps(res))
        if re.match("^ *$", label):
            res['state'] = 303
            return HttpResponse(json.dumps(res))
        # 插入数据，标题 标签 摘要
        with transaction.atomic():
            # obj = models.articleInfo.objects
            article_obj = models.articleInfo.objects.create(article_name=title,
                                              label_id=label,
                                              abstract=text[0:100])
            models.articleContent.objects.create(article_id=article_obj, article_content=content)
        res['state'] = 200
        return HttpResponse(json.dumps(res))

class exit(View):
    @method_decorator(verification.auth)
    def get(self, request):
        request.session.delete(request.session.session_key)
        return redirect('/manage/login/')

class user(View):
    @method_decorator(verification.auth)
    def get(self, request):
        return render(request, "user_manage.html")

@verification.auth
def article_imgs(request):
    if request.method == 'POST':
        try:
            article_img = request.FILES.get('upload_file')
            user = request.session['user']
            while True:
                part1 = time.strftime("%Y%m%d_%H%M%S_", time.localtime())
                part2 = str(random.randint(0,1000) )
                filename = user + "_article_" + part1 + part2 + ".jpg"
                path = os.path.join('static','upload','img', filename)
                res_path = "/static/upload/img/" + filename
                if not os.path.exists(path):
                    break
            with open(path, 'wb') as f:
                for item in article_img:
                    f.write(item)
            res = { 'success': True, 'msg': None, 'file_path': res_path }
            return HttpResponse(json.dumps(res))
        except Exception as e:
            error_msg = "catch exception: " + str(e)
            res = { 'success': False, 'msg': error_msg, 'file_path': None }
            return HttpResponse(json.dumps(res))





