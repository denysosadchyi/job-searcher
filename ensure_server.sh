#!/bin/bash
# Ensure the Flask vacancy server is running
# Called by cron daily at 2:53

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
[ -f "$SCRIPT_DIR/.env" ] && export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
LOG="$SCRIPT_DIR/app.log"

# Read port from config.py, default 8080
PORT=$(python3 -c "
try:
    from config import WEB_PORT; print(WEB_PORT)
except:
    print(8080)
" 2>/dev/null)

# Check if server actually responds, not just if process exists
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:$PORT/ 2>/dev/null)

if [ "$HTTP_CODE" = "200" ]; then
    echo "[$(date)] Server is responding (HTTP $HTTP_CODE), OK" >> "$LOG"
else
    echo "[$(date)] Server not responding (HTTP $HTTP_CODE), restarting..." >> "$LOG"
    # Kill any zombie processes holding the port
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 1
    nohup python3 app.py >> "$LOG" 2>&1 &
    sleep 2
    # Verify restart
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:$PORT/ 2>/dev/null)
    echo "[$(date)] Restart result: HTTP $HTTP_CODE" >> "$LOG"
fi
