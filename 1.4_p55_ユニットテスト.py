"""
テストから外部環境への依存を排除する
"""

#api.py
import requests

def post_to_sns(body):
    res = requests.post('https://example.com/posts', json={"body":body})
    return res.json()

def get_post(post_id):
    res = requests.get(f'https://example.com/posts/{post_id}')
    return res.json()

#test.py
'''
外部へアクセスするテストは
動作が遅くなる、ローカル環境にファイルが溜まりすぎる、クラウドサービスの利用料がかかるなどの悪影響が出るため避ける
避ける方法としては
responsesをつかって、requestsをモックする
RDB : バックエンドを切り替える
クラウドサービス: motoでモックに置き換える 
環境: tempfileを使う、仮想環境下で行う
'''

import responses
from .api import get_post, post_to_sns

class TestPostToSns:
    @responses.activate
    def test_post(self):
        responsed.add(responses.POST, 'https://example.com/posts', json={"body":"レスポンス本文"})
        data = post_to_sns("投稿の本文")
        
        assert len(responses.calls)==1
        assert responses.calls[0].request.body == '{"body": "投稿の本文"}'