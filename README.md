# Gmail一斉送信ツール 基本設計書

## 1. システム概要
本ツールは、Google Gmail API を使用して、CSVファイルで指定された複数の宛先に個別メールを一斉送信する Python スクリプトです。送信結果はログファイル（CSV形式）に記録されます。

---

## 2. 利用技術

| 項目           | 内容                                         |
|----------------|----------------------------------------------|
| 言語           | Python 3.10〜3.12 推奨                       |
| ライブラリ     | google-api-python-client, google-auth-oauthlib, csv, base64, email など |
| 外部サービス   | Gmail API（Google Cloud Platform）           |
| 認証方式       | OAuth 2.0（`token.json` によるトークン管理） |

---

## 3. フォルダ構成

/SendMail/
├── main.py # メインスクリプト
├── credentials.json # Google Cloud Consoleから取得した認証情報
├── token.json # 実行後に生成されるユーザー認証トークン
├── recipients.csv # 宛先リスト（name,email）
├── log.csv # 送信結果ログ

---

## 4. 機能仕様

### 4.1 宛先リストの読み込み
- ファイル名：`recipients.csv`
- 形式：1行目が `name,email` のヘッダー
- 内容を辞書リストとして読み込み、1件ずつ処理

### 4.2 メール送信処理
- 使用API：`users().messages().send()`
- 宛先：CSVに記載された `email`
- 件名：固定（例：一斉送信テスト）
- 本文：テンプレート文字列に `name` を差し込む形式

### 4.3 送信ログ出力
- ファイル名：`log.csv`
- 出力形式：`name,email,status`
- ステータス：成功（✅）／失敗（✖）

### 4.4 エラーハンドリング
- Gmail API の送信時に `HttpError` を捕捉し、ログ出力

---

## 5. 操作方法

1. `credentials.json` を同ディレクトリに配置
2. `recipients.csv` に宛先情報を記入（`name,email` の列）
3. 仮想環境内で依存ライブラリをインストール：
   ```bash
   pip install -r requirements.txt

## ライセンス
このプロジェクトは [MIT License](LICENSE) のもとで公開しています。
