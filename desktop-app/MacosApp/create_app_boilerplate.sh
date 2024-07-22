#!/bin/bash

# Check if app name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 AppName"
    exit 1
fi

APP_NAME="$1"
APP_DIR="${APP_NAME}.app"
CONTENT_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENT_DIR}/MacOS"
RESOURCES_DIR="${CONTENT_DIR}/Resources"
FRAMEWORKS_DIR="${CONTENT_DIR}/Frameworks"

# Create directory structure
mkdir -p "${MACOS_DIR}" "${RESOURCES_DIR}" "${FRAMEWORKS_DIR}"

# Create a simple executable as a placeholder
echo '#!/bin/bash' > "${MACOS_DIR}/${APP_NAME}"
echo 'echo "Hello, world!"' >> "${MACOS_DIR}/${APP_NAME}"
chmod +x "${MACOS_DIR}/${APP_NAME}"

# Generate a basic Info.plist file
cat <<EOL > "${CONTENT_DIR}/Info.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleExecutable</key>
    <string>${APP_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.${APP_NAME}</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
</dict>
</plist>
EOL

echo "${APP_NAME}.app boilerplate created!"

