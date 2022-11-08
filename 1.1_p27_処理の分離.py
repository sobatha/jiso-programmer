'''
Form: 入力のバリデーションチェック
View: 値の入出力と、処理全体の制御のみ
Model: データの保存
        データベースに情報を永続化する
        永続化されたデータを条件を指定して取得する
        よくある処理をモデルのプロパティーやQuerySetに実装する

'''


#validators.py
from django.core.exception import PermissionDenied

def validate_membership_permission(user, shop, role):
    if not user.memberships.filter(role=role, shop=shop).exists(): #existsは存在するか否かをBoolで返す
        raise PermissionDenied

#forms.py
class ItemSearchForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name",)

    def filter_items(self, items):
        name = self.cleaned_date["name"]
        items = items.filter(name__contains=name)
        return items

#models.py
class ItemQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_at__isnull=False)    
class Item(models.Model):
    name = models.CharField(min_length=3, max_length=127)
    published_at = models.DateTimeField(null=True, blank=True)
    objects = ItemQuerySet.as_manager()

    @proparty
    def price_tax_incl(self):
        return cal_tax_included(self.price)

#他の方法 
# Managerクラスを追加　
# ほかにもManagerクラスにメソッドを追加するやり方もある　しかしManagerクラス追加だと、クエリセットが返されるので複数のメゾットを重ねられない
# クエリセットからやる方が重ねられて便利
class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='A')

class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='E')

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=[('A', _('Author')), ('E', _('Editor'))])
    people = models.Manager()
    authors = AuthorManager()
    editors = EditorManager()

#views.py
@login_required
def item_list_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    validate_membership_permission(request.user, shop, Membership.ROLE_OWNER)

    items = Item.objects.filter(shop=shop).published()
    form = ItemSearchForm(request.GET)
    if form.is_valid():
        items = form.filter_items(items)
    return TemplateResponse(request, 'items/item_list.html', {"items":items, "form": form})


