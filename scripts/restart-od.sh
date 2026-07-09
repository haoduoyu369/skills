#!/usr/bin/env bash
# 重启 open-design 的 daemon + web 服务
#
# 用法：
#   bash scripts/restart-od.sh            # 后台启动，脚本退出后服务继续跑
#   bash scripts/restart-od.sh --fg       # 前台启动，Ctrl+C 停全部
#
# 启动后：
#   daemon → http://127.0.0.1:7456
#   web    → http://localhost:3000（预分配，不会自动递增）
#
# 日志：
#   /tmp/od-daemon.log
#   /tmp/od-web.log

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OD_ROOT="$(cd "$SCRIPT_DIR/../open-design" && pwd)"
DAEMON_PORT="${OD_PORT:-7456}"
WEB_PORT="${OD_WEB_PORT:-3000}"
API_TOKEN="${OD_API_TOKEN:-dev-test-token}"
FOREGROUND=false
[[ "${1:-}" == "--fg" ]] && FOREGROUND=true

DAEMON_LOG="/tmp/od-daemon.log"
WEB_LOG="/tmp/od-web.log"

echo "=== open-design 重启脚本 ==="
echo "OD_ROOT:  $OD_ROOT"
echo "DAEMON:   http://127.0.0.1:$DAEMON_PORT"
echo "WEB:      http://localhost:$WEB_PORT"
echo "LOGS:     $DAEMON_LOG / $WEB_LOG"
echo ""

# ── 1. 关闭已有服务 ──────────────────────────────────────
echo "[1/4] 关闭已有服务..."

# daemon（通过端口找进程）
OLD_DAEMON=$(lsof -ti :"$DAEMON_PORT" 2>/dev/null || true)
if [ -n "$OLD_DAEMON" ]; then
  echo "$OLD_DAEMON" | xargs kill 2>/dev/null || true
  echo "  已关闭旧 daemon (PID: $OLD_DAEMON)"
fi

# web（通过端口找进程，确保释放 WEB_PORT）
OLD_WEB_PORT=$(lsof -ti :"$WEB_PORT" 2>/dev/null || true)
if [ -n "$OLD_WEB_PORT" ]; then
  echo "$OLD_WEB_PORT" | xargs kill 2>/dev/null || true
  echo "  已关闭占用端口 $WEB_PORT 的进程 (PID: $OLD_WEB_PORT)"
fi

# 也通过 pgrep 查找 next dev 进程（可能在不同端口上）
OLD_WEB=$(pgrep -f "next dev.*$OD_ROOT/apps/web" 2>/dev/null || true)
if [ -n "$OLD_WEB" ]; then
  echo "$OLD_WEB" | xargs kill 2>/dev/null || true
  echo "  已关闭旧 web (PID: $OLD_WEB)"
fi

# 也杀掉上一轮脚本启动的 daemon node 进程
OLD_NODE=$(pgrep -f "node dist/cli.js --no-open" 2>/dev/null || true)
if [ -n "$OLD_NODE" ]; then
  echo "$OLD_NODE" | xargs kill 2>/dev/null || true
fi

sleep 2

# ── 2. 构建 daemon ────────────────────────────────────────
echo "[2/4] 构建 daemon..."
cd "$OD_ROOT/apps/daemon"
if pnpm run build > "$DAEMON_LOG" 2>&1; then
  echo "  构建成功 ✓"
else
  echo "  ✗ 构建失败，查看 $DAEMON_LOG"
  tail -5 "$DAEMON_LOG"
  exit 1
fi

# ── 3. 启动 daemon ────────────────────────────────────────
echo "[3/4] 启动 daemon..."
cd "$OD_ROOT/apps/daemon"

# 清空旧日志
: > "$DAEMON_LOG"

# OD_WEB_PORT 告知 daemon CORS 中间件允许 web 端口的 Origin
if [ "$FOREGROUND" = true ]; then
  OD_API_TOKEN="$API_TOKEN" OD_WEB_PORT="$WEB_PORT" node dist/cli.js --no-open 2>&1 | tee -a "$DAEMON_LOG" &
else
  OD_API_TOKEN="$API_TOKEN" OD_WEB_PORT="$WEB_PORT" node dist/cli.js --no-open >> "$DAEMON_LOG" 2>&1 &
fi
DAEMON_PID=$!
disown "$DAEMON_PID" 2>/dev/null || true

# 等待 daemon 就绪
printf "  等待 daemon 就绪"
DAEMON_OK=false
for i in $(seq 1 15); do
  if curl -sf "http://127.0.0.1:$DAEMON_PORT/api/health" >/dev/null 2>&1; then
    DAEMON_OK=true
    break
  fi
  printf "."
  sleep 1
done

if [ "$DAEMON_OK" = true ]; then
  echo " ✓"
else
  echo " ✗ 超时"
  echo "  最后 5 行日志："
  tail -5 "$DAEMON_LOG" 2>/dev/null
  exit 1
fi

# ── 4. 启动 web ───────────────────────────────────────────
echo "[4/4] 启动 web dev server..."
cd "$OD_ROOT/apps/web"

# 清空旧日志
: > "$WEB_LOG"

# 使用 -p 指定端口，Next.js 不会自动递增
if [ "$FOREGROUND" = true ]; then
  OD_API_TOKEN="$API_TOKEN" PORT="$WEB_PORT" pnpm run dev 2>&1 | tee -a "$WEB_LOG" &
else
  OD_API_TOKEN="$API_TOKEN" PORT="$WEB_PORT" pnpm run dev >> "$WEB_LOG" 2>&1 &
fi
WEB_PID=$!
disown "$WEB_PID" 2>/dev/null || true

# 等待 web 就绪
printf "  等待 web 就绪"
WEB_READY=false
for i in $(seq 1 30); do
  if curl -sf -o /dev/null "http://localhost:$WEB_PORT/" 2>/dev/null; then
    WEB_READY=true
    break
  fi
  printf "."
  sleep 1
done

if [ "$WEB_READY" = true ]; then
  echo " ✓"
else
  echo " ✗ 超时"
  echo "  最后 5 行日志："
  tail -5 "$WEB_LOG" 2>/dev/null
  exit 1
fi

# ── 完成 ──────────────────────────────────────────────────
echo ""
echo "=== 启动完成 ==="
echo "  daemon: http://127.0.0.1:$DAEMON_PORT"
echo "  web:    http://localhost:$WEB_PORT"
echo ""

if [ "$FOREGROUND" = true ]; then
  echo "前台模式运行中，按 Ctrl+C 停止所有服务。"
  trap 'echo ""; echo "正在关闭..."; kill $DAEMON_PID $WEB_PID 2>/dev/null; exit 0' INT TERM
  wait
else
  echo "后台模式，服务已脱离终端。要停止服务："
  echo "  bash scripts/restart-od.sh   # 再次运行会先关闭旧服务"
  echo "  或手动 kill PID: daemon=$DAEMON_PID web=$WEB_PID"
fi
