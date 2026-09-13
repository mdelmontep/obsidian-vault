# v48: tres instrucciones nombran nodos que NO son salida de su nodo.
# Ordenar al LLM "transiciona a X" cuando X no esta entre sus aristas es una orden imposible:
# o la ignora (y entonces sobra) o intenta cumplirla por la arista mas parecida.
# Solo se cambia TEXTO. Cero aristas nuevas, cero aristas borradas, global_prompt intacto.
import json, os, sys
S = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(f"{S}/flow_sinA2.json", encoding="utf-8"))
N = {n["id"]: n for n in f["nodes"]}

def salidas(i):
    n = N[i]; out = []
    for e in (n.get("edges") or []): out.append(e["destination_node_id"])
    for k in ("else_edge", "skip_response_edge", "edge"):
        if n.get(k): out.append(n[k]["destination_node_id"])
    return out

CAMBIOS = [
    # nodo, ancla, sustituto, destinos que el sustituto debe nombrar
    ("cierre_cita",
     "confirmar la cita. Con tus palabras. -> transiciona a cierre.",
     "confirmar la cita. Con tus palabras. Despues ofrecele resolver cualquier otra duda.\n"
     "Si no necesita nada mas, despidete SIEMPRE en voz alta antes de terminar, nunca en silencio:\n"
     'FRASE (no la cambies): "Perfecto. Gracias por llamar a Centro Elphis, cuidate."',
     []),
    ("info_cita",
     "Si acepta reservar → transiciona a fn_reservar.\n"
     "Si solo quiere dejar datos para que le llamen → transiciona a fn_crear_lead.\n"
     "Si no quiere nada más → transiciona a fn_crear_lead.",
     "Si acepta reservar → transiciona a consentimiento.\n"
     "Si solo quiere dejar datos para que le llamen → transiciona a extract_lead.\n"
     "Si no quiere nada más → transiciona a extract_lead.",
     ["consentimiento", "extract_lead"]),
    ("recepcion_aviso",
     "una frase, ofrécele info@centroelphis.com si insiste, y pasa a la despedida. Ver la sección",
     "una frase, ofrécele info@centroelphis.com si insiste, y transiciona a fuera_alcance. Ver la sección",
     ["fuera_alcance"]),
]

for nodo, viejo, nuevo, dests in CAMBIOS:
    t = N[nodo]["instruction"]["text"]
    assert t.count(viejo) == 1, f"{nodo}: el ancla aparece {t.count(viejo)} veces, no 1"
    for d in dests:
        assert d in salidas(nodo), f"{nodo}: el texto nuevo nombra {d}, que no es salida suya ({salidas(nodo)})"
    N[nodo]["instruction"]["text"] = t.replace(viejo, nuevo)
    print(f"ok {nodo}: -{len(viejo)} +{len(nuevo)} car.")

base = json.load(open(f"{S}/flow_sinA2.json", encoding="utf-8"))
assert json.dumps(base.get("global_prompt")) == json.dumps(f.get("global_prompt")), "global_prompt tocado"
def ar(g):
    s = set()
    for n in g["nodes"]:
        es = list(n.get("edges") or [])
        for k in ("else_edge", "skip_response_edge", "edge"):
            if n.get(k): es.append(n[k])
        for e in es: s.add(f"{n['id']}>{e['destination_node_id']}")
    return s
assert ar(base) == ar(f), "el grafo cambio"
assert json.dumps(base.get("tools"), sort_keys=True) == json.dumps(f.get("tools"), sort_keys=True), "tools tocadas"
dif = [n["id"] for n in f["nodes"] if json.dumps(n, sort_keys=True) != json.dumps({x["id"]: x for x in base["nodes"]}[n["id"]], sort_keys=True)]
assert sorted(dif) == sorted(c[0] for c in CAMBIOS), f"nodos tocados inesperados: {dif}"
json.dump(f, open(f"{S}/flow_v49_local.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito flow_v49_local.json | nodos tocados:", sorted(dif))
