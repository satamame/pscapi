# /conv

フォーマットを変換する API です。  
入出力は JSON 形式です。  
Web アプリから呼んで使います。  

## エンドポイント

/conv

例1 - ローカルの開発サーバの場合
: http://127.0.0.1:8000/conv

例2 - Deta の場合
: https://j8bx8j.deta.dev/conv

## メソッド

POST

## クエリパラメタ

### from

値

- 'json' (デフォルト)
- 'fountain'

入力となる台本データ (リクエストボディの `data` フィールド) のフォーマットです。

### to

値

- 'json' (デフォルト)
- 'pdf'
- 'html'

出力となる台本データ (レスポンスボディの `data` フィールド) のフォーマットです。

## リクエストボディ

```json
{
    'data': str,
    'pdf_params': {
        'size': [w, h],
        'margin': [x, y],
        'upper_space': float,
        'font_name': str,
        'num_font_name': str,
        'font_size': float,
        'line_space': float,
        'draw_page_num': bool
    },
    'html_params': {
        'title': str,
        'template': str,
        'css': str,
        'js': str
    }
}
```

data
: 入力となる台本データ (必須)。

pdf_params
: 出力フォーマットが 'pdf' の場合に指定できるオプション (省略可)。  
詳しくは [playscript.conv.pdf.psc_to_pdf](https://satamame.github.io/playscript/master/playscript.conv.html#playscript.conv.pdf.psc_to_pdf) のパラメタを参照。

html_params
: 出力フォーマットが 'html' の場合に指定できるオプション (省略可)。  
詳しくは [playscript.conv.html.psc_to_html](https://satamame.github.io/playscript/master/playscript.conv.html#playscript.conv.html.psc_to_html) のパラメタを参照。

## レスポンスボディ

```json
{
    'format': str,
    'data': str
}
```

format
: 'json', 'pdf' または 'html'

data
: 出力データ。`format` が 'pdf' の場合は Base64 エンコードされたバイナリデータ。

## 呼び出し方の例

### 例1 - Fountain (日本式) から PDF に変換

(JavaScript)

```javascript
const url = 'https://j8bx8j.deta.dev/conv?from=fountain&to=pdf';
const text = 'Title: タイトル\nAuthor: 著者\n...'; // Fountain (日本式)
const body = JSON.stringify({
  data: text,
  pdf_params: { size: [595.28, 841.89] }, // A4 サイズ
});
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: body,
});
const data = await response.json();
const pdf = atob(data.data); // Base64 デコード
```

※ size パラメタはポイント単位で、1mm = 72/25.4 ポイント です。
- 210(mm) ≒ 595.28(pt)
- 297(mm) ≒ 841.89(pt)

### 例2 - Fountain (日本式) から HTML に変換

(JavaScript)

```javascript
const url = 'https://j8bx8j.deta.dev/conv?from=fountain&to=html';
const text = 'Title: タイトル\nAuthor: 著者\n...'; // Fountain (日本式)
const body = JSON.stringify({
  data: text,
  html_params: { title: '台本サンプル' }, // HTML のタイトル
});
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: body,
});
const data = await response.json();
const html = data.data;
```
