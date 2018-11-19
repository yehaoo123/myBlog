#Author:yehao
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect

def auth_login(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('isLogin', False):
            return redirect('/manage/articles/')
        else:
            res = func(request, *args, **kwargs)
            return res
    return wrapper

def auth(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('isLogin', False):
            res = func(request, *args, **kwargs)
            return res
        else:
            return redirect('/manage/login/')
    return wrapper