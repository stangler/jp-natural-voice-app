#!/bin/bash

set -e

echo "🔄 Setting up jp-natural-voice-app environment..."

# venv を作成
uv venv

# 依存関係をインストール
uv pip install -e .

# Style-Bert-VITS2 のモデルファイルをダウンロードする例
# 実際には GitHub Releases や Hugging Face から取得する想定
MODEL_DIR="/workspace/models/style-bert-vits2-jp-extra"
mkdir -p "$MODEL_DIR"

echo "✅ Setup completed."