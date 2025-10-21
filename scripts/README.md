# Whombat Scripts

このディレクトリには、Whombatアプリケーションを管理するためのスクリプトが含まれています。

## 📋 スクリプト一覧

```
scripts/
├── start.sh          # 🚀 アプリケーション起動 (両方)
├── stop.sh           # 🛑 アプリケーション停止 (両方)
├── restart.sh        # 🔄 アプリケーション再起動 (両方)
├── status.sh         # 📊 ステータス確認
├── backend.sh        # ⚙️  バックエンド個別制御
├── frontend.sh       # 🎨 フロントエンド個別制御
├── setup.sh          # 📦 初回セットアップ
└── README.md         # 📚 このファイル
```

---

## 🚀 クイックスタート

### 1. 初回セットアップ

```bash
# 依存関係のインストールと環境設定
./scripts/setup.sh

# .envファイルを編集してドメインを設定
vim .env
# WHOMBAT_DOMAIN=your-server-ip-or-domain
```

### 2. アプリケーション起動

```bash
# 両方のサーバーを起動
./scripts/start.sh
```

### 3. ステータス確認

```bash
./scripts/status.sh
```

### 4. アプリケーション停止

```bash
./scripts/stop.sh
```

---

## 📖 詳細な使い方

### setup.sh - 初回セットアップ

開発環境を初めてセットアップする際に使用します。

```bash
./scripts/setup.sh
```

**実行内容:**
- システム要件のチェック (Python, uv, Node.js, npm)
- バックエンドの依存関係インストール (`uv sync`)
- フロントエンドの依存関係インストール (`npm install`)
- `.env`ファイルの作成 (`.env.example`から)
- ログディレクトリの作成

**必要な環境:**
- Python 3.11+
- uv ([インストールガイド](https://docs.astral.sh/uv/getting-started/installation/))
- Node.js 18+
- npm

---

### start.sh - アプリケーション起動

バックエンドとフロントエンドを同時に起動します。

```bash
./scripts/start.sh
```

**機能:**
- 環境変数の読み込み (`.env`)
- フロントエンド設定の自動生成 (`front/.env`)
- ポート使用状況の確認
- 既存プロセスの自動停止
- バックエンドサーバー起動 (デフォルト: ポート5000)
- フロントエンドサーバー起動 (デフォルト: ポート3000)
- リアルタイムログ表示

**ログファイル:**
- バックエンド: `logs/backend.log`
- フロントエンド: `logs/frontend.log`

**停止方法:**
- `Ctrl+C` で両方のサーバーを安全に停止
- または別ターミナルで `./scripts/stop.sh`

---

### stop.sh - アプリケーション停止

実行中のすべてのWhombatサーバーを停止します。

```bash
./scripts/stop.sh
```

**機能:**
- グレースフルシャットダウン (失敗時は強制終了)
- バックエンドサーバー停止
- フロントエンドサーバー停止
- 残存プロセスのクリーンアップ

---

### restart.sh - アプリケーション再起動

アプリケーションを停止してから再起動します。

```bash
./scripts/restart.sh
```

**使用例:**
- コード変更後の再起動
- 設定変更の反映 (`.env`変更後など)
- トラブル時のリセット

---

### status.sh - ステータス確認

現在のアプリケーション状態を確認します。

```bash
./scripts/status.sh
```

**表示内容:**
- バックエンドの起動状態
- フロントエンドの起動状態
- プロセスID (PID)
- ヘルスチェック結果
- アクセスURL
- 設定情報 (ドメイン、プロトコル)

**出力例:**
```
======================================
   Whombat Application Status
======================================

Backend (FastAPI):
  Port: 5000
  URL:  http://localhost:5000/docs
  Status: Running (PID: 12345)
  Process: python3
  Health: Responding

Frontend (Next.js):
  Port: 3000
  URL:  http://localhost:3000
  Status: Running (PID: 12346)
  Process: node
  Health: Responding

======================================

✓ All services are running

Access the application at:
  Frontend:  http://192.168.1.100:3000
  Backend:   http://192.168.1.100:5000
  API Docs:  http://192.168.1.100:5000/docs

Configuration:
  Domain:   192.168.1.100
  Protocol: http
```

---

### backend.sh - バックエンド個別制御

バックエンドサーバーのみを制御します。**開発時に便利です。**

```bash
# 起動
./scripts/backend.sh start

# 停止
./scripts/backend.sh stop

# 再起動
./scripts/backend.sh restart

# ログ表示
./scripts/backend.sh logs

# ステータス確認
./scripts/backend.sh status
```

**使用例:**
- API開発中、バックエンドのみ再起動したい
- バックエンドのログだけを監視したい
- フロントエンドは別の開発者が起動している

---

### frontend.sh - フロントエンド個別制御

フロントエンドサーバーのみを制御します。**開発時に便利です。**

```bash
# 起動
./scripts/frontend.sh start

# 停止
./scripts/frontend.sh stop

# 再起動
./scripts/frontend.sh restart

# ログ表示
./scripts/frontend.sh logs

# ステータス確認
./scripts/frontend.sh status
```

**使用例:**
- UI開発中、フロントエンドのみ再起動したい
- フロントエンドのログだけを監視したい
- バックエンドは別の開発者が起動している

---

## 🎯 よくある使用パターン

### パターン1: 本番環境での起動

```bash
# 初回セットアップ
./scripts/setup.sh
vim .env  # ドメイン設定

# 起動
./scripts/start.sh

# 動作確認
./scripts/status.sh
```

### パターン2: 開発環境での使用

```bash
# 起動（Ctrl+Cで終了可能）
./scripts/start.sh

# 別ターミナルでログ監視
./scripts/backend.sh logs
# または
./scripts/frontend.sh logs

# コード変更後に再起動
./scripts/restart.sh
```

### パターン3: バックエンド開発時

```bash
# フロントエンドとバックエンドを起動
./scripts/start.sh

# 別ターミナルでバックエンドAPI開発
# API変更後、バックエンドのみ再起動
./scripts/backend.sh restart

# バックエンドログを監視
./scripts/backend.sh logs
```

### パターン4: フロントエンド開発時

```bash
# 両方起動
./scripts/start.sh

# 別ターミナルでフロントエンドUI開発
# UI変更後、フロントエンドのみ再起動
./scripts/frontend.sh restart

# フロントエンドログを監視
./scripts/frontend.sh logs
```

### パターン5: デバッグ時

```bash
# ステータス確認
./scripts/status.sh

# 問題がある場合、個別に起動してログ確認
./scripts/stop.sh
./scripts/backend.sh start
# ログを確認...

./scripts/frontend.sh start
# ログを確認...
```

---

## 🔧 環境変数

すべてのスクリプトは `.env` ファイルから設定を読み込みます。

### 主要な環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|------------|------|
| `WHOMBAT_DOMAIN` | `localhost` | アクセスするドメインまたはIPアドレス |
| `WHOMBAT_HOST` | `0.0.0.0` | バインドするネットワークインターフェース |
| `WHOMBAT_PORT` | `5000` | バックエンドのポート番号 |
| `WHOMBAT_FRONTEND_PORT` | `3000` | フロントエンドのポート番号 |
| `WHOMBAT_PROTOCOL` | `http` | プロトコル (`http` または `https`) |
| `WHOMBAT_DEV` | `true` | 開発モード |

### 設定例

**ローカル開発:**
```bash
# .env
WHOMBAT_DOMAIN=localhost
WHOMBAT_HOST=localhost
WHOMBAT_DEV=true
```

**リモートサーバー:**
```bash
# .env
WHOMBAT_DOMAIN=192.168.1.100
WHOMBAT_HOST=0.0.0.0
WHOMBAT_DEV=false
```

詳細は [CONFIGURATION.md](../CONFIGURATION.md) を参照してください。

---

## 🔍 トラブルシューティング

### ポートが既に使用されている

スクリプトは自動的に既存プロセスを停止しますが、手動で停止する場合:

```bash
# バックエンドポート（5000）を解放
lsof -ti:5000 | xargs kill -9

# フロントエンドポート（3000）を解放
lsof -ti:3000 | xargs kill -9
```

### スクリプトが実行できない

実行権限を確認:

```bash
ls -l scripts/*.sh

# 権限がない場合は付与
chmod +x scripts/*.sh
```

### バックエンドが起動しない

1. ログを確認:
```bash
./scripts/backend.sh logs
# または
cat logs/backend.log
```

2. 仮想環境を確認:
```bash
cd back
ls -la .venv
```

3. 再セットアップ:
```bash
./scripts/setup.sh
```

### フロントエンドが起動しない

1. ログを確認:
```bash
./scripts/frontend.sh logs
# または
cat logs/frontend.log
```

2. node_modulesを確認:
```bash
cd front
ls -la node_modules
```

3. 再セットアップ:
```bash
./scripts/setup.sh
```

### 環境変数が反映されない

```bash
# .envファイルを確認
cat .env

# 再起動
./scripts/restart.sh
```

---

## 🌐 アクセスURL

起動後、以下のURLでアクセスできます（デフォルト設定の場合）:

| サービス | URL | 説明 |
|---------|-----|------|
| **フロントエンド** | http://localhost:3000 | メインアプリケーション |
| **API ドキュメント** | http://localhost:5000/docs | Swagger UI |
| **API ReDoc** | http://localhost:5000/redoc | ReDoc形式のAPIドキュメント |
| **バックエンド** | http://localhost:5000 | REST API エンドポイント |

**注意:** ドメイン設定により URLは変わります。`./scripts/status.sh` で実際のURLを確認してください。

---

## 💡 Tips

### バックグラウンド実行

長時間実行する場合:

```bash
# nohupで起動（ログアウト後も実行継続）
nohup ./scripts/start.sh > /dev/null 2>&1 &

# tmux/screenを使用（推奨）
tmux new -s whombat
./scripts/start.sh
# Ctrl+B, D でデタッチ

# 再接続
tmux attach -t whombat
```

### ログ管理

```bash
# リアルタイムでログを監視
./scripts/backend.sh logs   # バックエンド
./scripts/frontend.sh logs  # フロントエンド

# 両方のログを同時に監視
tail -f logs/backend.log logs/frontend.log

# ログをクリア
> logs/backend.log
> logs/frontend.log
```

### 開発効率化

```bash
# エイリアスを設定 (.bashrc または .zshrc)
alias whombat-start='cd /path/to/whombat && ./scripts/start.sh'
alias whombat-stop='cd /path/to/whombat && ./scripts/stop.sh'
alias whombat-status='cd /path/to/whombat && ./scripts/status.sh'
alias whombat-backend='cd /path/to/whombat && ./scripts/backend.sh'
alias whombat-frontend='cd /path/to/whombat && ./scripts/frontend.sh'
```

---

## 📚 関連ドキュメント

- [CONFIGURATION.md](../CONFIGURATION.md) - 詳細な設定ガイド
- [.env.example](../.env.example) - 環境変数の例

---

## 📞 サポート

問題が発生した場合:

1. ログファイルを確認: `logs/backend.log`, `logs/frontend.log`
2. ステータスを確認: `./scripts/status.sh`
3. 設定を確認: `.env`, `CONFIGURATION.md`
4. GitHubのIssueを確認: https://github.com/mbsantiago/whombat/issues

---

**更新日**: 2025-10-21
**対応環境**: Linux
