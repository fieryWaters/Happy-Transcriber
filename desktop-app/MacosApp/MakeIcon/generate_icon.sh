#!/bin/bash

# Script to automate the icon generation process

# Check if an argument (image path) is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path_to_image.png"
    exit 1
fi

IMAGE_PATH="$1"
BASENAME=$(basename "$IMAGE_PATH" .png)

# Create a directory for the iconset if it doesn't exist
mkdir -p ${BASENAME}.iconset

python3 round_corners.py "$IMAGE_PATH" "$IMAGE_PATH"

# Generate the different sizes
sips -Z 16x16   "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_16x16.png
sips -Z 32x32   "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_32x32.png
sips -Z 64x64   "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_32x32@2x.png
sips -Z 128x128 "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_128x128.png
sips -Z 256x256 "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_128x128@2x.png
sips -Z 512x512 "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_512x512.png
sips -Z 1024x1024 "$IMAGE_PATH" --out ${BASENAME}.iconset/icon_512x512@2x.png

# Generate the .icns file
iconutil -c icns ${BASENAME}.iconset

echo "Icon generation completed."

