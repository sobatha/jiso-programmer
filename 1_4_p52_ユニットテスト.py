
"""
関数の引数やfixtureに大げさな値が必要な設計にしない
処理を分離して、すべての動作確認にすべてのデータが必要ないようにする
関数やクラスを分離して、細かいテストは分離した関数、クラスを対象に行う
（分離した関数を呼び出す関数では、細かいテストは書かないようにする）
"""
#sales.py
import csv
from dataclasses import dataclass
from typing import List

@dataclass
class Sale:
    id: int
    item_id: int
    price: int
    amount: int

    def validate(self):
        if self['price'] <= 0:
            raise ValueError("Invalid sale.price")
        if self['amount'] <= 0:
            raise ValueError("Invalid sale.amount")

    @proparty
    def price(self):
        return self.amount * self.price
    
@dataclass
class Sales:
    data: List[Sale]

    @proparty
    def price(self):
        return sum(self.price for sale in self.data)

    @classmethod
    def from_asset(cls, path="./sales.csv"):
        data = []
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    sale = Sale(**row)
                    sale.validate()
                except Exception:
                    #TODO: Logging
                    continue
                data.append(sale)
        return cls(data=data)

#test.py
import pytest

class TestSale:
    def test_validate_invalid_price(self):
        sale = Sale(1, 1, 0, 2)
        with pytest.raises(ValueError):
            sale.validate

class TestSales:
    def test_from_asset_invalid_row(self):
        #TODO

