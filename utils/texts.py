# streamlitのmenubarを隠す
HIDE_ST_STYLE = """
<style>
div[data-testid="stToolbar"] {
visibility: hidden;
height: 0%;
position: fixed;
}
div[data-testid="stDecoration"] {
visibility: hidden;
height: 0%;
position: fixed;
}
#MainMenu {
visibility: hidden;
height: 0%;
}
header {
visibility: hidden;
height: 0%;
}
footer {
visibility: hidden;
height: 0%;
}
.appview-container .main .block-container{
    padding-top: 1rem;
    padding-right: 3rem;
    padding-left: 3rem;
    padding-bottom: 1rem;
}
.reportview-container {
    padding-top: 0rem;
    padding-right: 3rem;
    padding-left: 3rem;
    padding-bottom: 0rem;
}
header[data-testid="stHeader"] {
    z-index: -1;
}
div[data-testid="stToolbar"] {
z-index: 100;
}
div[data-testid="stDecoration"] {
z-index: 100;
}
</style>
"""


ABSTRACT = """
- Streamlitに対して、リアルタイム性という観点での簡易的な機能検証を行った。
- 具体的には、以下の処理を同時に実行するアプリを制作した。
    - 外部からのデータインプット
        - Webカメラ
        - スクリーンキャプチャ(※動画を流すことで、画像処理が実際のユースケースに近づく)
    - 内部処理
        - 無加工
        - 二値化
        - 背景差分
            - [高速道路のライブカメラ](https://www.youtube.com/results?search_query=%E3%83%A9%E3%82%A4%E3%83%96%E3%82%AB%E3%83%A1%E3%83%A9+%E9%AB%98%E9%80%9F%E9%81%93%E8%B7%AF) での検証がおすすめ
    - 処理結果のリアルタイム表示
    - 通知（トースト）
        - 今回は録画の開始/停止を想定した動作
        - 録画開始ボタンは画像処理と並行して通知表示ができることの簡易確認用であり、録画機能の内部処理は実装していない。

"""
