#!/usr/bin/env python3
"""Gate de inviolables: compara un flow candidato contra la v29 servida.
Falla ruidosamente. Un gate que no discrimina no es un gate: los casos que
DEBEN bloquear son los que valen, no los que pasan trivialmente."""
import json, os, sys, re, unicodedata

# La raiz se deriva del propio fichero: este arnes vive en el vault.
S = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(f"{S}/snapshots/flow-v29.json"))
CAND = json.load(open(sys.argv[1]))

def norm(s):
    # NFKD descompone el acento en base + marca combinante; hay que BORRAR la marca, no solo
    # descomponerla, o "estas" nunca casa con "estás". Se quitan tambien los signos ¿? ¡! y las
    # comillas, que el JSON escapa de formas distintas segun quien lo escribiera.
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[¿?¡!\"'\u201c\u201d]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def nodo(f, i):
    return next((n for n in f["nodes"] if n.get("id") == i), None)

fallos, checks = [], 0
def check(nombre, ok, detalle=""):
    global checks
    checks += 1
    if not ok: fallos.append(f"{nombre}: {detalle}")

# 1. Los nodos de crisis, INTACTOS byte a byte. Es el unico bloque con riesgo clinico.
for cid in ["crisis_frase", "crisis_confirmar", "crisis_recurso", "crisis_fallback", "crisis_transfer"]:
    a, b = nodo(BASE, cid), nodo(CAND, cid)
    check(f"crisis {cid} intacto",
          a is not None and b is not None and json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False),
          "ha cambiado")

# 2. El transfer de crisis apunta al Telefono de la Esperanza REAL.
ct = nodo(CAND, "crisis_transfer")
check("crisis -> 717 003 717", "717003717" in json.dumps(ct, ensure_ascii=False).replace(" ", ""), "destino distinto o ausente")

# 3. Motor: temperatura y modelo no se tocan (la temperatura evalua tambien las condiciones de arista).
check("temperatura 0.22", CAND.get("model_temperature") == 0.22, f"es {CAND.get('model_temperature')}")
check("modelo haiku 4.5", (CAND.get("model_choice") or {}).get("model") == (BASE.get("model_choice") or {}).get("model"), "modelo cambiado")

# 4. Art. 50: la presentacion como IA sigue en welcome.
w = norm(json.dumps(nodo(CAND, "welcome"), ensure_ascii=False))
check("art.50 asistente virtual", "asistente virtual" in w, "falta")
check("art.50 inteligencia artificial", "inteligencia artificial" in w, "falta (o abreviado a la sigla, que el TTS lee mal)")

# 5. El consentimiento sigue pidiendose en SU nodo, y solo ahi.
cons = norm(json.dumps(nodo(CAND, "consentimiento"), ensure_ascii=False))
# La formula RGPD, LITERAL. "contiene la palabra consentimiento" no discrimina: hay que
# comprobar la frase que de verdad se pronuncia, porque es lo que ampara el registro de datos.
FORMULA = "para poder registrar tus datos y gestionar la cita, me confirmas que estas de acuerdo"
check("formula RGPD literal e intacta", FORMULA in norm(json.dumps(nodo(CAND, "consentimiento"), ensure_ascii=False)),
      "la frase de consentimiento ha cambiado o desaparecido")
check("consentimiento sigue siendo obligatorio", "di exactamente esta frase" in cons,
      "se ha relajado el caracter literal de la formula")
gp = norm(CAND.get("global_prompt") or "")
check("consentimiento NO duplicado en global", "me confirmas que estas de acuerdo" not in gp,
      "la formula ha vuelto al global_prompt: se pedira dos veces")

# 6. Topologia: mismos nodos, ni uno mas ni uno menos.
check("mismos nodos", sorted(n["id"] for n in BASE["nodes"]) == sorted(n["id"] for n in CAND["nodes"]),
      "el conjunto de nodos ha cambiado")

# 7. Las tres aristas de despedida siguen vivas y siguen siendo LAS ULTIMAS de su nodo
#    (el orden es prioridad: por delante se comerian las de crisis).
for nid, eid in [("welcome", "e_bienv_fin"), ("intake", "e_intake_fin"), ("info_cita", "e_info_fin")]:
    n = nodo(CAND, nid) or {}
    eds = n.get("edges") or []
    ids = [e.get("id") for e in eds]
    check(f"arista {eid} existe", eid in ids, "ha desaparecido")
    check(f"arista {eid} va la ULTIMA", ids and ids[-1] == eid, f"orden actual {ids}")

# 8. Precios y domicilio, ANCLADOS AL NODO QUE LOS DICE.
#    Comprobar que la cifra existe "en algun sitio del flow" no discrimina: una mutacion que
#    cambiaba 1.772 -> 1.900 en info_cita pasaba el gate porque la cifra vivia tambien en otro
#    nodo. Se compara el multiconjunto de cifras nodo a nodo.
def cifras(n):
    return sorted(re.findall(r"\b\d{1,2}[.,]\d{3}\b|\b\d{3,4}\b", json.dumps(n, ensure_ascii=False)))
for b in BASE["nodes"]:
    c = nodo(CAND, b["id"])
    if c is None: continue
    cb = cifras(b)
    if not cb: continue
    check(f"cifras intactas en {b['id']}", cifras(c) == cb, f"{cb} -> {cifras(c)}")
# 8b. Los precios REALES viven en el global_prompt, no en info_cita: sin este check, alterar
#     una tarifa pasaba el gate entero (medido por mutacion; el caso de info_cita era un
#     mutante equivalente, no una victima).
check("cifras intactas en global_prompt", cifras(CAND.get("global_prompt") or "") == cifras(BASE.get("global_prompt") or ""),
      f"{cifras(BASE.get('global_prompt') or '')} -> {cifras(CAND.get('global_prompt') or '')}")
check("domicilio O'Donnell", "O'Donnell" in json.dumps(nodo(CAND, "info_cita") or {}, ensure_ascii=False)
      or "O'Donnell" in json.dumps(CAND, ensure_ascii=False), "ha desaparecido")

print(f"gate: {checks} comprobaciones, {len(fallos)} fallo(s)")
for f in fallos: print("  FALLA -", f)
sys.exit(1 if fallos else 0)
