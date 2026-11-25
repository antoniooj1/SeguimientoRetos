#!/bin/zsh
# Arranca el MySQL local del proyecto (puerto 3307) si no está corriendo.
cd "${0:A:h}/.."
if lsof -nP -iTCP:3307 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "MySQL ya está corriendo en el puerto 3307."
  exit 0
fi
D="$PWD/.local/mysql"
exec /opt/homebrew/opt/mysql@8.4/bin/mysqld \
  --datadir="$D/data" --port=3307 --bind-address=127.0.0.1 \
  --socket="$D/mysql.sock" --pid-file="$D/mysql.pid" --log-error="$D/mysql.log"
