# jp-natural-voice-app

Style-Bert-VITS2 JP-Extra を使った日本語音声合成・音声クローン環境。

## 特徴

- Devcontainer で完結するローカル開発環境
- Windows + WSL2 + Docker Desktop + NVIDIA GPU 対応
- PyTorch 2.4 + CUDA 12.1 ベースのコンテナ
- Gradio WebUI による Dataset / Train / Inference 操作

## セットアップ

### 1. リポジトリのクローンと Devcontainer 起動

1. リポジトリをクローン
2. VS Code で `jp-natural-voice-app` を開く
3. 「Reopen in Container」を実行

### 2. Devcontainer 内での初期セットアップ（初回のみ）

Devcontainer 起動後、ターミナルで以下を実行します。

```bash
# ffmpeg のインストール
apt-get update
apt-get install -y ffmpeg

# pip パッケージのインストール
pip install --upgrade pip
pip install torchaudio librosa soundfile transformers accelerate pyyaml gradio numpy scipy jaconv fugashi unidic-lite ipadic openai-whisper loguru onnxruntime pyworld num2words faster-whisper soxr

# Style-Bert-VITS2 の初期化
python initialize.py