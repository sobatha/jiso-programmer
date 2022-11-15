"""
try節はできるだけ短く、1つの目的に絞って処理を実装する
"""


def purchase_from_view(request):
    try:
        product_id = request.POST["product_id"]
        purchase_count = request.POST["purchase_count"]
    except Keyerror as e:
        # 必要なデータがPOSTされていない
        return render(request, "purchase/purchase.html", {"error": f"{e.arg[0]}は必須です"})

    try:
        purchase_count = int(purchase_count)
        if purchase_count < 0:
            raise ValueError
    except ValueError:
        return render(
            requesr, "purchase/purchase.html", {"error": "purchase_countは不正な値です"}
        )

    try:
        product = get_product_by_id(product_id)
    except DoesNotExit:
        return render(request, "purchase/purchase.html", {"error": "指定された商品が見つかりません"})

    if purchase_count > product.stock.count:
        return render(request, "purchase/purchase.html", {"error": "商品の在庫が不足しています"})

    # 購入の保存
    product.stock.count -= purchase_count
    product.stock.save()
    purchase = create_purchase(
        product=product,
        count=purchase_count,
        amount_price=purchase_count * product.price,
    )

    return render(request, "purchase/result.html", {"purchase": purchase})


# purchaseformを作る
class PurchaseForm(django.forms.Form):
    product = forms.IntegerField(label="商品")
    purchase_count = forms.IntergerField(label="個数", min_value=1, max_value=99)

    def clean_product(self):
        """
        The clean_<fieldname>() method is called on a form subclass where <fieldname> is replaced with the name
        of the form field attribute. This method does any cleaning that is specific to that particular attribute,
        unrelated to the type of field that it is. This method is not passed any parameters.
        You will need to look up the value of the field in self.cleaned_data and remember that
        it will be a Python object at this point, not the original string submitted in the form
         (it will be in cleaned_data because the general field clean() method,
         above, has already cleaned the data once).
        For example, if you wanted to validate that the contents of a CharField called serialnumber was unique,
        clean_serialnumber() would be the right place to do this.
        You dont need a specific field (its a CharField), but you want a formfield-specific piece of validation
        and, possibly, cleaning/normalizing the data.
        The return value of this method replaces the existing value in cleaned_data,
        so it must be the fields value from cleaned_data (even if this method didnt change it) or a new cleaned value.
        """
        try:
            return Product.objects.get(pk=self.cleaned_data["product"])
        except Product.DoesNotExist:
            raise forms.ValidationError("指定された商品が見つかりません")
