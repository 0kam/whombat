# Whombat 起動・停止スクリプト

このディレクトリには、Whombatアプリケーションを簡単に起動・停止するためのシェルスクリプトが含まれています。

## 📋 スクリプト一覧

### 🚀 start.sh - アプリケーション起動

バックエンド（FastAPI）とフロントエンド（Next.js）を同時に起動します。

```bash
./scripts/start.sh
```

**機能**:
- ポート使用状況の自動チェック
- 既存プロセスの自動停止
- バックエンドサーバー起動 (ポート5000)
- フロントエンドサーバー起動 (ポート3000)
- リアルタイムログ表示
- Ctrl+Cでの安全な終了

**ログファイル**:
- バックエンド: `logs/backend.log`
- フロントエンド: `logs/frontend.log`

**環境変数**:
```bash
# カスタムポートで起動
WHOMBAT_BACKEND_PORT=8000 WHOMBAT_FRONTEND_PORT=4000 ./scripts/start.sh
```

---

### 🛑 stop.sh - アプリケーション停止

実行中のすべてのWhombatサーバーを停止します。

```bash
./scripts/stop.sh
```

**機能**:
- バックエンドサーバー停止
- フロントエンドサーバー停止
- グレースフルシャットダウン（失敗時は強制終了）
- 残存プロセスのクリーンアップ

---

### 🔄 restart.sh - アプリケーション再起動

アプリケーションを停止してから再起動します。

```bash
./scripts/restart.sh
```

**使用例**:
- コード変更後の再起動
- 設定変更の反映
- トラブル時のリセット

---

### 📊 status.sh - ステータス確認

現在のアプリケーション状態を確認します。

```bash
./scripts/status.sh
```

**表示内容**:
- バックエンドの起動状態
- フロントエンドの起動状態
- プロセスID (PID)
- ヘルスチェック結果
- アクセスURL

**出力例**:
```
======================================
   Whombat Application Status
======================================

Backend (FastAPI):
  Port: 5000
  URL:  http://localhost:5000/docs
  Status: Running (PID: 12345)
  Process: python
  Health: Responding

Frontend (Next.js):
  Port: 3000
  URL:  http://localhost:3000
  Status: Running (PID: 12346)
  Process: node
  Health: Responding

✓ All services are running
```

---

## 🎯 使用方法

### 初回セットアップ

```bash
# 1. バックエンドの依存関係インストール
cd back
uv sync

# 2. フロントエンドの依存関係インストール
cd ../front
npm install

# 3. プロジェクトルートに戻る
cd ..
```

### 基本的なワークフロー

```bash
# アプリケーション起動
./scripts/start.sh

# ブラウザでアクセス
# http://localhost:3000

# ステータス確認
./scripts/status.sh

# 停止
./scripts/stop.sh
```

### 開発中の使用

```bash
# 起動（Ctrl+Cで終了可能）
./scripts/start.sh

# 別ターミナルでログ監視
tail -f logs/backend.log
tail -f logs/frontend.log

# コード変更後に再起動
./scripts/restart.sh
```

---

## 🔧 トラブルシューティング

### ポートが既に使用されている

スクリプトは自動的に既存プロセスを停止しますが、手動で停止する場合：

```bash
# バックエンドポート（5000）を解放
lsof -ti:5000 | xargs kill -9

# フロントエンドポート（3000）を解放
lsof -ti:3000 | xargs kill -9
```

### スクリプトが実行できない

実行権限を確認：

```bash
ls -l scripts/*.sh

# 権限がない場合は付与
chmod +x scripts/*.sh
```

### バックエンドが起動しない

1. ログを確認：
```bash
cat logs/backend.log
```

2. 仮想環境を確認：
```bash
cd back
ls -la .venv
```

3. 手動で起動テスト：
```bash
cd back
WHOMBAT_DEV=true uv run python -m whombat
```

### フロントエンドが起動しない

1. ログを確認：
```bash
cat logs/frontend.log
```

2. node_modulesを確認：
```bash
cd front
ls -la node_modules
```

3. 手動で起動テスト：
```bash
cd front
npm run dev
```

### ログが見つからない

ログディレクトリは自動作成されますが、手動で作成する場合：

```bash
mkdir -p logs
```

---

## 🌐 アクセスURL

起動後、以下のURLでアクセスできます：

| サービス | URL | 説明 |
|---------|-----|------|
| **フロントエンド** | http://localhost:3000 | メインアプリケーション |
| **API ドキュメント** | http://localhost:5000/docs | Swagger UI |
| **API ReDoc** | http://localhost:5000/redoc | ReDoc形式のAPIドキュメント |
| **バックエンド** | http://localhost:5000 | REST API エンドポイント |

---

## 📝 環境変数

スクリプトで使用できる環境変数：

| 変数名 | デフォルト値 | 説明 |
|--------|------------|------|
| `WHOMBAT_BACKEND_PORT` | 5000 | バックエンドのポート番号 |
| `WHOMBAT_FRONTEND_PORT` | 3000 | フロントエンドのポート番号 |
| `WHOMBAT_DEV` | true | 開発モード（start.shで自動設定） |

**使用例**:
```bash
# カスタムポートで起動
WHOMBAT_BACKEND_PORT=8080 WHOMBAT_FRONTEND_PORT=8081 ./scripts/start.sh

# ステータス確認も同じポートを使用
WHOMBAT_BACKEND_PORT=8080 WHOMBAT_FRONTEND_PORT=8081 ./scripts/status.sh
```

---

## 🔍 機能の確認

### 可視性制御機能のテスト手順

起動後、以下の手順で実装した可視性制御機能を確認できます：

1. **アカウント作成とログイン**
   - http://localhost:3000 にアクセス
   - 新規アカウントを作成

2. **データセット作成**
   - Datasets → Create Dataset
   - Visibilityセレクタを確認：
     - 🌍 Public
     - 👥 Restricted
     - 🔒 Private

3. **グループ機能**
   - Restrictedを選択するとGroupセレクタが表示される
   - まずAdmin画面でグループを作成
   - 自分をManagerロールで追加

4. **アノテーションプロジェクト**
   - Annotation Projects → Create Project
   - 同じVisibility機能を確認

5. **可視性バッジ**
   - 一覧画面で各アイテムのバッジを確認
   - 色分けとアイコンを確認

---

## 💡 Tips

### バックグラウンド実行

長時間実行する場合：

```bash
# nohupで起動（ログアウト後も実行継続）
nohup ./scripts/start.sh > /dev/null 2>&1 &

# tmux/screenを使用
tmux new -s whombat
./scripts/start.sh
# Ctrl+B, D でデタッチ

# 再接続
tmux attach -t whombat
```

### 定期的なログクリーンアップ

```bash
# ログファイルをクリア
> logs/backend.log
> logs/frontend.log

# または削除
rm logs/*.log
```

### systemdサービス化（Linux）

本番環境でsystemdサービスとして登録する例：

```bash
# /etc/systemd/system/whombat.service
[Unit]
Description=Whombat Application
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/whombat
ExecStart=/path/to/whombat/scripts/start.sh
ExecStop=/path/to/whombat/scripts/stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## 📞 サポート

問題が発生した場合：

1. ログファイルを確認：`logs/backend.log`, `logs/frontend.log`
2. ステータスを確認：`./scripts/status.sh`
3. GitHubのIssueを確認：https://github.com/mbsantiago/whombat/issues

---

**作成日**: 2025-10-18
**バージョン**: 1.0.0
