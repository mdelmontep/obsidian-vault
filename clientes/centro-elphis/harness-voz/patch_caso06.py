# -*- coding: utf-8 -*-
"""9-sep-2026 · caso 06: Laura ignora una pregunta directa para seguir su guion.

Medido en LAS DOS corridas de la suite (jobs f8d8d6eb7edf y 00881d430b3a), identico:
  USER : "...llevo tres anos con problemas de cocaina. Que tipo de tratamientos ofrecen?"
  AGENT: "Entiendo que llevas tiempo con la cocaina. Que te ha hecho llamar hoy?"

No es el nombre (el primer veredicto del juez lo atribuia al nombre; el transcript dice otra
cosa, y el segundo veredicto lo describe bien). Es el punto 3 de `intake`, que ordena dedicar
UN turno a entender "antes de pedirle nada" y sugiere literalmente "que le ha hecho llamar
hoy". La regla que lo arreglaria ya existe -- pero al final del punto 4 y anclada al nombre.

Dos sustituciones en el nodo `intake`, ambas en su sitio:
  A) la excepcion, DENTRO del punto 3, donde se decide.
  B) la regla final, desanclada del nombre: vale para todo el guion.
"""
import json, os, sys, urllib.request

SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOW = "conversation_flow_a42bf76dcfa0"
AGENT = "agent_e21120298343bc2ef8b4a535c9"
KEY = os.environ["RETELL_KEY"]

A_OLD = """   encadenes ni las recites en orden.
"""
A_NEW = """   encadenes ni las recites en orden.
   EXCEPCION, y manda sobre todo este punto 3: si en ese mismo mensaje te ha hecho una pregunta
   que sabes contestar (que tratamientos hay, si la terapia es individual o grupal, cuanto dura,
   precio, donde estais), RESPONDELA PRIMERO y en corto. Responder YA ES dedicarle el turno: no
   hace falta ademas la pregunta abierta, y si la haces va DETRAS de la respuesta, nunca en su
   lugar. Dejar sin contestar una pregunta que sabes responder para seguir tu guion es el peor
   fallo que puedes cometer en esta llamada.
   Y no le preguntes algo que ya te ha contado: si acaba de decirte por que llama, preguntarle
   "que te ha hecho llamar hoy" es no haberle escuchado.
"""
B_OLD = "Y si mientras tanto te hace una pregunta, RESPONDELA: nunca ignores lo que te pregunta para insistir con el nombre."
B_NEW = ("Y esto vale en TODA la conversacion, no solo con el nombre: si te hace una pregunta, RESPONDELA. "
         "Nunca ignores lo que te pregunta para pasar a tu siguiente paso — ni el nombre, ni la pregunta "
         "abierta del punto 3, ni los datos de la cita.")

def api(method, path, body=None, params=""):
    req = urllib.request.Request(
        f"https://api.retellai.com/{path}{params}",
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method=method)
    with urllib.request.urlopen(req) as r:
        raw = r.read().decode()
        return r.status, (json.loads(raw) if raw.strip() else {})

# 1 · borrador desde la v45
st, ver = api("POST", f"create-agent-version/{AGENT}", {"base_version": 45})
av = ver["version"]; fv = ver["response_engine"]["version"]
print(f"borrador creado: agent v{av} · flow v{fv}  (HTTP {st})")

# 2 · leer ESE borrador, no un snapshot local
st, fl = api("GET", f"get-conversation-flow/{FLOW}", params=f"?version={fv}")
nodes = fl["nodes"]
intake = [n for n in nodes if n["id"] == "intake"][0]
t = intake["instruction"]["text"]
json.dump(fl, open(f"{SP}/fixes/flow-v{fv}-PRE-caso06.json", "w"), ensure_ascii=False, indent=1)

assert t.count(A_OLD) == 1, f"ancla A: {t.count(A_OLD)}"
assert t.count(B_OLD) == 1, f"ancla B: {t.count(B_OLD)}"
t2 = t.replace(A_OLD, A_NEW).replace(B_OLD, B_NEW)
assert A_NEW in t2 and B_NEW in t2
print(f"intake: {len(t)} -> {len(t2)} chars (+{len(t2)-len(t)})")
intake["instruction"]["text"] = t2

# 3 · PATCH solo nodes
st, _ = api("PATCH", f"update-conversation-flow/{FLOW}", {"nodes": nodes}, f"?version={fv}")
print(f"PATCH flow v{fv}: HTTP {st}")

# 4 · verificar server-side ANTES de publicar
st, chk = api("GET", f"get-conversation-flow/{FLOW}", params=f"?version={fv}")
ci = [n for n in chk["nodes"] if n["id"] == "intake"][0]["instruction"]["text"]
ok = (A_NEW in ci) and (B_NEW in ci) and (B_OLD not in ci)
print(f"verificacion server-side: {'OK' if ok else 'FALLO'} · nodos {len(chk['nodes'])} (v45 tenia 24)")
assert ok and len(chk["nodes"]) == 24
json.dump(chk, open(f"{SP}/fixes/flow-v{fv}-POST-caso06.json", "w"), ensure_ascii=False, indent=1)

# 5 · publicar (NO mueve el pin ni el numero: eso es una decision aparte)
st, _ = api("POST", f"publish-agent-version/{AGENT}", {"version": av})
print(f"publish agent v{av}: HTTP {st}")
print(f"\nPUBLICADA v{av}. El DDI sigue sirviendo la 45 y el pin sigue en 45.")
