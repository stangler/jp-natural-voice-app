# CUDA 12.1 + PyTorch 2.4.0 + cuDNN 9 のイメージに変更
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# git だけ入れる（ffmpeg と pip install は後で）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace