# Retell v49 (sobre v48 publicada): el horario del centro.
# Llamada real 13-sep 13:43 (call_f27129552274466c52afa564ebd): a "¿qué horario tenéis?" Laura
# dijo "te lo confirma recepción cuando te llamen" y dos turnos después lo recitó igual, desde la
# Base de conocimiento, como "de 9 a 21 horas". Dos fallos:
#  1. La regla de A1 prohibía dar el horario FIJO (que sí sabemos) para evitar que dedujera si el
#     centro está abierto AHORA (que no sabemos). El dato seguía en la base: el modelo se
#     contradecía entre las dos.
#  2. Las cifras en formato 24 h se leen tal cual ("veintiuna horas"). La instrucción de cómo
#     decirlas va pegada al dato, no en otra sección
#     (-> dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion).
# Solo texto del global_prompt. Única cifra quitada: el "9" de "manana a las 9" (ahora en palabras).
# Nodos, aristas y tools intactos.
import json, os, re
S = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(f"{S}/snapshots/flow-PROD-v48.json", encoding="utf-8"))
base = json.loads(json.dumps(f))
g = f["global_prompt"]

CAMBIOS = [
 ('- NUNCA digas que el centro esta cerrado ni abierto, ni a que hora abre, ni "manana a las 9".\n'
  '- Si preguntan por el horario: "El horario te lo confirma recepcion cuando te llamen."\n',
  '- El horario FIJO del centro si lo sabes y lo das cuando lo pregunten, con estas palabras:\n'
  '  "De lunes a viernes, de nueve de la mañana a nueve de la noche. Los sábados, de nueve de la\n'
  '  mañana a tres de la tarde. Domingos y festivos, cerrado."\n'
  '  Nunca lo mandes a recepción: es un dato que tienes.\n'
  '- Lo que NO sabes es si AHORA está abierto: NUNCA digas "ahora está cerrado", "ahora mismo\n'
  '  abierto" ni "mañana a las nueve".\n'),
 ("Horario: L-V 9-21 h, S 9-15 h. Cerrado domingos y festivos.",
  "Horario (dilo SIEMPRE con palabras y en horas de reloj: \"de nueve de la mañana a nueve de la noche\"; "
  "NUNCA leas las cifras tal cual ni digas \"veintiuna horas\"): L-V 9-21 h, S 9-15 h. Cerrado domingos y festivos."),
 ("Horario: L-J 10-19 h, V 10-15:30 h (salen comidos), S 11-13 h (ese día solo ambulatorio grupal).",
  "Horario (dilo con palabras y en horas de reloj, \"de diez de la mañana a siete de la tarde\"): "
  "L-J 10-19 h, V 10-15:30 h (salen comidos), S 11-13 h (ese día solo ambulatorio grupal)."),
]
for viejo, nuevo in CAMBIOS:
    assert g.count(viejo) == 1, f"ancla aparece {g.count(viejo)} veces: {viejo[:60]}"
    g = g.replace(viejo, nuevo)
f["global_prompt"] = g

cif = lambda t: sorted(re.findall(r"\b\d{1,2}[.,]\d{3}\b|\b\d{1,4}\b", t))
import collections as C
assert C.Counter(cif(base["global_prompt"])) - C.Counter(cif(g)) == C.Counter(["9"]) and not (C.Counter(cif(g)) - C.Counter(cif(base["global_prompt"]))), "cifras distintas de lo declarado"
assert "te lo confirma recepcion" not in g
for k in ("nodes", "tools", "start_node_id", "default_dynamic_variables"):
    assert json.dumps(f.get(k), sort_keys=True) == json.dumps(base.get(k), sort_keys=True), f"{k} tocado"
json.dump(f, open(f"{S}/flow_r49_horario.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"escrito flow_r49_horario.json | global_prompt {len(base['global_prompt'])} -> {len(g)} car.")
