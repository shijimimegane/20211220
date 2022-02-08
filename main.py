import requests
import json
import streamlit as st
import threading
from mycomponent import mycomponent

x = "x"
y = st.empty()
value = mycomponent(my_input_value=x, y=y)
# st.write("Received", value)

placeholder = st.empty()
placeholder.write(x)

dict_values = {'マグナN': ['Lv60 ティアマト・マグナ',
  'Lv80 コロッサス・マグナ',
  'Lv70 リヴァイアサン・マグナ',
  'Lv70 ユグドラシル・マグナ',
  'Lv85 シュヴァリエ・マグナ',
  'Lv85 セレスト・マグナ'],
 '旧石マルチ': ['Lv100 ナタク',
  'Lv100 フラム＝グラス',
  'Lv100 マキュラ・マリウス',
  'Lv100 メドゥーサ',
  'Lv100 アポロン',
  'Lv100 Dエンジェル・オリヴィエ'],
 '新石マルチ': ['Lv100 アテナ',
  'Lv100 グラニ',
  'Lv100 バアル',
  'Lv100 ガルーダ',
  'Lv100 オーディン',
  'Lv100 リッチ'],
 'その他N': ['Lv100 ジ・オーダー・グランデ',
  'Lv100 プロトバハムート',
  'Lv100 黄龍',
  'Lv100 黒麒麟',
  'Lv100 ミカエル',
  'Lv100 ガブリエル',
  'Lv100 ウリエル',
  'Lv100 ラファエル',
  'Lv150 アルティメットバハムート'],
 'マグナHL': ['Lv100 ティアマト・マグナ',
  'Lv100 コロッサス・マグナ',
  'Lv100 リヴァイアサン・マグナ',
  'Lv100 ユグドラシル・マグナ',
  'Lv100 シュヴァリエ・マグナ',
  'Lv100 セレスト・マグナ'],
 '旧石HL': ['Lv120 ナタク',
  'Lv120 フラム＝グラス',
  'Lv120 マキュラ・マリウス',
  'Lv120 メドゥーサ',
  'Lv120 アポロン',
  'Lv120 Dエンジェル・オリヴィエ'],
 'マグナII': ['Lv120 シヴァ',
  'Lv120 エウロペ',
  'Lv120 ブローディア',
  'Lv120 グリームニル',
  'Lv120 メタトロン',
  'Lv120 アバター'],
 '高級鞄': ['Lv120 プロメテウス',
  'Lv120 カー・オン',
  'Lv120 ギルガメッシュ',
  'Lv120 バイヴカハ',
  'Lv120 ヘクトル',
  'Lv120 アヌビス'],
 'マリス': ['Lv150 ティアマト・マリス',
  'Lv150 リヴァイアサン・マリス',
  'Lv150 フロネシス',
  'Lv150 シュヴァリエ・マリス',
  'Lv150 アニマ・アニムス・コア'],
 '☆６': ['黄龍・黒麒麟HL', 'Lv150 ルシファー', '四大天司ＨＬ', 'Lv200 リンドブルム'],
 '☆７': ['Lv200 ウィルナス',
  'Lv200 ワムデュス',
  'Lv200 イーウィヤ',
  'Lv200 ガレオン',
  'Lv200 ル・オー',
  'Lv200 フェディエル'],
 '☆８': ['Lv150 プロトバハムート',
  'Lv200 アーカーシャ',
  'Lv200 ジ・オーダー・グランデ',
  'Lv200 アルティメットバハムート'],
 '☆９': ['Lv250 ルシファー', 'Lv250 ベルゼバブ', 'Lv250 ベリアル'],
 '古戦場': ['Lv90 マンモス', 'Lv95 マンモス']}

class Stream_Listener_V2(object):
    def __init__(self):
        self.bearer_token = st.secrets["bearer_token"]
        self.base_url = "https://api.twitter.com/2/tweets/search/stream"
        self.headers={"Authorization": f"Bearer {self.bearer_token}"}
    def bearer_oauth(self, r):
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FilteredStreamPython"
        return r

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                response.status_code, response.text,
                )
            )
        # print(json.dumps(response.json()))
        return response.json()

    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        # print(json.dumps(response.json()))

    def set_rule(self, item):
        rule = [{"value": "参戦ID {}".format(item), "tag": "JPN"}]
        payload = {"add": rule}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        # print(response)
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                response.status_code, response.text,
                )
            )
        # print(json.dumps(response.json()))
        return response.json()

    def get_stream(self):

        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            auth=self.bearer_oauth, stream=True,
        )
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
            
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                text = json_response['data']['text']
                mark = text.find(':参戦ID')
                raid_id = text[mark - 9:mark - 1]
                global x
                x = raid_id
                placeholder.write(raid_id)

listener = Stream_Listener_V2()
st.title('Search & Copy')

kind_selected = st.selectbox(
    'マルチの種類',
    list(dict_values.keys()),
    index=11
)

target = st.selectbox(
    '対象',
    dict_values[kind_selected]
)

start_button = st.button('開始')

if start_button:
    
    listener.set_rule(target)
    listener.get_stream()
