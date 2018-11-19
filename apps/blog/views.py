from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.views import View

from apps.repertory import models

class homepage(View):
    def get(self, request, **kwargs):
        if not kwargs['type']:

            label_classify_obj = models.labelClassify.objects.all()
            label_obj = models.label.objects.all()
            active = 'all'
            show = None

            article_info_obj = models.articleInfo.objects.all()

            count = len(article_info_obj)
            result, remain = divmod(count, 9)

            page_count = result+1 if remain != 0 else result
            page = int( kwargs.get('page') ) if kwargs.get('page') != '' else 1

            if page_count >=5 :
                if page <= 2:
                    page_inner_str = ''
                    for i in range(1, 6):
                        if i == page and i == 1:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/">'+str(i)+'</a></li>'
                        elif i == page and i != 1:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/' + str(i) + '">' + str(i) + '</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/'+str(i)+'">'+str(i)+'</a></li>'
                elif page >= page_count-1:
                    page_inner_str = ''
                    for i in range(page_count-4, page_count+1):
                        if i == page:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/'+str(i)+'">'+str(i)+'</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/'+str(i)+'">'+str(i)+'</a></li>'
                else:
                    page_inner_str = ''
                    for i in range(page-2, page+3):
                        if i == page:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/'+str(i)+'">'+str(i)+'</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/'+str(i)+'">'+str(i)+'</a></li>'
            else:
                page_inner_str = ''
                for i in range(1, page_count + 1):
                    if i == page:
                        page_inner_str += '<li class="page-item active"><a class="page-link" href="/' + str(i) + '">' + str(i) + '</a></li>'
                    else:
                        page_inner_str += '<li class="page-item"><a class="page-link" href="/' + str(i) + '">' + str(i) + '</a></li>'
            page_front_str = '''
            <nav aria-label="Page navigation" class="float-right mt-3 mr-3">
                    <ul class="pagination">
                        <li class="page-item">
                            <a class="page-link" href="/" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                                <span class="sr-only">Previous</span>
                            </a>
                        </li>
                        '''
            page_back_str = '''
            <li class="page-item">
                            <a class="page-link" href="/'''+ str(page_count) +'''" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                                <span class="sr-only">Next</span>
                            </a>
                        </li>
                      </ul>
                </nav>
                '''
            article_info = article_info_obj[(page-1)*9:page*9]
            return render(request, 'homepage.html',{'label_classify': label_classify_obj,
                                                    'label': label_obj,
                                                    'active': active,
                                                    'show': show,
                                                    'article_info': article_info,
                                                    'page': page_front_str+page_inner_str+page_back_str} )
        else:
            type = kwargs.get('type')
            page = kwargs.get('page')
            # print(type, page)
            label_classify_obj = models.labelClassify.objects.all()
            label_obj = models.label.objects.all()
            active = int(type)
            show = None

            for label in label_obj:
                if label.id == int(type):
                    show = label.classify_id

            for label in label_obj:
                if label.id == int(type):
                    type_name = label.label_name

            article_info_obj = models.articleInfo.objects.filter(label_id = type_name)
            count = len(article_info_obj)
            result, remain = divmod(count, 9)

            page_count = result + 1 if remain != 0 else result
            page = int(page)
            if page_count >= 5:
                if page <= 2:
                    page_inner_str = ''
                    for i in range(1, 6):
                        if i == page:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/blog/classify-'+type+'-page-'+str(i)+'">'+str(i)+'</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/blog/classify-'+type+'-page-'+str(i)+'">'+str(i)+'</a></li>'
                elif page >= page_count-1:
                    page_inner_str = ''
                    for i in range(page_count-4, page_count+1):
                        if i == page:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'
                else:
                    page_inner_str = ''
                    for i in range(page-2, page+3):
                        if i == page:
                            page_inner_str += '<li class="page-item active"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'
                        else:
                            page_inner_str += '<li class="page-item"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'
            else:
                page_inner_str = ''
                for i in range(1, page_count+1):
                    if i == page:
                        page_inner_str += '<li class="page-item active"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'
                    else:
                        page_inner_str += '<li class="page-item"><a class="page-link" href="/blog/classify-' + type + '-page-' + str(i) + '">' + str(i) + '</a></li>'

            page_front_str = '''
                        <nav aria-label="Page navigation" class="float-right mt-3 mr-3">
                                <ul class="pagination">
                                    <li class="page-item">
                                        <a class="page-link" href="/blog/classify-'''+type+'-page-1/'+'''" aria-label="Previous">
                                            <span aria-hidden="true">&laquo;</span>
                                            <span class="sr-only">Previous</span>
                                        </a>
                                    </li>
                                    '''
            page_back_str = '''
                        <li class="page-item">
                                        <a class="page-link" href="/blog/classify-'''+type+'-page-'+str(page_count)+'''/" aria-label="Next">
                                            <span aria-hidden="true">&raquo;</span>
                                            <span class="sr-only">Next</span>
                                        </a>
                                    </li>
                                  </ul>
                            </nav>
                            '''

            article_info = article_info_obj[(page-1)*9:page*9]
            return render(request, 'homepage.html',{'label_classify': label_classify_obj,
                                                    'label': label_obj,
                                                    'active': active,
                                                    'show': show,
                                                    'article_info': article_info,
                                                    'page': page_front_str+page_inner_str+page_back_str} )

class articleContent(View):
    def get(self, request, **kwargs):
        aid = kwargs.get('article_id')
        article_info = models.articleInfo.objects.filter(id=aid).first()
        article_content = models.articleContent.objects.filter(article_id_id=aid).first()
        return render(request,'article_view.html',{'article_info': article_info,
                                                   'article_content': article_content})
