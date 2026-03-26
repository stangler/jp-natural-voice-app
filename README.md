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

- `/workspaces/jp-natural-voice-app/models/style-bert-vits2-jp-extra/config.json`
- `/workspaces/jp-natural-voice-app/models/style-bert-vits2-jp-extra/NotAnimeJPManySpeaker_e120_s22200.safetensors`
- `/workspaces/jp-natural-voice-app/models/style-bert-vits2-jp-extra/style_vectors.npy`

### ダウンロード元（Hugging Face）

- `config.json`  
  https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/config.json?download=true
- `NotAnimeJPManySpeaker_e120_s22200.safetensors`  
  https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/NotAnimeJPManySpeaker_e120_s22200.safetensors?download=true
- `style_vectors.npy`  
  https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/style_vectors.npy?download=true

## 実行

```bash
python main.py
```

実行すると、日本語テキストの入力が求められます。  
合成された音声は `/workspace/output.wav` に出力されます。