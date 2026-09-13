"""Pone el flow de TEST en un estado concreto a partir de un BORRADOR LOCAL.

Reescrito el 7-sep-2026 (F4.9 del RUNBOOK). Lo que cambia respecto a la version de agosto:
- Ya no hay `crisis_transfer`: la decision cerrada es CERO transferencias. El aserto
  `"600000000" in crisis_transfer` no puede seguir siendo el guardarrail, porque el nodo
  no existe. Lo sustituye `not any(type=="transfer_call")`, que es lo que de verdad
  impide que una suite de crisis marque un telefono real.
- Ya no aplica `patches.py` sobre un snapshot: la fuente es el borrador compuesto
  (`flow_new_body.json`), que es lo que se va a desplegar. Probar otra cosa no prueba nada.
- Empuja tambien `tools`, `start_node_id` y `default_dynamic_variables`: el borrador cambia
  el nodo de inicio (`calc_hora`) y anade tres tools. Un TEST sin ellas no es el mismo grafo.

Uso:
    python3 tf.py <borrador.json>            # tools TAL CUAL (para batch con tool_mocks)
    python3 tf.py <borrador.json> --neutro   # tools con URL muerta (para pruebas de CHAT,
                                             # donde tool_mocks NO existe y crear_lead
                                             # pegaria a produccion y crearia un lead real)
"""
import json, os, sys, copy, urllib.request, urllib.error

S = os.path.dirname(os.path.abspath(__file__))
TOK = open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()
TF = "conversation_flow_b857e417f7f8"
URL_MUERTA = "https://n8n-elphis.agentesia.madrid/webhook/zz-tf-noop-no-existe"

def api(m, p, b=None):
    r = urllib.request.Request("https://api.retellai.com" + p, method=m,
        headers={"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"},
        data=json.dumps(b).encode() if b is not None else None)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:600]); raise

borrador = sys.argv[1]
neutro = "--neutro" in sys.argv[2:]
g = json.load(open(borrador, encoding="utf-8"))

# Guardarrail de entrada. Hasta el 12-sep-2026 era `assert not any(transfer_call)`, heredado del
# diseno F4 (cero transferencias), que NO esta desplegado: produccion transfiere en crisis al
# 717 003 717 desde el 19-may. Con ese assert, el unico flow que de verdad atiende llamadas no se
# podia probar — y un arnes que solo admite el diseno que no existe no mide nada. Lo que hay que
# impedir no es el nodo, es que una suite marque un telefono real: se neutraliza el destino a
# +34600000000 (la politica de agosto) y se verifica DESPUES contra el servidor.
TEL_NEUTRO = "+34600000000"
neutralizados = []
for n in g["nodes"]:
    if n.get("type") == "transfer_call":
        d = n.get("transfer_destination") or {}
        if d.get("number") != TEL_NEUTRO:
            neutralizados.append((n["id"], d.get("number")))
            d["number"] = TEL_NEUTRO
            n["transfer_destination"] = d

cuerpo = {
    "global_prompt": g["global_prompt"],
    "nodes": g["nodes"],
    "tools": copy.deepcopy(g["tools"]),
    "start_node_id": g["start_node_id"],
    "default_dynamic_variables": g.get("default_dynamic_variables"),
}
if neutro:
    for t in cuerpo["tools"]:
        t["url"] = URL_MUERTA

api("PATCH", f"/update-conversation-flow/{TF}", cuerpo)
srv = api("GET", f"/get-conversation-flow/{TF}")

# Verificacion CONTRA EL SERVIDOR (no contra lo que creemos haber mandado).
malos = [(n["id"], (n.get("transfer_destination") or {}).get("number")) for n in srv["nodes"]
         if n.get("type") == "transfer_call"
         and (n.get("transfer_destination") or {}).get("number") != TEL_NEUTRO]
assert not malos, f"el flow de TEST marcaria un telefono real: {malos}"
assert srv["global_prompt"] == g["global_prompt"], "el servidor no aplico el global_prompt"
# Hasta el 12-sep aqui solo se comparaba la LISTA DE IDS: un PATCH que cambiara el texto de un
# nodo, una condicion de arista o una variable pasaba la verificacion sin que nadie lo viera, y lo
# que se media no era lo que se creia estar midiendo. Se compara el contenido, restando el
# `skippable:false` que la API escribe sola en todos los nodos en cada PATCH, y el telefono
# neutralizado, que es la unica diferencia declarada.
def _sin_ruido(n):
    n = {k: v for k, v in n.items() if not (k == "skippable" and v is False)}
    if n.get("type") == "transfer_call": n.pop("transfer_destination", None)
    return n
_a = {n["id"]: _sin_ruido(n) for n in g["nodes"]}
_b = {n["id"]: _sin_ruido(n) for n in srv["nodes"]}
assert set(_a) == set(_b), f"el servidor no aplico los nodos: {sorted(set(_a) ^ set(_b))}"
_dif = [i for i in _a if json.dumps(_a[i], sort_keys=True, ensure_ascii=False) != json.dumps(_b[i], sort_keys=True, ensure_ascii=False)]
assert not _dif, f"el servidor guardo otra cosa en estos nodos: {_dif}"
assert srv.get("default_dynamic_variables") == g.get("default_dynamic_variables"), "default_dynamic_variables no coincide"
assert srv["start_node_id"] == g["start_node_id"], "el servidor no aplico start_node_id"
assert sorted(t["name"] for t in srv["tools"]) == sorted(t["name"] for t in g["tools"]), "tools distintas"
if neutro:
    assert all(t["url"] == URL_MUERTA for t in srv["tools"]), "alguna tool sigue apuntando a produccion"

print(f"  flow de TEST cargado desde {os.path.basename(borrador)} | v{srv['version']} | "
      f"{len(srv['nodes'])} nodos, {len(srv['tools'])} tools | transfer neutralizado: {neutralizados or 'no habia'} | "
      f"urls={'MUERTAS' if neutro else 'reales (exige tool_mocks)'}")
