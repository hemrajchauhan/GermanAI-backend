#!/bin/bash
set -e

# --- Edit these variables as needed, or pass as env/args ---
MODEL_ID="${MODEL_ID:-meta-llama/Llama-3.2-3B-Instruct}"   # E.g., "microsoft/Phi-3-mini-4k-instruct"
MODEL_FILENAME="${MODEL_FILENAME:-}"   # E.g., "pytorch_model.bin" or "" for whole repo
BLOB_HASH="${BLOB_HASH:-}"   # e.g. from HF page

# Optional: allow passing via CLI args for flexibility
if [ -n "$1" ]; then MODEL_ID="$1"; fi
if [ -n "$2" ]; then MODEL_FILENAME="$2"; fi
if [ -n "$3" ]; then BLOB_HASH="$3"; fi

MODEL_CACHE_DIR="$HOME/.cache/huggingface/hub/models--${MODEL_ID/\//--}"

# Check for filename in all snapshot dirs
FILE_PRESENT=""
if [ -n "$MODEL_FILENAME" ]; then
  FILE_PRESENT=$(find "$MODEL_CACHE_DIR/snapshots" -type f -name "$MODEL_FILENAME" 2>/dev/null | head -n 1)
fi

# Check for blob hash in blobs dir
BLOB_PRESENT=""
if [ -n "$BLOB_HASH" ]; then
  BLOB_PRESENT="$MODEL_CACHE_DIR/blobs/$BLOB_HASH"
fi

if { [ -n "$FILE_PRESENT" ] && [ -f "$FILE_PRESENT" ]; } || { [ -n "$BLOB_HASH" ] && [ -f "$BLOB_PRESENT" ]; }; then
  echo "Model file or blob already present (file: $FILE_PRESENT, blob: $BLOB_PRESENT), skipping download."
  exit 0
fi

if ! command -v huggingface-cli &> /dev/null; then
    echo "huggingface_hub not found, installing..."
    pip install huggingface_hub
fi

if [ -z "$HUGGINGFACE_HUB_TOKEN" ]; then
  echo "Error: Please set HUGGINGFACE_HUB_TOKEN environment variable."
  exit 1
fi

echo "Logging in to Hugging Face CLI..."
huggingface-cli login --token "$HUGGINGFACE_HUB_TOKEN"

echo "Downloading model $MODEL_ID ..."
if [ -n "$MODEL_FILENAME" ]; then
  huggingface-cli download "$MODEL_ID" --include "$MODEL_FILENAME"
else
  huggingface-cli download "$MODEL_ID"
fi

echo "Done."
