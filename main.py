#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

import torch
import numpy as np
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.utils.stdout_wrapper import SAFE_STDOUT


# モデルファイルの配置ディレクトリ
MODEL_DIR = Path("/workspaces/jp-natural-voice-app/models/style-bert-vits2-jp-extra/")
MODEL_PATH = MODEL_DIR / "NotAnimeJPManySpeaker_e120_s22200.safetensors"
CONFIG_PATH = MODEL_DIR / "config.json"
STYLE_VECTORS_PATH = MODEL_DIR / "style_vectors.npy"


def check_model_files():
    """必要なモデルファイルが存在するか確認する"""
    required_files = [
        MODEL_PATH,
        CONFIG_PATH,
        STYLE_VECTORS_PATH,
    ]
    missing = [f for f in required_files if not f.exists()]
    if missing:
        print("以下のファイルが見つかりません:", file=SAFE_STDOUT)
        for f in missing:
            print(f"  {f}", file=SAFE_STDOUT)
        print("\nダウンロード先:", file=SAFE_STDOUT)
        print("  config.json:", file=SAFE_STDOUT)
        print("    https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/config.json?download=true", file=SAFE_STDOUT)
        print("  NotAnimeJPManySpeaker_e120_s22200.safetensors:", file=SAFE_STDOUT)
        print("    https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/NotAnimeJPManySpeaker_e120_s22200.safetensors?download=true", file=SAFE_STDOUT)
        print("  style_vectors.npy:", file=SAFE_STDOUT)
        print("    https://huggingface.co/Mofa-Xingche/girl-style-bert-vits2-JPExtra-models/resolve/main/style_vectors.npy?download=true", file=SAFE_STDOUT)
        sys.exit(1)


def main():
    print("Style-Bert-VITS2 model", file=SAFE_STDOUT)

    # モデルファイルの存在確認
    check_model_files()

    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}", file=SAFE_STDOUT)

    # Style-Bert-VITS2 モデルのロード
    print("Loading Style-Bert-VITS2 model...", file=SAFE_STDOUT)
    from style_bert_vits2.models.infer import load_model
    model, config = load_model(
        model_path=str(MODEL_PATH),
        config_path=str(CONFIG_PATH),
        style_vec_path=str(STYLE_VECTORS_PATH),
        device=device,
    )
    print("Model loaded.", file=SAFE_STDOUT)

    # デフォルトパラメータ
    speaker_id = 0
    style = "Neutral"
    style_weight = 0.7
    sdp_ratio = 0.2
    noise_scale = 0.6
    noise_scale_w = 0.8
    length_scale = 1.0
    language = "JP"
    auto_split = True
    split_interval = 0.5
    assist_text_weight = 1.0
    assist_text = ""
    use_assist_text = False

    # テキスト入力
    text = input("合成したい日本語テキストを入力してください: ").strip()
    if not text:
        print("テキストが入力されていません。", file=SAFE_STDOUT)
        return

    # 音声合成
    print("音声合成中...", file=SAFE_STDOUT)
    try:
        wav = model.infer(
            text=text,
            language=language,
            speaker_id=speaker_id,
            reference_audio=None,
            sdp_ratio=sdp_ratio,
            noise=noise_scale,
            noisew=noise_scale_w,
            length=length_scale,
            style=style,
            style_weight=style_weight,
            auto_split=auto_split,
            split_interval=split_interval,
            assist_text=assist_text if use_assist_text else None,
            assist_text_weight=assist_text_weight,
        )
    except Exception as e:
        print(f"音声合成に失敗しました: {e}", file=SAFE_STDOUT)
        return

    # WAV ファイル出力
    output_path = Path("/workspace/output.wav")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    import soundfile as sf
    sf.write(str(output_path), wav, config.data.sampling_rate)
    print(f"音声ファイルを出力しました: {output_path}", file=SAFE_STDOUT)


if __name__ == "__main__":
    main()