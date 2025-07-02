#!/bin/bash
set -e

MODEL_DIR="/root/.cache/huggingface/hub/models--google--gemma-3-4b-it-qat-q4_0-gguf/blobs"
MODEL_PATH="$MODEL_DIR/76aed0a8285b83102f18b5d60e53c70d09eb4e9917a20ce8956bd546452b56e2"

if [ -f "$MODEL_PATH" ]; then
  echo "Model already present at $MODEL_PATH, skipping download."
  exit 0
fi

pip install huggingface_hub
huggingface-cli login --token $HUGGINGFACE_HUB_TOKEN
huggingface-cli download google/gemma-3-4b-it-qat-q4_0-gguf
