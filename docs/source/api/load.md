# /load

Web 上にある台本データを取得する API です。  
Web ブラウザ等から呼んで、データをレスポンスとして受け取ります。

## エンドポイント

/load

例1 - ローカルの開発サーバの場合
: http://127.0.0.1:8000/load

例2 - Deta の場合
: https://pscapi-1-a9576981.deta.app/load

## メソッド

GET

## クエリパラメタ

### src

取得したい台本データの URI です。

### format

値

- 'fountain' (デフォルト)
- 'json'

取得したい台本データの Web 上でのフォーマットです。

### as

値

- 'pscv' (デフォルト)
- 'json'
- 'pdf'
- 'html'

レスポンスとして受け取るデータのフォーマットです。  
'pscv' を指定すると、[pscv (台本ビューア)](https://github.com/satamame/pscv) で読み込めるフォーマットになります。

### size

値

- 'A5' (デフォルト)
- 'A4'

PDF として受け取る時のページサイズです。

## 呼び出し方の例

### 例1 - Fountain (日本式) を pscv (台本ビューア) で読み込む

このリポジトリのサンプルを Deta 経由で読み込む場合です。  
以下の URI を [pscv](https://github.com/satamame/pscv) の「URL から取得する」に入力します。

```
https://pscapi-1-a9576981.deta.app/load?src=https://raw.githubusercontent.com/satamame/pscapi/main/sample/example.fountain
```

### 例2 - JSON を PDF としてダウンロードする

このリポジトリのサンプルを Deta 経由で読み込む場合です。  
以下の URI を Web ブラウザのアドレスバーに入力します。

```
https://pscapi-1-a9576981.deta.app/load?src=https://raw.githubusercontent.com/satamame/pscapi/main/sample/example.json&format=json&as=pdf
```
