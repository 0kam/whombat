# Whombat クイックスタートガイド

このガイドでは、Whombatアプリケーションを最速で起動する方法を説明します。

## 📦 起動方法の選択

Whombatには2つの起動方法があります：

- **🐳 Docker版（推奨）**: 最も簡単で信頼性が高い
- **💻 開発版（uv + npm）**: 開発やカスタマイズ向け

---

## 🐳 Docker版で起動（推奨）

### Step 1: 環境設定

```bash
# .envファイルを作成
cp .env.example .env

# .envを編集してオーディオディレクトリを設定
# WHOMBAT_AUDIO_DIR=/path/to/your/audio/files
nano .env
```

### Step 2: 起動

```bash
./scripts/docker.sh start
```

### Step 3: アクセス

ブラウザで http://localhost:5000 を開く

**詳細**: [DOCKER.md](DOCKER.md) を参照

---

## 💻 開発版で起動（uv + npm）

### Step 1: 依存関係のインストール（初回のみ）

```bash
# バックエンドの依存関係
cd back
uv sync

# フロントエンドの依存関係
cd ../front
npm install

# プロジェクトルートに戻る
cd ..
```

### Step 2: アプリケーション起動

```bash
./scripts/start.sh
```

起動完了まで約30秒かかります。以下のメッセージが表示されれば成功です：

```
======================================
   🚀 Whombat is now running!
======================================
Frontend:  http://localhost:3000
Backend:   http://localhost:5000
API Docs:  http://localhost:5000/docs
```

### Step 3: ブラウザでアクセス

ブラウザで http://localhost:3000 を開く

---

## 📌 よく使うコマンド

### Docker版

```bash
# 起動
./scripts/docker.sh start

# 停止
./scripts/docker.sh stop

# 再起動
./scripts/docker.sh restart

# ステータス確認
./scripts/docker.sh status

# ログ表示
./scripts/docker.sh logs
```

### 開発版（uv + npm）

```bash
# 起動
./scripts/start.sh

# 停止
./scripts/stop.sh

# 再起動
./scripts/restart.sh

# ステータス確認
./scripts/status.sh
```

---

## 🎯 可視性制御機能の使い方

### 1. アカウント作成

1. http://localhost:3000 にアクセス
2. 「Sign Up」をクリック
3. ユーザー情報を入力して登録

### 2. データセットの作成

1. 左メニューから「Datasets」を選択
2. 「Create Dataset」をクリック
3. 必要な情報を入力：
   - **Name**: データセット名
   - **Description**: 説明
   - **Audio Directory**: 音声ファイルのディレクトリパス
   - **Visibility**: 可視性レベルを選択
     - 🌍 **Public**: 全認証ユーザーが閲覧可能
     - 👥 **Restricted**: 選択したグループメンバーのみ閲覧可能
     - 🔒 **Private**: あなたのみ閲覧可能

4. Restrictedを選択した場合：
   - Groupセレクタが表示される
   - あなたがManagerであるグループのみ選択可能

### 3. グループの作成（Restricted機能を使う場合）

1. Admin権限が必要
2. 左メニューから「Admin」→「Groups」を選択
3. 「Create Group」をクリック
4. グループ名と説明を入力
5. メンバーを追加し、ロールを設定：
   - **Manager**: グループ管理権限、Restrictedリソース作成可能
   - **Member**: グループリソースの閲覧のみ

### 4. アノテーションプロジェクトの作成

1. 左メニューから「Annotation Projects」を選択
2. 「Create Project」をクリック
3. データセットと同じVisibility設定が可能

---

## 🔍 可視性レベルの詳細

| レベル | アイコン | 誰が見れる？ | 誰が編集できる？ | 使用例 |
|--------|---------|------------|---------------|--------|
| **Public** | 🌍 | 全認証ユーザー | 作成者のみ | 公開データセット |
| **Restricted** | 👥 | グループメンバー | グループManager | チーム共有プロジェクト |
| **Private** | 🔒 | 作成者のみ | 作成者のみ | 個人用データ |

---

## 💡 Tips

### ログの確認

```bash
# バックエンドのログ
tail -f logs/backend.log

# フロントエンドのログ
tail -f logs/frontend.log
```

### トラブルシューティング

**問題**: ポートが既に使用されている

```bash
# 強制停止
./scripts/stop.sh
```

**問題**: 起動に失敗する

```bash
# ログを確認
cat logs/backend.log
cat logs/frontend.log

# 手動で起動テスト
cd back
WHOMBAT_DEV=true uv run python -m whombat

cd ../front
npm run dev
```

**問題**: データベースエラー

```bash
# データベースをリセット（開発環境のみ）
cd back
rm -f whombat.db
uv run alembic upgrade head
```

---

## 🌐 アクセスURL一覧

| サービス | URL | 説明 |
|---------|-----|------|
| **メインアプリ** | http://localhost:3000 | フロントエンド |
| **API Docs** | http://localhost:5000/docs | Swagger UI |
| **ReDoc** | http://localhost:5000/redoc | API仕様書 |
| **API** | http://localhost:5000/api/v1 | REST API |

---

## 📚 詳細ドキュメント

- **起動スクリプト**: [scripts/README.md](scripts/README.md)
- **可視性制御実装**: [VISIBILITY_IMPLEMENTATION_COMPLETE.md](VISIBILITY_IMPLEMENTATION_COMPLETE.md)
- **実装計画**: [VISIBILITY_CONTROL_PLAN_v2.md](VISIBILITY_CONTROL_PLAN_v2.md)

---

## 🎓 さらに学ぶ

### API仕様の確認

1. http://localhost:5000/docs にアクセス
2. 各エンドポイントの説明を確認
3. 「Try it out」で直接APIをテスト可能

### データベースの確認

```bash
cd back
uv run python

>>> from whombat.models import Dataset, AnnotationProject
>>> # モデルを調査
```

### フロントエンドのStorybookを確認

```bash
cd front
npm run storybook
# http://localhost:6006 でアクセス
```

---

## 🛟 サポート

問題が発生した場合：

1. **ステータス確認**: `./scripts/status.sh`
2. **ログ確認**: `logs/backend.log`, `logs/frontend.log`
3. **再起動**: `./scripts/restart.sh`
4. **Issue報告**: https://github.com/mbsantiago/whombat/issues

---

**最終更新**: 2025-10-18
**バージョン**: 0.8.6

Happy Annotating! 🎵🔊
