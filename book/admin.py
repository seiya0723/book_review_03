from django.contrib import admin
from django.utils.html import format_html


from .models import Book,Category
from .forms import BookForm,BookAdminForm

import requests,re,datetime

class BookAdmin(admin.ModelAdmin):
    list_display = [ "isbn","category","title","format_thumbnail","dt","author","description","published","format_info" ]

    search_fields = [ "title","author","description" ]
    list_filter = [ "category" ]

    form = BookAdminForm


    #画像のフィールドはimgタグで画像そのものを表示させる
    def format_thumbnail(self,obj):
        if obj.thumbnail:
            return format_html('<img src="{}" alt="画像" style="width:5rem">', obj.thumbnail)

    #画像を表示するときのラベル(photoのverbose_nameをそのまま参照している)
    format_thumbnail.short_description      = Book.thumbnail.field.verbose_name
    format_thumbnail.empty_value_display    = "画像なし"

    def format_info(self,obj):
        if obj.info:
            return format_html('<a href="{}">詳細情報</a>', obj.info)

    format_info.short_description      = Book.info.field.verbose_name
    format_info.empty_value_display    = "詳細情報なし"



    #TODO:保存した時、ISBN検索を実行、不足している情報があれば埋める
    def save_model(self, request, obj, form, change):

        print("管理サイトから保存をする")

        #ここが保存する処理
        super(BookAdmin, self).save_model(request, obj, form, change)

        #TIPS:objは新規作成で記録するデータを含むモデルオブジェクト

        #下記のいずれかがnullであれば検索を実行する
        #全てに値がある場合は終了(アーリーリターン)
        if obj.title and obj.author and obj.description and obj.published and obj.thumbnail and obj.info:
            return False

        try:
            result  = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + obj.isbn )
        except:
            print("通信エラー")
            return False

        
        #返却されたJSONを辞書型に変換する。
        data    = result.json()

        if data["totalItems"] != 1:
            return False

        print(data["items"][0]["volumeInfo"]["title"])
        print(data["items"][0]["volumeInfo"]["publishedDate"])
        print(data["items"][0]["volumeInfo"]["authors"])
        print(data["items"][0]["volumeInfo"]["description"])
        print(data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"])
        print(data["items"][0]["volumeInfo"]["infoLink"])


        obj.title       = data["items"][0]["volumeInfo"]["title"]
        obj.author      = data["items"][0]["volumeInfo"]["authors"][0]
        obj.description = data["items"][0]["volumeInfo"]["description"]

        #日付は変換する必要があるため、下記は通用しない。(XXXX-XXとXXXX-XX-XXの2パターンある。)
        #obj.published   = data["items"][0]["volumeInfo"]["publishedDate"]

        dt  = data["items"][0]["volumeInfo"]["publishedDate"]

        match   = re.search(r"\d{4}-\d{2}-\d{2}", dt)
        if match:
            print("年月日のパターン")
            print(match.group())

            dt_str          = match.group()
            obj.published   = datetime.datetime.strptime(dt_str, "%Y-%m-%d")

        else:
            match   = re.search(r"\d{4}-\d{2}", dt)
            if match:
                print("年月のパターン")
                print(match.group())

                dt_str          = match.group()
                obj.published   = datetime.datetime.strptime(dt_str+"-01", "%Y-%m-%d")

        obj.thumbnail   = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        obj.info        = data["items"][0]["volumeInfo"]["infoLink"]

        form    = BookForm(obj.__dict__, instance=obj)
        
        if form.is_valid():
            form.save()


admin.site.register(Book,BookAdmin)
admin.site.register(Category)
