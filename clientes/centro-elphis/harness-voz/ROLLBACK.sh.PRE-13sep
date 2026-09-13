#!/usr/bin/env bash
# Devuelve el agente de voz de Centro Elphis a una version anterior.
# Funciona porque el numero +34910054950 NO fija agent_version: sirve latest_published,
# asi que republicar una version vieja es rollback completo y sin corte.
#   ./ROLLBACK.sh        -> vuelve a la v29 (la que servia antes de esta tanda)
#   ./ROLLBACK.sh 21     -> vuelve a la v21
set -euo pipefail
R=$(cat ~/Projects/elphis-psicologia/infra/tests/.token-retell)
A=agent_e21120298343bc2ef8b4a535c9
V=${1:-29}
curl -sf -X POST "https://api.retellai.com/publish-agent/$A?version=$V" \
  -H "Authorization: Bearer $R" -H "Content-Type: application/json" -d '{}' > /dev/null
sleep 2
# Verificacion: get-agent SIN ?version devuelve el BORRADOR, no lo servido.
# Lo servido es la MAYOR con is_published=true.
srv=$(curl -sf "https://api.retellai.com/get-agent-versions/$A" -H "Authorization: Bearer $R" \
  | python3 -c "import sys,json;print(max(x['version'] for x in json.load(sys.stdin) if x.get('is_published')))")
if [ "$srv" != "$V" ]; then
  echo "ROLLBACK FALLIDO: sirviendo v$srv, se pedia v$V" >&2; exit 1
fi
echo "OK: sirviendo v$V"
