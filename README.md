以下に、Devcontainer 環境で Style-Bert-VITS2 JP-Extra を動かすための README.md を記載します。

---

# Style-Bert-VITS2 JP-Extra Devcontainer 環境

このリポジトリは、Windows + WSL2 + Docker Desktop 環境で、Style-Bert-VITS2 JP-Extra を Devcontainer として動かすための設定と手順をまとめたものです。

## 前提環境

- OS: Windows
- WSL2: Ubuntu
- Docker: Docker Desktop on WSL2
- GPU: NVIDIA GeForce RTX 3060
- ドライバ: NVIDIA-SMI 595.79, CUDA Version: 13.2（ホスト側）

WSL2 内で以下が動作確認済みであることを想定しています。

```bash
nvidia-smi
docker run --gpus all nvidia/cuda:11.8.0-base-ubuntu20.04 nvidia-smi
```

## ファイル構成

- `.devcontainer/Dockerfile`
- `.devcontainer/devcontainer.json`
- `requirements.txt`（Style-Bert-VITS2 のもの）

## Devcontainer の設定

### Dockerfile

```dockerfile
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

RUN apt-get update && apt-get install -y git

WORKDIR /workspace
```

### devcontainer.json

```json
{
  "name": "Style-Bert-VITS2 JP-Extra",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "runArgs": [
    "--gpus=all"
  ],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/opt/conda/bin/python"
      }
    }
  },
  "portsAttributes": {
    "7860": {
      "label": "Gradio WebUI"
    }
  },
  "forwardPorts": [
    7860
  ],
  "remoteUser": "root"
}
```

## セットアップ手順

### 1. Devcontainer の起動

VS Code でこのリポジトリを開き、「Reopen in Container」を実行して Devcontainer を起動します。

### 2. ffmpeg のインストール

```bash
apt-get update
apt-get install -y ffmpeg
```

### 3. pip パッケージのインストール

```bash
pip install --upgrade pip
pip install torchaudio librosa soundfile transformers accelerate pyyaml gradio numpy scipy jaconv fugashi unidic-lite ipadic openai-whisper
```

### 4. Style-Bert-VITS2 の初期化

```bash
cd /tmp
git clone https://github.com/litagin02/Style-Bert-VITS2.git
cd Style-Bert-VITS2
cp -r .git /workspaces/jp-natural-voice-app/
cp -r ./* /workspaces/jp-natural-voice-app/
cd /workspaces/jp-natural-voice-app
python initialize.py
```

※ `initialize.py` はモデルファイルのダウンロード・初期化を行います。数分〜十数分かかります。

### 5. 追加パッケージのインストール

```bash
pip install loguru onnxruntime pyworld num2words gradio
```

`pyworld` でビルドエラーが出る場合は、ビルド環境を整えます。

```bash
apt-get install -y build-essential cmake
pip install pyworld
```

### 6. `pyopenjtalk` のインストール

```bash
apt-get install -y build-essential cmake
pip install pyopenjtalk
```

### 7. `requirements.txt` の調整とインストール

`faster-whisper` が `av==10.*` を要求してビルドエラーになるため、`requirements.txt` から `faster-whisper` を除外します。

```bash
sed -i '/faster-whisper/d' requirements.txt
pip install -r requirements.txt
```

### 8. WebUI の起動

```bash
python app.py
```

ブラウザで `http://localhost:7860` にアクセスすると、Style-Bert-VITS2 の WebUI が表示されます。

## 音声クローンの作成手順

### 1. Dataset タブ

- 「音声ファイルをアップロード」で自分の声の WAV ファイルを複数アップロード
- 各音声に対応する書き起こしテキストを用意
- 「データセットの前処理」を実行

### 2. Train タブ

- モデル名、エポック数、バッチサイズなどを設定
- 「学習開始」を実行（GPU を使用し、数十分〜数時間かかります）

### 3. Inference タブ

- 学習済みモデルを選択
- テキストを入力し、「生成」ボタンを押す
- 自分の声で読み上げた音声が生成される

## 注意点

- `torch` は `requirements.txt` により `2.3.1` にダウングレードされますが、Style-Bert-VITS2 の動作には問題ありません。
- `transformers` の警告（`PyTorch >= 2.4 is required but found 2.3.1`）は無視して構いません。
- `faster-whisper` は除外していますが、Style-Bert-VITS2 の主要機能には影響しません。

## 参考リンク

- Style-Bert-VITS2 公式リポジトリ  
  [GitHub](https://github.com/litagin02/Style-Bert-VITS2)
- Style-Bert-VITS2 の使い方メモ（日本語）  
  [Zenn](https://zenn.dev/asap/articles/f8c0621cdd74cc)
- 自分の声をクローン化する方法（動画）  
  [YouTube](https://www.youtube.com/watch?v=LMtVOQtc9BE)

---

以上で、Devcontainer 環境での Style-Bert-VITS2 JP-Extra のセットアップと音声クローンの作成が可能になります。