# pscapi

## 概要

[playscript](https://github.com/satamame/playscript) というパッケージの機能を API として提供するプログラムです。  

### フォーマット変換

- 入力は [Fountain](https://satamame.github.io/playscript/master/fountain.html) または JSON 形式です。
    - sample フォルダにサンプル (example.fountain, example.json) があります。
- 出力は PDF, HTML, または JSON 形式です。
    - JSON 形式は [pscv (台本ビューア)](https://github.com/satamame/pscv) で使えます。

## デプロイ

[FastAPI のドキュメント](https://fastapi.tiangolo.com/ja/deployment/) を参考にデプロイしてください。

## APIs

(Work in progress)

## 呼び出し方の例

- ローカルで API を起動して JavaScript で [Fountain](https://satamame.github.io/playscript/master/fountain.html) から PDF に変換する場合です。
- `pdf_params` の仕様は playscript の [psc_to_pdf()](https://satamame.github.io/playscript/master/playscript.conv.html#playscript.conv.pdf.psc_to_pdf) 関数の引数に準じます。
- size パラメタはポイント単位で、1mm = 72/25.4 ポイント です。
    - 210(mm) ≒ 595.28(pt)
    - 297(mm) ≒ 841.89(pt)
- sample フォルダにその他の変換のサンプル (index.html) があります。

```javascript
const url = 'http://127.0.0.1:8000/conv?from=fountain&to=pdf';
const text = 'Title: タイトル\nAuthor: 著者\n...'; // Fountain 形式
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
const pdf = atob(data.data); // PDF は Base64 エンコードされている
```
