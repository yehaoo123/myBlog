#Author:yehao
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random

_lower_letters = "abcdefghjkmnpqrstuvwxy"    # 小写字母，去除可能干扰的i，l，o，z
_upper_letters = _lower_letters.upper()
_numbers = ''.join([ str(i) for i in range(3, 10) ])

init_chars = _lower_letters+_upper_letters+_numbers

print(init_chars)

a = random.choice(init_chars)
print(a)

check_code_list = ['1','2','3','4']
strs = ' %s ' % ' '.join(check_code_list)

print(strs)

