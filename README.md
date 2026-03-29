# jp-natural-voice-app

Style-Bert-VITS2 JP-Extra を使った日本語音声合成・音声クローン環境。

## 特徴

- Devcontainer で完結するローカル開発環境
- Windows + WSL2 + Docker Desktop + NVIDIA GPU 対応
- PyTorch 2.6 + CUDA 12.4 ベースのコンテナ
- 音声クローンモデルの学習・推論を CLI で実行

> **注意**: Gradio WebUI (`app.py`) は現在の依存バージョン制約（`huggingface_hub==0.19.4`）により起動不可です。学習・推論は CLI で行います。

## 動作確認済み環境

| 項目 | 内容 |
|---|---|
| OS | Windows + WSL2 Ubuntu |
| Docker | Docker Desktop on WSL2 |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU（VRAM 6GB） |
| Python | 3.10.20 |
| PyTorch | 2.6.0+cu124 |
| torchaudio | 2.4.0 |
| transformers | 4.37.2 |
| huggingface_hub | 0.19.4 |

## セットアップ

### 1. リポジトリのクローンと Devcontainer 起動

1. リポジトリをクローン
2. VS Code で `jp-natural-voice-app` を開く
3. 「Reopen in Container」を実行

### 2. Devcontainer 内での初期セットアップ（初回・再ビルド時）

Devcontainer 起動後、ターミナルで以下を順番に実行します。

```bash
# 必要なシステムパッケージのインストール
apt-get update && apt-get install -y ffmpeg build-essential cmake git-lfs

# uv のインストールとパッケージセットアップ
pip install uv
uv pip install -r requirements.txt --system

# PyTorch を cu124 版に差し替え（torchaudio は 2.4.0 固定）
uv pip uninstall torch torchaudio --system
uv pip install "torch>=2.6.0" "torchaudio==2.4.0" --index-url https://download.pytorch.org/whl/cu124 --system

# 追加パッケージ
uv pip install soxr --system
uv pip install faster-whisper --system

# Style-Bert-VITS2 の初期化（モデルのダウンロード）
python initialize.py

# バージョン固定（最後に上書き）
uv pip install "transformers==4.37.2" "huggingface_hub==0.19.4" --system
```

### 3. パッチの適用（初回・再ビルド時）

#### bert_feature.py パッチ

`word2ph` と `text` の長さ不一致による `assert` エラーを trim/pad で回避します。

```bash
python3 -c "
path = 'style_bert_vits2/nlp/japanese/bert_feature.py'
with open(path, 'r') as f:
    content = f.read()

old = '    text = text.replace(\"。\", \".\").replace(\"、\", \",\")\n    assert len(word2ph) == len(text) + 2, text'

new = '''    text = text.replace(\"。\", \".\").replace(\"、\", \",\")
    expected = len(text) + 2
    if len(word2ph) != expected:
        if len(word2ph) > expected:
            word2ph = word2ph[:expected]
        else:
            word2ph = word2ph + [1] * (expected - len(word2ph))'''

count = content.count(old)
print(f'Found {count} occurrence(s)')
if count > 0:
    content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)
    print('Patched!')
else:
    print('Pattern not found')
"
```

#### lightning_fabric パッチ

PyTorch 2.6 の `torch.load` デフォルト変更（`weights_only=True`）に対応します。

```bash
python3 -c "
path = '/usr/local/lib/python3.10/site-packages/lightning_fabric/utilities/cloud_io.py'
with open(path, 'r') as f:
    content = f.read()

old = '    fs = get_filesystem(path_or_url)\n    with fs.open(path_or_url, \"rb\") as f:\n        return torch.load(\n            f,\n            map_location=map_location,  # type: ignore[arg-type]\n            weights_only=weights_only,\n        )'

new = '    if weights_only is None:\n        weights_only = False\n    fs = get_filesystem(path_or_url)\n    with fs.open(path_or_url, \"rb\") as f:\n        return torch.load(\n            f,\n            map_location=map_location,  # type: ignore[arg-type]\n            weights_only=weights_only,\n        )'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)
    print('Patched!')
else:
    print('Pattern not found - check manually')
"
```

## 学習（Training）

### 1. 前処理

```bash
# BERT 特徴量の生成（.bert.pt）
python bert_gen.py --config Data/<モデル名>/config.json

# スタイルベクトルの生成（.npy）
python style_gen.py --config Data/<モデル名>/config.json
```

### 2. config.json の設定（VRAM 6GB 向け推奨値）

```bash
python3 -c "
import json
path = 'Data/<モデル名>/config.json'
with open(path, 'r') as f:
    config = json.load(f)
config['train']['batch_size'] = 2
config['train']['fp16_run'] = True
with open(path, 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print('batch_size:', config['train']['batch_size'])
print('fp16_run:', config['train']['fp16_run'])
"
```

### 3. 学習の実行

```bash
export MKL_THREADING_LAYER=GNU
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python train_ms_jp_extra.py -c Data/<モデル名>/config.json -m Data/<モデル名>
```

> **注意**: `-m` オプションには `Data/<モデル名>` のように `Data/` を含めること。省略すると `FileNotFoundError` が発生します。

### VRAM 不足（OOM）が発生した場合

`batch_size` をさらに下げてください：

```bash
python3 -c "
import json
path = 'Data/<モデル名>/config.json'
with open(path, 'r') as f:
    config = json.load(f)
config['train']['batch_size'] = 1
with open(path, 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print('batch_size:', config['train']['batch_size'])
"
```

## 固定バージョン（変更禁止）

以下のパッケージバージョンは動作確認済みの組み合わせです。変更すると互換性が壊れる可能性があります。

| パッケージ | バージョン | 理由 |
|---|---|---|
| torchaudio | 2.4.0 | それ以降のバージョンは非互換 |
| transformers | 4.37.2 | それ以降は huggingface_hub との非互換あり |
| huggingface_hub | 0.19.4 | transformers 4.37.2 と組み合わせ固定 |