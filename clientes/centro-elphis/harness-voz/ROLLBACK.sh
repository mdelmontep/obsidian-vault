#!/usr/bin/env bash
# Devuelve el agente de voz de Centro Elphis a una version anterior.
#
# 13-sep-2026 — REESCRITO. La version anterior decia "el numero +34910054950 NO fija
# agent_version: sirve latest_published, asi que republicar una version vieja es rollback
# completo". Eso es FALSO y lo era ya cuando se escribio: el DDI lleva
# inbound_agents[{agent_version: <entero>}], comprobado hoy con get-phone-number. Republicar
# una version vieja no mueve el DDI ni un milimetro, y el script verificaba la version
# PUBLICADA — que si cambiaba — asi que imprimia "OK: sirviendo v21" con produccion intacta.
# Un rollback que reporta exito sin hacer nada es peor que no tener rollback.
#
# El rollback de verdad es BAJAR EL PIN del trinquete en Postgres. guard-retell-pin (T1, cada
# 5 min) repone el DDI al valor del pin; el PATCH del DDI de aqui solo evita esperar esos
# minutos. Si se hace al reves (mover el DDI sin tocar el pin) el guard lo revierte y el
# equipo recibe un rojo en Slack.
#
#   ./ROLLBACK.sh 46     -> vuelve a la v46
set -euo pipefail
R=$(cat ~/Projects/elphis-psicologia/infra/tests/.token-retell)
A=agent_e21120298343bc2ef8b4a535c9
DDI="+34910054950"
PGC="elphis-n8nwithpostgres-wtqddl-postgres-aux-1"
V=${1:?uso: ./ROLLBACK.sh <version>}

# 1. La version tiene que existir Y estar publicada: fijar el DDI a una version sin publicar
#    deja el numero sin agente que atienda.
pub=$(curl -sf "https://api.retellai.com/get-agent-versions/$A" -H "Authorization: Bearer $R" \
  | python3 -c "import sys,json;print('si' if any(x['version']==$V and x.get('is_published') for x in json.load(sys.stdin)) else 'no')")
[ "$pub" = "si" ] || { echo "ABORTA: la v$V no esta publicada en Retell" >&2; exit 1; }

# 2. El pin PRIMERO. Sin esto no hay rollback.
ssh elphis "docker exec $PGC psql -U elphis_app -d elphis_app -c \
  \"UPDATE idempotency_log SET response = jsonb_set(response,'{pin}','$V'::jsonb), created_at = NOW() \
    WHERE key = 'guard-retell-pin:config'\"" > /dev/null
pin=$(ssh elphis "docker exec $PGC psql -U elphis_app -d elphis_app -tAc \
  \"SELECT response->>'pin' FROM idempotency_log WHERE key='guard-retell-pin:config'\"" | tr -d '[:space:]')
[ "$pin" = "$V" ] || { echo "ABORTA: el pin quedo en '$pin', se pedia $V" >&2; exit 1; }

# 3. El DDI despues, solo para no esperar a T1.
curl -sf -X PATCH "https://api.retellai.com/update-phone-number/$DDI" \
  -H "Authorization: Bearer $R" -H "Content-Type: application/json" \
  -d "{\"inbound_agents\":[{\"agent_id\":\"$A\",\"agent_version\":$V,\"weight\":1}]}" > /dev/null
sleep 2

# 4. Verificar lo que SIRVE, no lo que esta publicado. Esta es la comprobacion que faltaba.
srv=$(curl -sf "https://api.retellai.com/get-phone-number/$DDI" -H "Authorization: Bearer $R" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print((d.get('inbound_agents') or [{}])[0].get('agent_version'))")
[ "$srv" = "$V" ] || { echo "ROLLBACK FALLIDO: el DDI sirve v$srv, se pedia v$V (pin=$pin)" >&2; exit 1; }
echo "OK: el DDI $DDI sirve v$V y el pin esta en $V"
