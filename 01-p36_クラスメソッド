from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    name: str
    birthday: date
    id: int
    '''
    dont do
    def calc_age~~~
    これをすると、一度この関数を呼び出さないとageが使えない
    '''

    @proparty #ここでfunctools.cached_propertyを使うと、一度propartyが計算された後、更新されなくなる（計算を削減できるが、更新されないので不便）
    def age(self):
        today = date.today
        age = today.year - self.birthday.year
        if (self.birthday.month, self.birthday.day) > (today.month, today.day): #タプルの大小は前から順に評価
            age -= 1
        return age

    @classmethod #インスタンスを作る関数を、クラスメソッドにする　APIから取得すべきデータである場合、わけてimportしなくてよくて便利
    def retrieve(cls, id:int) -> 'User':
        """データAPIから情報を取得して、インスタンスとして返す"""
        res = requests.get(f'/api/products/{id}') #この処理は別途モジュールにAPIにアクセスするだけの関数としてまとめておくべき
        data = res.json
        return cls(
            id = data['id'],
            name=data['name'],
        )
