#Author:yehao
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

__lower_letters = "abcdefghjkmnpqrstuvwxy"    # 小写字母，去除可能干扰的i，l，o，z
__upper_letters = __lower_letters.upper()
__numbers = ''.join([ str(i) for i in range(3, 10) ])

init_chars = __lower_letters+__upper_letters+__numbers

class check_code(object):
    def __init__(self, length=4, img_type="JPEG", mode="RGB", bg_color=(255, 255, 255), fg_color=(0, 0, 255), chars=init_chars,
                 size=(100, 40), font_size=18, font_type="Monaco.ttf", draw_lines=True, n_line=(1, 2), draw_points=True, point_chance=2):
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.length = 4
        self.chars = chars
        self.font_size = font_size
        self.font_type = font_type
        self.img_type = img_type
        self.mode = mode
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.draw_lines = draw_lines
        self.n_line = n_line
        self.draw_points = draw_points
        self.point_chance = point_chance
    def __create_lines(self, draw):
        line_num = random.randint(*self.n_line)
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, self.width), random.randint(0, self.height))
            # 结束点
            end = (random.randint(0, self.width), random.randint(0, self.height))
            draw.line([begin, end], fill=(0, 0, 0))
    def __create_points(self, draw):
        chance = min(100, max(0, self.point_chance) )  # 大小限制在[0, 100]
        for w in range(self.width):
            for h in range(self.height):
                tmp = random.randint(0, 99)
                if tmp < chance:
                    draw.point((w, h), fill=(0, 0, 0) )
    def __create_strs(self, draw):
        check_code_list = random.sample(self.chars, self.length)
        check_code_chars = '%s ' % (' '.join(check_code_list) )

        font = ImageFont.truetype(self.font_type, self.font_size)
        font_width, font_height = font.getsize(check_code_chars)

        draw.text( ( (self.width - font_width) / 3, (self.height - font_height) / 3),
                   check_code_chars, font=font, fill=self.fg_color)

        return ''.join(check_code_list)

    def create_img(self):
        img = Image.new(self.mode, self.size, self.bg_color)
        draw = ImageDraw.Draw(img)
        if self.draw_lines:
            self.__create_lines(draw)
        if self.draw_points:
            self.__create_points(draw)
        strs = self.__create_strs(draw)

        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                 ]
        img = img.transform( self.size, Image.PERSPECTIVE, params )
        img = img.filter( ImageFilter.EDGE_ENHANCE_MORE )

        return img, strs


