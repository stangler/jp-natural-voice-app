FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# CUDA 11.8 のベースイメージを使う前提なので、ここでは追加の CUDA インストールは行わない
# NVIDIA Container Toolkit と nvidia-docker2 がホスト側で動いている前提

# システムパッケージの更新と基本ツールのインストール
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# uv のインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 作業ディレクトリを設定
WORKDIR /workspace

# venv の場所を固定
ENV VIRTUAL_ENV=/workspace/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 日本語ロケール（必要に応じて）
RUN apt-get update && apt-get install -y locales && \
    locale-gen ja_JP.UTF-8 && \
    update-locale LANG=ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8