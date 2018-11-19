#Author:yehao
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re

class articleFilter(object):
    __instance = None

    def __init__(self):
        self.valid_tags = ['mark', 'br', 'span', 'a', 'img', 'b', 'strong', 'i', 'strike', 'u', 'font', 'p', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'hr']
        self.valid_attr = {
            'img': ['src', 'alt', 'width', 'height', 'data-non-image'],
            'a': ['href', 'target'],
            'font': ['color'],
            'code': ['class'],
        }
        self.valid_style = {
            'span': ['color', 'font-size'],
            'b': ['color'],
            'i': ['color'],
            'strong': ['color'],
            'strike': ['color'],
            'u': ['color'],
            'p': ['margin-left', 'text-align'],
            'h1': ['margin-left', 'text-align'],
            'h2': ['margin-left', 'text-align'],
            'h3': ['margin-left', 'text-align'],
            'h4': ['margin-left', 'text-align']
        }
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
        return cls.__instance

    def filter(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup.find_all(recursive=True):
            if tag.name not in self.valid_tags:
                tag.hidden = True
                if tag.name not in ['html', 'body']:
                    tag.clear()
                continue

            attr = self.valid_attr.get(tag.name, [])
            attr.append('style')
            tag_attr = list(tag.attrs.keys())
            for item in tag_attr:
                if item not in attr:
                    del tag[item]

            style = tag.get('style', '').strip()
            if ';' in style:
                style_list = style.split(';')
                if '' in style_list:
                    style_list.remove('')
                # print(style_list)
                for item in style_list:
                    style_attr = item.split(':')[0].strip()
                    # print(style_attr)
                    if style_attr not in self.valid_style.get(tag.name, []):
                        style_list[ style_list.index(item) ] = ''
                while True:
                    if '' in style_list:
                        style_list.remove('')
                    else:
                        break
                if len(style_list) > 0:
                    style = ';'.join(style_list) + ';'
                    tag['style'] = style
                else:
                    del tag['style']
            else:
                if ':' in style:
                    style_attr = style.split(':')[0].strip()
                    if style_attr not in self.valid_style.get(tag.name, []):
                        del tag['style']
                    else:
                        style = style + ';'
                        tag['style'] = style
        text = soup.get_text().strip()
        text = ''.join( re.split('['+chr(10)+'\n]', text) )
        return soup.decode(), text

if __name__ == '__main__':
    html = '''
<p class='abcd' style="margin-left: 0px;color: red;height:100px"><mark style='color:red;'>第一行</mark></p>
<p style="margin-left: 0px;"><span style="font-size: 1.5em">第二行</span></p>
<p style="margin-left: 0px;">第三行</p>
<p style="margin-left: 0px;"><span style="color: rgb(227, 55, 55);">彩色文字</span><br></p>
<script>alert(123);</script>
<div><p>123</p>123</div>'''
    xss_filter = articleFilter()
    xss_filter.filter(html)

