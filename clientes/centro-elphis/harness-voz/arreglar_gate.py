# -*- coding: utf-8 -*-
"""9-sep-2026 · gate.py volvia a no discriminar, por la razon contraria a la del 7-sep.

El 7-sep se reescribio para que dejara de BLOQUEAR el diseno de la Fase 4 (P6: cero
transferencias, rama de crisis de 12 nodos, consentimiento y saludo en static_text). Se le
puso P6 como linea base... y P6 nunca se publico. Resultado medido hoy: exit=1 con 33 fallos
contra v37, los mismos 33 contra v44 y contra v45. Un gate que falla identicamente pase lo
que pase no mide deriva: es ruido, y un rojo permanente se acaba ignorando.

Resnapshotear a produccion sin mas habria borrado el requisito de F4 (que es una decision de
negocio pendiente, no un error). Asi que el gate pasa a tener DOS categorias:

  · VIGENTE — se mide contra el snapshot de PRODUCCION. Falla => exit 1. Es lo que protege
    de que alguien -- yo -- rompa lo que hoy funciona.
  · DEUDA   — propiedades del diseno F4 que produccion NO cumple. Se listan, no bloquean.
    Se conservan porque son el registro de lo que queda por decidir y desplegar.

Lo que produccion cumple y no se toca: crisis_frase es static_text y dice el Telefono de la
Esperanza, el transfer marca +34717003717, temperatura 0.22, cifras ancladas por nodo.
"""
import json, os, re, shutil, subprocess, sys

H = os.path.expanduser("~/Projects/obsidian-vault/clientes/centro-elphis/harness-voz")
G = f"{H}/gate.py"
SNAP = f"{H}/snapshots/flow-PROD-v45.json"
FLOW45 = ("/private/tmp/claude-501/-Users-manueldelmonte-Projects-elphis/"
          "937de8f5-ec06-4280-bb86-cb1b4607f480/scratchpad/fixes/flow-v45-servidor.json")

shutil.copy(G, f"{G}.PRE-2sets")
shutil.copy(FLOW45, SNAP)
print("snapshot de produccion:", SNAP)

src = open(G, encoding="utf-8").read()


def sust(viejo, nuevo, etiqueta):
    global src
    n = src.count(viejo)
    assert n == 1, f"[{etiqueta}] ancla x{n}, se esperaba 1"
    src = src.replace(viejo, nuevo)


# ── la base pasa a ser produccion, y P6 se conserva para las reglas de deuda ──
sust('BASE = json.load(open(f"{S}/snapshots/flow-P6.json", encoding="utf-8"))',
     'BASE = json.load(open(f"{S}/snapshots/flow-PROD-v45.json", encoding="utf-8"))\n'
     '# P6 = el diseno de la Fase 4, NO desplegado. Solo alimenta las comprobaciones de deuda.\n'
     'P6 = json.load(open(f"{S}/snapshots/flow-P6.json", encoding="utf-8"))',
     "base")

# ── dos contadores ───────────────────────────────────────────────────────────
sust('fallos, checks = [], 0\n'
     'def check(nombre, ok, detalle=""):\n'
     '    global checks\n'
     '    checks += 1\n'
     '    if not ok: fallos.append(f"{nombre}: {detalle}")',
     # ---
     'fallos, checks = [], 0\n'
     'pendientes, deudas = [], 0\n'
     'def check(nombre, ok, detalle=""):\n'
     '    """Inviolable VIGENTE: se mide contra produccion y su fallo bloquea (exit 1)."""\n'
     '    global checks\n'
     '    checks += 1\n'
     '    if not ok: fallos.append(f"{nombre}: {detalle}")\n\n'
     'def deuda(nombre, ok, detalle=""):\n'
     '    """Propiedad del diseno de la Fase 4 que produccion todavia NO cumple.\n'
     '    Se lista para no perderla de vista, pero NO bloquea: no es deriva, es trabajo\n'
     '    pendiente de decidir y desplegar. El dia que F4 se despliegue, estas pasan a check()."""\n'
     '    global deudas\n'
     '    deudas += 1\n'
     '    if not ok: pendientes.append(f"{nombre}: {detalle}")',
     "contadores")

# ── 1 · el bloque de crisis intacto: los nodos que existen en PRODUCCION ─────
sust('CRISIS = ["crisis_frase", "crisis_confirmar", "crisis_confirmar_tercero", "crisis_recurso",\n'
     '          "crisis_propio", "crisis_tercero", "crisis_cierre_propio", "crisis_cierre_tercero",\n'
     '          "fn_crisis_registro", "crisis_sujeto", "fn_crisis_cierre", "extract_crisis"]',
     # ---
     '# La rama de crisis TAL COMO ESTA EN PRODUCCION. La lista anterior era la de P6 (12 nodos\n'
     '# del diseno F4); ninguno de esos nodos existe en el flow servido, asi que las 12\n'
     '# comprobaciones fallaban siempre y ninguna miraba lo que de verdad esta atendiendo llamadas.\n'
     'CRISIS = ["crisis_frase", "crisis_transfer", "crisis_fallback", "crisis_confirmar",\n'
     '          "crisis_recurso"]\n'
     'CRISIS_F4 = ["crisis_confirmar_tercero", "crisis_propio", "crisis_tercero",\n'
     '             "crisis_cierre_propio", "crisis_cierre_tercero", "fn_crisis_registro",\n'
     '             "crisis_sujeto", "fn_crisis_cierre", "extract_crisis"]',
     "lista-crisis")

sust('for cid in CRISIS:\n'
     '    a, b = nodo(BASE, cid), nodo(CAND, cid)\n'
     '    check(f"crisis {cid} intacto",\n'
     '          a is not None and b is not None and json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False),\n'
     '          "ha cambiado o falta")',
     # ---
     'for cid in CRISIS:\n'
     '    a, b = nodo(BASE, cid), nodo(CAND, cid)\n'
     '    check(f"crisis {cid} intacto",\n'
     '          a is not None and b is not None and json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False),\n'
     '          "ha cambiado o falta")\n'
     'for cid in CRISIS_F4:\n'
     '    deuda(f"F4: existe el nodo {cid}", nodo(CAND, cid) is not None, "la rama de crisis de F4 no esta desplegada")',
     "bloque-crisis")

# ── 2 · el transfer: lo VIGENTE es que marque al 717; F4 pide cero transfers ──
sust('check("cero transfer_call", not any(n.get("type") == "transfer_call" for n in CAND["nodes"]),\n'
     '      "hay un nodo transfer_call: esta version no pasa llamadas a nadie")',
     # ---
     '# Produccion SI transfiere en crisis, y al Telefono de la Esperanza: decision de Manu del\n'
     '# 19-may-2026, recogida en la propuesta firmada. Lo VIGENTE es que ese numero sea el 717 y\n'
     '# no otro. "Cero transferencias" es el diseno de F4 y vive abajo, como deuda.\n'
     'ct = nodo(CAND, "crisis_transfer") or {}\n'
     'check("el transfer de crisis marca el 717 003 717",\n'
     '      (ct.get("transfer_destination") or {}).get("number", "").replace(" ", "").endswith("717003717"),\n'
     '      f\'marca {(ct.get("transfer_destination") or {}).get("number")!r}\')\n'
     'deuda("F4: cero transfer_call", not any(n.get("type") == "transfer_call" for n in CAND["nodes"]),\n'
     '      "produccion transfiere en crisis; F4 pedia darle los telefonos de viva voz")',
     "transfer")

sust('check("crisis dice 112", "112" in txt, "falta el 112 en la frase que se pronuncia")\n'
     'check("crisis dice 717 003 717", "717003717" in txt.replace(" ", ""), "falta el Telefono de la Esperanza")',
     # ---
     '# En produccion la frase ANUNCIA el transfer ("te paso ahora mismo con el Telefono de la\n'
     '# Esperanza"); el numero lo marca `crisis_transfer`, no lo dicta la voz. En F4 la frase era\n'
     '# el unico canal y por eso tenia que recitar el 112 y el 717.\n'
     'check("la frase de crisis nombra el Telefono de la Esperanza",\n'
     '      "telefono de la esperanza" in norm(txt), "la frase ya no dice a donde va la llamada")\n'
     'deuda("F4: la frase de crisis recita el 112", "112" in txt, "no se dice de viva voz")\n'
     'deuda("F4: la frase de crisis recita el 717 003 717", "717003717" in txt.replace(" ", ""),\n'
     '      "no se dice de viva voz: lo marca el transfer")',
     "frase-crisis")

sust('check("crisis_frase sigue siendo el nodo global del gate",',
     'check("crisis_frase sigue siendo el nodo global del gate",', "noop-global")

sust('check("crisis_frase deja constancia",\n'
     '      (cf.get("skip_response_edge") or {}).get("destination_node_id") == "fn_crisis_registro",\n'
     '      "la crisis ya no pasa por el registro: quedaria sin constancia")',
     # ---
     '# En produccion la salida de crisis_frase es el transfer; el registro de la crisis lo hace\n'
     '# el webhook post-call, no un nodo del flow. En F4 (sin transfer) tenia que hacerlo el flow.\n'
     'check("crisis_frase sale al transfer",\n'
     '      (cf.get("skip_response_edge") or {}).get("destination_node_id") == "crisis_transfer",\n'
     '      f\'sale a {(cf.get("skip_response_edge") or {}).get("destination_node_id")!r}\')\n'
     'deuda("F4: crisis_frase deja constancia en el flow",\n'
     '      (cf.get("skip_response_edge") or {}).get("destination_node_id") == "fn_crisis_registro",\n'
     '      "el registro depende hoy del webhook post-call")',
     "constancia")

# ── 2c · la cobertura de la condicion: es F4, produccion exige INMINENCIA ────
for viejo, et in [
    ('check("crisis cubre el riesgo de un TERCERO", "otra persona" in cc and "quitarse la vida" in cc,\n'
     '      "la condicion no dice que el riesgo contado de otra persona tambien entra: es el agujero del caso 025")', "2c-a"),
    ('check("negar la inmediatez NO desactiva la crisis",\n'
     '      "no desactiva" in cc and ("ahora mismo no esta en peligro" in cc or "no esta en peligro" in cc),\n'
     '      "la condicion no dice que \'ahora mismo no esta en peligro\' NO cancela la deteccion")', "2c-b"),
    ('check("la crisis gana al motivo de la llamada (cita/ingreso)",\n'
     '      "ingreso" in cc and ("gana" in cc or "tampoco la desactiva" in cc),\n'
     '      "la condicion no dice que gana sobre cita/ingreso: una arista normal se la come")', "2c-c"),
    ('check("hay aristas normales hacia crisis_frase", len(aristas_cf) >= 4,\n'
     '      f"solo {len(aristas_cf)}: los nodos donde aterriza una llamada deben poder entrar en crisis")', "2d"),
]:
    sust(viejo, viejo.replace("check(", "deuda(", 1).replace('deuda("crisis', 'deuda("F4: crisis', 1)
         .replace('deuda("negar', 'deuda("F4: negar', 1).replace('deuda("la crisis', 'deuda("F4: la crisis', 1)
         .replace('deuda("hay aristas', 'deuda("F4: hay aristas', 1), et)

# ── 2b · el global_prompt SI dice "te paso": es la frase de crisis ───────────
sust('for frase in ["te paso", "te pongo con", "no cuelgues"]:\n'
     '    check(f"global_prompt sin \'{frase}\'", frase not in gp, "aparece en el prompt: se recitaria")',
     # ---
     '# Produccion transfiere, asi que "te paso ... no cuelgues" es la frase CORRECTA de crisis y\n'
     '# tiene que estar. Prohibirla era un inviolable de F4 (donde no hay transfer que anunciar).\n'
     'for frase in ["te paso", "te pongo con", "no cuelgues"]:\n'
     '    deuda(f"F4: global_prompt sin \'{frase}\'", frase not in gp, "hoy es legitimo: anuncia el transfer de crisis")',
     "2b")

sust('check("global_prompt: \'transfier\' solo en prohibiciones", not malas, f"{malas[:1]}")',
     'deuda("F4: \'transfier\' solo en prohibiciones", not malas, f"{malas[:1]}")', "2b-2")

# ── 4 y 5 · art.50 y RGPD: determinismo es F4; el contenido es VIGENTE ───────
sust('check("art.50 el saludo es determinista", wi.get("type") == "static_text",\n'
     '      "el saludo vuelve a depender del LLM: el aviso de IA deja de estar garantizado")',
     # ---
     '# El nodo `welcome` es `prompt` porque tiene logica condicional (no repetir el saludo si el\n'
     '# usuario pisa la primera frase, caso 05 de la suite). Lo VIGENTE es que la frase exacta\n'
     '# este ordenada y que el aviso de IA aparezca; que ademas sea static_text es lo que pedia F4.\n'
     'check("art.50 la frase del saludo esta ordenada literal",\n'
     '      "di exactamente" in norm(wi.get("text", "")) and "soy laura" in norm(wi.get("text", "")),\n'
     '      "el saludo ya no fija la frase: el aviso de IA queda al criterio del modelo")\n'
     'deuda("F4: art.50 el saludo es static_text", wi.get("type") == "static_text",\n'
     '      "hoy es `prompt`: la identificacion como IA depende de que el modelo obedezca")',
     "art50")

sust('check("consentimiento es static_text", ci.get("type") == "static_text",\n'
     '      "la formula RGPD vuelve a depender del LLM")\n'
     'FORMULA = "para poder registrar tus datos y gestionar tu consulta, me confirmas que estas de acuerdo"',
     # ---
     '# `consentimiento` paso a `prompt` el 27-ago a proposito: como static_text se recitaba con\n'
     '# sus propias directrices en voz alta. La formula vigente dice "gestionar la cita".\n'
     'deuda("F4: consentimiento es static_text", ci.get("type") == "static_text",\n'
     '      "hoy es `prompt` (deliberado el 27-ago: el static_text se recitaba con las directrices)")\n'
     'FORMULA = "para poder registrar tus datos y gestionar la cita, me confirmas que estas de acuerdo"',
     "rgpd")

# ── 7 · topologia de salidas: la de PRODUCCION ──────────────────────────────
sust('check("solo despedida entra en end", ent_end == ["despedida"], f"{ent_end}")\n'
     'check("toda entrada a despedida viene de una herramienta o de un post-registro",\n'
     '      ent_desp == ["cierre", "cierre_cita", "fn_crisis_cierre", "fn_lead_silencioso", "preguntas"], f"{ent_desp}")',
     # ---
     '# Las dos listas son las de PRODUCCION, no las de F4. Siguen siendo un inviolable util: si\n'
     '# aparece una entrada nueva a `end` o a `despedida`, alguien ha abierto una fuga sin registro.\n'
     'check("las entradas a end son las conocidas",\n'
     '      ent_end == ["crisis_fallback", "despedida", "estado_afectado"], f"{ent_end}")\n'
     'check("las entradas a despedida son las conocidas",\n'
     '      ent_desp == ["cierre", "cierre_cita", "consentimiento", "fuera_alcance", "info_cita",\n'
     '                   "intake", "preguntas", "welcome"], f"{ent_desp}")\n'
     'deuda("F4: solo despedida entra en end", ent_end == ["despedida"], f"{ent_end}")',
     "topologia")

sust('check("consultar_cita nace apagada",\n'
     '      (CAND.get("default_dynamic_variables") or {}).get("feature_consulta_cita") == "off",\n'
     '      "la bandera de consulta de agenda esta encendida: exige OK de Alba y del DPD")',
     # ---
     '# Ausente y "off" son lo mismo aqui: la bandera no existe en el flow servido. Es el criterio\n'
     '# que ya usa T5 de `guard-retell-pin`, que vigila esto mismo cada dia contra produccion.\n'
     'check("consultar_cita nace apagada",\n'
     '      ((CAND.get("default_dynamic_variables") or {}).get("feature_consulta_cita") or "off") == "off",\n'
     '      "la bandera de consulta de agenda esta encendida: exige OK de Alba y del DPD")',
     "consultar-cita")

# ── salida: dos bloques ─────────────────────────────────────────────────────
sust('print(f"gate: {checks} comprobaciones, {len(fallos)} fallo(s)")\n'
     'for f in fallos: print("  FALLA -", f)\n'
     'sys.exit(1 if fallos else 0)',
     # ---
     'print(f"gate: {checks} inviolables VIGENTES, {len(fallos)} fallo(s)")\n'
     'for f in fallos: print("  FALLA -", f)\n'
     'print(f"deuda: {deudas} propiedades de la Fase 4, {len(pendientes)} sin desplegar (NO bloquean)")\n'
     'for p in pendientes: print("  pendiente -", p)\n'
     'sys.exit(1 if fallos else 0)',
     "salida")

open(G, "w", encoding="utf-8").write(src)
print("gate.py reescrito ·", len(src), "bytes")
