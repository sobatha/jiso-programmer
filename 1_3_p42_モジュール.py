#ビジネスロジックを専用のモジュールに分割する

#payment.py
from some_payment_asp import purchase_item

def render_purchase_mail(item):
    return render_to_string('payment/item_purchase.txt', {'item':item}) #render_to_string関数はファイルの中身を読み取って、文字列型を返す

def purchase(user, item, amount):
    purchase_item(user.card.asp_id, item.asp_id, amount=amount)
    PurchaseHistory.objects.create(item=item, user=request.user)
    body = render_purchase_mail(item)
    send_mail(
        '購入が完了しました',
        body,
        settings.PAYMENT_PURCHASE_MAIL,
        [user.email],
        fail_silently=False, #When it’s False, send_mail() will raise an smtplib.SMTPException if an error occurs
    )
