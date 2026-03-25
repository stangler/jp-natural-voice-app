# jp-natural-voice-app

Style-Bert-VITS2 (JP-Extra) を使った日本語音声合成アプリ。

## 特徴

- Devcontainer で完結するローカル開発環境
- CUDA 11.8 + GPU 対応
- uv による依存管理
- Style-Bert-VITS2 (JP-Extra) による高品質な日本語音声合成

## セットアップ

1. リポジトリをクローン
2. VS Code で `jp-natural-voice-app` を開く
3. 「Reopen in Container」を実行
4. Devcontainer 起動後、自動で `.devcontainer/post-create.sh` が実行される

## モデルの準備

Style-Bert-VITS2 (JP-Extra) のモデルファイルを以下に配置してください。

- `/workspace/models/style-bert-vits2-jp-extra/config.yml`
- `/workspace/models/style-bert-vits2-jp-extra/model.pth`

（実際のダウンロード元は公式リポジトリや Hugging Face を参照）

## 実行

```bash
python main.py