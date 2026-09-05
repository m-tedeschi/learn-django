#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/.django.pid"
LOG_FILE="$ROOT_DIR/.django.log"
VITE_PID_FILE="$ROOT_DIR/.vite.pid"
VITE_LOG_FILE="$ROOT_DIR/.vite.log"
PYTHON="$ROOT_DIR/.venv/bin/python"
FRONTEND_DIR="$ROOT_DIR/frontend"

usage() {
  echo "Usage: ./server.sh {start|stop}"
}

start() {
  cd "$ROOT_DIR"

  if [[ ! -x "$PYTHON" ]]; then
    echo "Missing virtual environment. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
  fi

  docker compose up -d db
  "$PYTHON" manage.py migrate

  start_django
  start_vite
}

start_django() {
  if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Django is already running at http://127.0.0.1:8000/"
    return
  fi

  nohup "$PYTHON" manage.py runserver 127.0.0.1:8000 --noreload >"$LOG_FILE" 2>&1 &
  echo "$!" > "$PID_FILE"

  sleep 1
  if ! kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Django failed to start. Logs:"
    cat "$LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
  fi

  echo "Django started at http://127.0.0.1:8000/"
  echo "Logs: $LOG_FILE"
}

start_vite() {
  if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    echo "Missing frontend dependencies. Run: cd frontend && npm install"
    exit 1
  fi

  if [[ -f "$VITE_PID_FILE" ]] && kill -0 "$(cat "$VITE_PID_FILE")" 2>/dev/null; then
    echo "Vite is already running at http://127.0.0.1:5173/"
    return
  fi

  cd "$FRONTEND_DIR"
  nohup "$FRONTEND_DIR/node_modules/.bin/vite" --host 127.0.0.1 >"$VITE_LOG_FILE" 2>&1 &
  echo "$!" > "$VITE_PID_FILE"

  sleep 1
  if ! kill -0 "$(cat "$VITE_PID_FILE")" 2>/dev/null; then
    echo "Vite failed to start. Logs:"
    cat "$VITE_LOG_FILE"
    rm -f "$VITE_PID_FILE"
    exit 1
  fi

  echo "Vite started at http://127.0.0.1:5173/"
  echo "Logs: $VITE_LOG_FILE"
}

stop_process() {
  local name="$1"
  local pid_file="$2"

  if [[ -f "$pid_file" ]]; then
    pid="$(cat "$pid_file")"
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid"
      echo "Stopped $name."
    else
      echo "$name PID file existed, but the process was not running."
    fi
    rm -f "$pid_file"
  else
    echo "No $name PID file found."
  fi
}

stop() {
  cd "$ROOT_DIR"
  stop_process "Vite" "$VITE_PID_FILE"
  stop_process "Django" "$PID_FILE"

  docker compose down
}

case "${1:-}" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    usage
    exit 1
    ;;
esac
