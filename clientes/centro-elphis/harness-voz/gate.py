#!/usr/bin/env python3
"""Gate de inviolables del agente de voz de Centro Elphis.

DOS CATEGORIAS, DOS SALIDAS (9-sep-2026):

- check()  VIGENTE. Se mide contra `snapshots/flow-PROD-v45.json`, que es lo que sirve el
           +34910054950 hoy. Su fallo BLOQUEA (exit 1). Protege de que alguien rompa lo que
           funciona: que la frase de identificacion como IA este ordenada literal y en el
           primer turno (art. 50), que la formula RGPD siga intacta en su nodo y sin duplicar
           en el global_prompt, el 717 003 717 en `crisis_transfer`, las cifras ancladas al
           nodo que las dice, y que ninguna salida conversacional se vaya sin pasar por una
           herramienta. OJO: que el saludo y el consentimiento sean `static_text` -es decir,
           que no dependan de que el modelo obedezca- NO es un check: hoy los dos son
           `prompt` y eso es DEUDA de F4 (el consentimiento, ademas, a proposito desde el
           27-ago). El gate garantiza que la frase este mandada, no que sea determinista.
- deuda()  Propiedades del diseno de la Fase 4 (`snapshots/flow-P6.json`) que produccion NO
           cumple. Se LISTAN y no bloquean. El dia que F4 se despliegue, cada deuda() pasa a
           check(). Se conservan porque son el registro de lo que queda por decidir.

Por que se parte en dos (9-sep): el gate se reescribio el 7-sep con P6 como linea base, y P6
nunca se publico. Resultado medido: exit=1 con LOS MISMOS 33 fallos contra v37, contra v44 y
contra v45. Un gate que falla identicamente pase lo que pase no mide deriva; un rojo
permanente se acaba ignorando, que es justo el fallo que motivo la reescritura del 7-sep.
Resnapshotear a produccion a secas habria borrado el requisito de F4, que es una decision de
negocio pendiente, no un error.

OJO CON LA CABECERA DEL 7-SEP, que decia: «BLOQUEABA el cambio que Alba ha pedido (cero
transferencias)». Esa afirmacion no aparece en ningun otro sitio del vault y contradice el
transfer al 717 003 717 que Manu confirmo el 19-may y que esta en la propuesta firmada. Un
gate no es sitio para guardar la unica copia de una decision de negocio: mientras no se
cierre con la clienta, el transfer al 717 es VIGENTE y su ausencia es DEUDA.

Uso: gate.py [flow.json]   ->  exit 0 si los inviolables VIGENTES se cumplen.
"""
import json, os, sys, re, unicodedata

S = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(f"{S}/snapshots/flow-PROD-v45.json", encoding="utf-8"))
# P6 = el diseno de la Fase 4, NO desplegado. Solo alimenta las comprobaciones de deuda.
P6 = json.load(open(f"{S}/snapshots/flow-P6.json", encoding="utf-8"))
CAND = json.load(open(sys.argv[1], encoding="utf-8"))

# La rama de crisis TAL COMO ESTA EN PRODUCCION. La lista anterior era la de P6 (12 nodos
# del diseno F4); ninguno de esos nodos existe en el flow servido, asi que las 12
# comprobaciones fallaban siempre y ninguna miraba lo que de verdad esta atendiendo llamadas.
CRISIS = ["crisis_frase", "crisis_transfer", "crisis_fallback", "crisis_confirmar",
          "crisis_recurso"]
CRISIS_F4 = ["crisis_confirmar_tercero", "crisis_propio", "crisis_tercero",
             "crisis_cierre_propio", "crisis_cierre_tercero", "fn_crisis_registro",
             "crisis_sujeto", "fn_crisis_cierre", "extract_crisis"]

def norm(s):
    # NFKD descompone el acento en base + marca combinante; hay que BORRAR la marca, no solo
    # descomponerla, o "estas" nunca casa con "estás". Se quitan tambien los signos ¿? ¡! y las
    # comillas, que el JSON escapa de formas distintas segun quien lo escribiera.
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[¿?¡!\"'“”]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def nodo(f, i):
    return next((n for n in f["nodes"] if n.get("id") == i), None)

fallos, checks = [], 0
pendientes, deudas = [], 0
def check(nombre, ok, detalle=""):
    """Inviolable VIGENTE: se mide contra produccion y su fallo bloquea (exit 1)."""
    global checks
    checks += 1
    if not ok: fallos.append(f"{nombre}: {detalle}")

def deuda(nombre, ok, detalle=""):
    """Propiedad del diseno de la Fase 4 que produccion todavia NO cumple.
    Se lista para no perderla de vista, pero NO bloquea: no es deriva, es trabajo
    pendiente de decidir y desplegar. El dia que F4 se despliegue, estas pasan a check()."""
    global deudas
    deudas += 1
    if not ok: pendientes.append(f"{nombre}: {detalle}")

# 1. La rama de crisis, INTACTA byte a byte. Es el unico bloque con riesgo clinico.
for cid in CRISIS:
    a, b = nodo(BASE, cid), nodo(CAND, cid)
    check(f"crisis {cid} intacto",
          a is not None and b is not None and json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False),
          "ha cambiado o falta")
for cid in CRISIS_F4:
    deuda(f"F4: existe el nodo {cid}", nodo(CAND, cid) is not None, "la rama de crisis de F4 no esta desplegada")

# 2. CERO transferencias, y los telefonos de ayuda dichos de viva voz en la frase de crisis.
# Produccion SI transfiere en crisis, y al Telefono de la Esperanza: decision de Manu del
# 19-may-2026, recogida en la propuesta firmada. Lo VIGENTE es que ese numero sea el 717 y
# no otro. "Cero transferencias" es el diseno de F4 y vive abajo, como deuda.
ct = nodo(CAND, "crisis_transfer") or {}
check("el transfer de crisis marca el 717 003 717",
      (ct.get("transfer_destination") or {}).get("number", "").replace(" ", "").endswith("717003717"),
      f'marca {(ct.get("transfer_destination") or {}).get("number")!r}')
deuda("F4: cero transfer_call", not any(n.get("type") == "transfer_call" for n in CAND["nodes"]),
      "produccion transfiere en crisis; F4 pedia darle los telefonos de viva voz")
cf = nodo(CAND, "crisis_frase") or {}
ins = cf.get("instruction") or {}
check("crisis_frase es static_text", ins.get("type") == "static_text",
      f"es {ins.get('type')}: con 'prompt' la frase deja de ser determinista")
txt = ins.get("text") or ""
# En produccion la frase ANUNCIA el transfer ("te paso ahora mismo con el Telefono de la
# Esperanza"); el numero lo marca `crisis_transfer`, no lo dicta la voz. En F4 la frase era
# el unico canal y por eso tenia que recitar el 112 y el 717.
check("la frase de crisis nombra el Telefono de la Esperanza",
      "telefono de la esperanza" in norm(txt), "la frase ya no dice a donde va la llamada")
deuda("F4: la frase de crisis recita el 112", "112" in txt, "no se dice de viva voz")
deuda("F4: la frase de crisis recita el 717 003 717", "717003717" in txt.replace(" ", ""),
      "no se dice de viva voz: lo marca el transfer")
check("crisis_frase sigue siendo el nodo global del gate",
      (cf.get("global_node_setting") or {}).get("condition") == (nodo(BASE, "crisis_frase") or {}).get("global_node_setting", {}).get("condition"),
      "la condicion del gate de crisis ha cambiado")
# En produccion la salida de crisis_frase es el transfer; el registro de la crisis lo hace
# el webhook post-call, no un nodo del flow. En F4 (sin transfer) tenia que hacerlo el flow.
check("crisis_frase sale al transfer",
      (cf.get("skip_response_edge") or {}).get("destination_node_id") == "crisis_transfer",
      f'sale a {(cf.get("skip_response_edge") or {}).get("destination_node_id")!r}')
deuda("F4: crisis_frase deja constancia en el flow",
      (cf.get("skip_response_edge") or {}).get("destination_node_id") == "fn_crisis_registro",
      "el registro depende hoy del webhook post-call")

# 2c. LA COBERTURA DE LA CONDICION DE CRISIS (F4b, 7-sep-2026).
#     Los checks 1 y 2 anclaban la condicion del gate de crisis al snapshot: BYTE A BYTE. Eso no es
#     un inviolable, es un CONGELADO — y lo que congelaba estaba medido como roto: con la condicion
#     de v34, el caso 025 (T2: ideacion explicita de un tercero contada por la tia, con "ahora mismo
#     no esta en peligro" en el mismo turno) NO entraba en la rama de crisis en ninguna de las dos
#     corridas de F4. Un gate que impide arreglar el agujero que motivo el plan no protege: obliga a
#     saltarselo. Se re-ancla la base al borrador corregido y se anaden aqui las tres propiedades
#     que el congelado suplia, que ademas son INDEPENDIENTES de la base:
#       (a) la condicion cubre el riesgo dicho de OTRA persona;
#       (b) que se niegue la inmediatez no la desactiva;
#       (c) que la llamada venga por cita/ingreso no la desactiva.
#     Medido: sin (a) T2 se queda fuera; sin (c) T2 se va por `e_w_ingreso` y los globales ya no se
#     reevaluan para ese turno (batch test_batch_3e2b333ed813: D1, el mismo texto SIN la negacion de
#     inmediatez, tampoco entraba; D2, el mismo texto SIN el encuadre de ingreso, si entraba).
cond_cf = ((nodo(CAND, "crisis_frase") or {}).get("global_node_setting") or {}).get("condition") or ""
cc = norm(cond_cf)
deuda("F4: crisis cubre el riesgo de un TERCERO", "otra persona" in cc and "quitarse la vida" in cc,
      "la condicion no dice que el riesgo contado de otra persona tambien entra: es el agujero del caso 025")
deuda("F4: negar la inmediatez NO desactiva la crisis",
      "no desactiva" in cc and ("ahora mismo no esta en peligro" in cc or "no esta en peligro" in cc),
      "la condicion no dice que 'ahora mismo no esta en peligro' NO cancela la deteccion")
deuda("F4: la crisis gana al motivo de la llamada (cita/ingreso)",
      "ingreso" in cc and ("gana" in cc or "tampoco la desactiva" in cc),
      "la condicion no dice que gana sobre cita/ingreso: una arista normal se la come")

# 2d. Las aristas normales que llevan a `crisis_frase` deben llevar EXACTAMENTE la misma condicion
#     que el nodo global. Este es el defecto medido: `e_w_crisis` era mas ESTRECHA que hacia falta y,
#     al casar `e_w_ingreso` antes, la decision del turno se cerraba sin que el global entrara nunca.
#     Una arista mas estrecha que el global es un falso negativo silencioso; esta comprobacion no
#     depende de la base, solo de que las dos cosas digan lo mismo.
aristas_cf = [(n["id"], e["id"], (e.get("transition_condition") or {}).get("prompt") or "")
              for n in CAND["nodes"] for e in (n.get("edges") or [])
              if e.get("destination_node_id") == "crisis_frase" and not (n.get("global_node_setting"))]
deuda("F4: hay aristas normales hacia crisis_frase", len(aristas_cf) >= 4,
      f"solo {len(aristas_cf)}: los nodos donde aterriza una llamada deben poder entrar en crisis")
desync = [(nid, eid) for nid, eid, p in aristas_cf if p != cond_cf]
check("las aristas a crisis_frase no se desincronizan del global", not desync, f"{desync}")

# 2e. Toda arista de ECUACION referencia la variable con {{ }}. Medido el 7-sep-2026: `e_cs_tercero`
#     comparaba `"dv_crisis_sujeto" == "tercero"` (la cadena literal, sin llaves), que nunca es cierto,
#     y las cuatro sondas de crisis de tercero cayeron por el else a `crisis_propio` — el nodo que
#     afirma que la persona en riesgo esta al telefono — con dv_crisis_sujeto == "tercero".
mal_eq = []
for n in CAND["nodes"]:
    es = list(n.get("edges") or [])
    for k in ("else_edge", "skip_response_edge", "edge"):
        if n.get(k): es.append(n[k])
    for e in es:
        tc = e.get("transition_condition") or {}
        if tc.get("type") != "equation": continue
        for eq in tc.get("equations") or []:
            if not re.fullmatch(r"\{\{[^{}]+\}\}", str(eq.get("left", ""))):
                mal_eq.append((n["id"], e.get("id"), eq.get("left")))
check("las ecuaciones referencian la variable con {{ }}", not mal_eq, f"{mal_eq}")

# 2b. El global_prompt no puede ORDENAR transferir. "transfier" es legitimo dentro de una
#     prohibicion; "te paso" / "te pongo con" / "no cuelgues" no lo son en ningun contexto.
gp_raw = CAND.get("global_prompt") or ""
gp = norm(gp_raw)
# Produccion transfiere, asi que "te paso ... no cuelgues" es la frase CORRECTA de crisis y
# tiene que estar. Prohibirla era un inviolable de F4 (donde no hay transfer que anunciar).
for frase in ["te paso", "te pongo con", "no cuelgues"]:
    deuda(f"F4: global_prompt sin '{frase}'", frase not in gp, "hoy es legitimo: anuncia el transfer de crisis")
malas = [l for l in gp_raw.lower().split("\n")
         if "transfier" in l and not re.search(r"nunca|prohibid|no digas|jamas", l)]
deuda("F4: 'transfier' solo en prohibiciones", not malas, f"{malas[:1]}")

# 3. Motor: temperatura y modelo no se tocan (la temperatura evalua tambien las condiciones de arista).
check("temperatura 0.22", CAND.get("model_temperature") == 0.22, f"es {CAND.get('model_temperature')}")
check("modelo haiku 4.5", (CAND.get("model_choice") or {}).get("model") == (BASE.get("model_choice") or {}).get("model"), "modelo cambiado")

# 4. Art. 50: la identificacion como IA sigue en el PRIMER turno y sigue siendo determinista.
w = nodo(CAND, "welcome") or {}
wi = w.get("instruction") or {}
# El nodo `welcome` es `prompt` porque tiene logica condicional (no repetir el saludo si el
# usuario pisa la primera frase, caso 05 de la suite). Lo VIGENTE es que la frase exacta
# este ordenada y que el aviso de IA aparezca; que ademas sea static_text es lo que pedia F4.
check("art.50 la frase del saludo esta ordenada literal",
      "di exactamente" in norm(wi.get("text", "")) and "soy laura" in norm(wi.get("text", "")),
      "el saludo ya no fija la frase: el aviso de IA queda al criterio del modelo")
deuda("F4: art.50 el saludo es static_text", wi.get("type") == "static_text",
      "hoy es `prompt`: la identificacion como IA depende de que el modelo obedezca")
check("art.50 inteligencia artificial", "inteligencia artificial" in norm(wi.get("text", "")),
      "falta (o abreviado a la sigla, que el TTS lee mal)")
check("art.50 el saludo es el primer turno", CAND.get("start_node_id") in ("calc_hora", "welcome"),
      f"start_node_id={CAND.get('start_node_id')}")
check("art.50 el nodo de inicio no habla",
      (nodo(CAND, "calc_hora") or {}).get("speak_during_execution") in (False, None),
      "el nodo de inicio habla antes del aviso de IA")

# 5. El consentimiento sigue pidiendose en SU nodo, literal, y solo ahi.
cons = nodo(CAND, "consentimiento") or {}
ci = cons.get("instruction") or {}
# `consentimiento` paso a `prompt` el 27-ago a proposito: como static_text se recitaba con
# sus propias directrices en voz alta. La formula vigente dice "gestionar la cita".
deuda("F4: consentimiento es static_text", ci.get("type") == "static_text",
      "hoy es `prompt` (deliberado el 27-ago: el static_text se recitaba con las directrices)")
FORMULA = "para poder registrar tus datos y gestionar la cita, me confirmas que estas de acuerdo"
check("formula RGPD literal e intacta", FORMULA in norm(ci.get("text", "")),
      "la frase de consentimiento ha cambiado o desaparecido")
check("consentimiento NO duplicado en global", "me confirmas que estas de acuerdo" not in gp,
      "la formula ha vuelto al global_prompt: se pedira dos veces")

# 6. Topologia: mismos nodos, ni uno mas ni uno menos.
check("mismos nodos", sorted(n["id"] for n in BASE["nodes"]) == sorted(n["id"] for n in CAND["nodes"]),
      "el conjunto de nodos ha cambiado")

# 7. Garantia de registro: ninguna salida conversacional llega a `despedida` o a `end` sin
#    haber pasado por una herramienta. Sustituye al check de aristas de fuga por nombre, que
#    comprobaba el sintoma (que existiera e_bienv_fin) y no la propiedad.
def salidas(n):
    es = list(n.get("edges") or [])
    for k in ("else_edge", "skip_response_edge", "edge"):
        if n.get(k): es.append(n[k])
    return [e.get("destination_node_id") for e in es if e.get("destination_node_id")]
ent_desp = sorted({n["id"] for n in CAND["nodes"] if "despedida" in salidas(n)})
ent_end = sorted({n["id"] for n in CAND["nodes"] if "end" in salidas(n)})
# Las dos listas son las de PRODUCCION, no las de F4. Siguen siendo un inviolable util: si
# aparece una entrada nueva a `end` o a `despedida`, alguien ha abierto una fuga sin registro.
check("las entradas a end son las conocidas",
      ent_end == ["crisis_fallback", "despedida", "estado_afectado"], f"{ent_end}")
check("las entradas a despedida son las conocidas",
      ent_desp == ["cierre", "cierre_cita", "consentimiento", "fuera_alcance", "info_cita",
                   "intake", "preguntas", "welcome"], f"{ent_desp}")
deuda("F4: solo despedida entra en end", ent_end == ["despedida"], f"{ent_end}")
# Ausente y "off" son lo mismo aqui: la bandera no existe en el flow servido. Es el criterio
# que ya usa T5 de `guard-retell-pin`, que vigila esto mismo cada dia contra produccion.
check("consultar_cita nace apagada",
      ((CAND.get("default_dynamic_variables") or {}).get("feature_consulta_cita") or "off") == "off",
      "la bandera de consulta de agenda esta encendida: exige OK de Alba y del DPD")

# 8. Precios y domicilio, ANCLADOS AL NODO QUE LOS DICE.
#    Comprobar que la cifra existe "en algun sitio del flow" no discrimina: una mutacion que
#    cambiaba 1.772 -> 1.900 en info_cita pasaba el gate porque la cifra vivia tambien en otro
#    nodo. Se compara el multiconjunto de cifras nodo a nodo.
def textos(n):
    # SOLO lo que se pronuncia o condiciona. json.dumps del nodo entero metia
    # `display_position` (x=1326, y=414...) en el recuento: el gate saltaba al mover un nodo
    # en la UI, que es un falso positivo, y un gate con falsos positivos se acaba saltando.
    out = []
    if isinstance(n, str): return [n]
    ins = n.get("instruction") or {}
    out.append(ins.get("text") or "")
    es = list(n.get("edges") or [])
    for k in ("else_edge", "skip_response_edge", "edge"):
        if n.get(k): es.append(n[k])
    for e in es:
        tc = e.get("transition_condition") or {}
        out.append(str(tc.get("prompt") or ""))
    out.append(str((n.get("global_node_setting") or {}).get("condition") or ""))
    return out

def cifras(n):
    return sorted(re.findall(r"\b\d{1,2}[.,]\d{3}\b|\b\d{3,4}\b", " ".join(textos(n))))
for b in BASE["nodes"]:
    c = nodo(CAND, b["id"])
    if c is None: continue
    cb = cifras(b)
    if not cb: continue
    check(f"cifras intactas en {b['id']}", cifras(c) == cb, f"{cb} -> {cifras(c)}")
# 8b. Los precios REALES viven en el global_prompt, no en info_cita: sin este check, alterar
#     una tarifa pasaba el gate entero (medido por mutacion; el caso de info_cita era un
#     mutante equivalente, no una victima).
check("cifras intactas en global_prompt", cifras(gp_raw) == cifras(BASE.get("global_prompt") or ""),
      f"{cifras(BASE.get('global_prompt') or '')} -> {cifras(gp_raw)}")
check("domicilio O'Donnell", "O'Donnell" in json.dumps(CAND, ensure_ascii=False), "ha desaparecido")

print(f"gate: {checks} inviolables VIGENTES, {len(fallos)} fallo(s)")
for f in fallos: print("  FALLA -", f)
print(f"deuda: {deudas} propiedades de la Fase 4, {len(pendientes)} sin desplegar (NO bloquean)")
for p in pendientes: print("  pendiente -", p)
sys.exit(1 if fallos else 0)
