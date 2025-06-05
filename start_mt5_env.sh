#!/bin/bash

# Set Wine prefix
export WINEPREFIX="$HOME/.wine64"

# Path to wine64
WINE64="/usr/local/bin/wine"

# Optional: change to your MetaTrader installation path inside Wine
MT5_PATH="C:\\Program Files\\MetaTrader 5\\terminal64.exe"

# Launch MetaTrader 5
echo "Starting MetaTrader 5..."
"$WINE64" "$MT5_PATH" &

# Wait a bit for MT5 to fully load
sleep 5

# Open Wine command prompt for running your Python scripts
echo "Opening Wine command prompt (cmd.exe)..."
"$WINE64" cmd
