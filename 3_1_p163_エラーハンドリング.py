'''
専用の例外クラスを自作して、エラーを明示的に実装する。
例外の親クラスを定義しておけば、例外処理を行うコードで同系統の例外をまとめて捕まえられるため、
簡潔でわかりやすい実装になる。
'''
# exceptions.py
class MailReceivingError(Exception):
    pretext =''
    def __init__(self, message, *args) -> None:
        if self.pretext:
            message = f"{self.pretext}: {message}"
        super().__init__(message, *args)

class MailConnectionError(MailReceivingError):
    pretext = '接続エラー'

class MailAuthError(MailReceivingError):
    pretext = '認証エラー　'

class MailHeaderError(MailReceivingError):
    pretext = 'メールヘッダーエラー'

#mail_serviceのメソッドを上記の例外を上げるように実装
#view.py
from . import service
from . import exceptions

def get_newest_mail(user):
    '''
    ユーザーのメールアドレスに届いている一時間以内の最新のメールを取得する
    直近一時間のメールがない場合、Noneを返す
    '''
    mail_service = service.get_mail_service()
    #MailConnectionError, MailAuthError等が発生する可能性がある
    mail_service.login(user.email, user.email_password)
    mail = mail_service.get_newest_mail()

    if mail.date < datetime.now() - timedelta(hours=1):
        return None
    return mail

def newmail(request):
    try:
        mail = het_newest_mail(request.user)
    except exceptions.MailReceivingError as e: # 継承している３つの例外クラスどれでも捕まえられる
        #logにWaringレベルで例外発生時のトレースバックを出力
        logger.warning('Mail Receiving Error', exc_info=True)
        return render(request, 'mail-receiving-error.html', context={'message': str(e)})

    else:
        if mail is None:
            #正常系のメッセージをわかりやすく表示
            return render(request, 'no-mail.html', context={'message': '一時間以内のメールはありません'})

    context = {
        'from': mail.from_, 'to':mail.to,
        'date': mail.date, 'subject':mail.subject,
        'excerpt': mail.body[:100],
    }
    return render(request, 'new_mail.html', context=context)