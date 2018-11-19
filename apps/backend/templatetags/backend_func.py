#Author:yehao
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
import re

register = template.Library()

@register.filter
def multi_text(string):
    string = string.replace('\n','\\n')
    return string