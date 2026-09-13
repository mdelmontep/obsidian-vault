"""Hace identificable el aviso de cancelacion sin deal anotable.

Hoy el aviso a Slack dice `sin anotar: sin_deals_abiertos` y NO dice de quien: el 11-sep se
cancelo la cita de Laura Caro Nieto (18/9/2026 11:00) y nadie pudo saber quien era. Anade el
asunto del correo de Doctoralia al mensaje y lo redacta como accion pendiente.

No toca el filtro `.filter(d => st !== 3 && st !== 4)` de `Cancel: elegir deals`: excluir deals
Won/Lost es decision explicita de Manu del 03-09-2026 y es correcta en el caso general.

Uso: python3 fix_aviso_cancel.py          (hace backup, aplica, verifica)
"""
import json, os, urllib.request, urllib.error, subprocess, datetime

WF = "dxuxgroTneI6QMo1"
NODO = "Avisar correo descartado"
BASE = "https://n8n-elphis.agentesia.madrid/api/v1"
KEY = subprocess.check_output(
    ["opsa", "read", "op://Elphis/giidbepoapvkfliidqdcaoxf6y/credencial"]).decode().strip()

def api(m, p, b=None):
    r = urllib.request.Request(BASE + p, method=m,
        headers={"X-N8N-API-KEY": KEY, "Content-Type": "application/json"},
        data=json.dumps(b).encode() if b is not None else None)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:600]); raise

VIEJO = "  const extra = n > 0 ? (' · ' + n + ' deal(s) anotados') : (' · sin anotar: ' + (s._cancel_motivo || 'desconocido'));"
NUEVO = ("  const asunto = String((s.raw && s.raw.subject) || '').replace(/\\s+/g, ' ').replace(/:/g, '.').trim();\n"
         "  const extra = n > 0 ? (' · ' + n + ' deal(s) anotados')\n"
         "    : (' · SIN ANOTAR, hay que hacerlo a mano en el CRM (' + (s._cancel_motivo || 'desconocido') + ') · ' + (asunto || gid));")

wf = api("GET", f"/workflows/{WF}")
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
bak = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"n8n-PRE-{WF}-{ts}.json")
open(bak, "w").write(json.dumps(wf, ensure_ascii=False, indent=1))
print("backup:", bak)

objetivo = [n for n in wf["nodes"] if n["name"] == NODO]
assert len(objetivo) == 1, f"nodos llamados {NODO!r}: {len(objetivo)}"
cod = objetivo[0]["parameters"]["jsCode"]
assert cod.count(VIEJO) == 1, f"ancla no unica: {cod.count(VIEJO)} ocurrencias"
objetivo[0]["parameters"]["jsCode"] = cod.replace(VIEJO, NUEVO)

n_pre, c_pre = len(wf["nodes"]), len(wf["connections"])
act_pre, ew_pre = wf.get("active"), (wf.get("settings") or {}).get("errorWorkflow")

cuerpo = {"name": wf["name"], "nodes": wf["nodes"], "connections": wf["connections"],
          "settings": wf.get("settings") or {}}
api("PUT", f"/workflows/{WF}", cuerpo)

post = api("GET", f"/workflows/{WF}")
assert len(post["nodes"]) == n_pre, "cambio el numero de nodos"
assert len(post["connections"]) == c_pre, "cambiaron las conexiones"
assert post.get("active") == act_pre, f"active cambio: {act_pre} -> {post.get('active')}"
assert (post.get("settings") or {}).get("errorWorkflow") == ew_pre, "se perdio errorWorkflow"
nuevo_cod = [n for n in post["nodes"] if n["name"] == NODO][0]["parameters"]["jsCode"]
assert NUEVO in nuevo_cod and VIEJO not in nuevo_cod, "el cambio no esta en el servidor"
print("OK: aplicado y verificado contra el servidor.")
print(f"   nodos={len(post['nodes'])} conexiones={len(post['connections'])} active={post.get('active')}")
