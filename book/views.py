from django.shortcuts import render
from django.views import View
# Create your views here.

from .models import Book

class IndexView(View):

    #リクエストがGETメソッドのときの処理
    def get(self, request, *args, **kwargs):

        context = {}
        context["books"] = Book.objects.order_by("-dt")

        return render(request,"book/index.html",context)

index = IndexView.as_view()


class SingleView(View):

    def get(self, request, pk, *args, **kwargs):

        context = {}

        #pkを使って対象の書籍データを特定する。(idで一意に特定できるので単一のモデルオブジェクトを返却する)
        context["book"] = Book.objects.filter(id=pk).first()

        return render(request,"book/single.html",context)

single = SingleView.as_view()

