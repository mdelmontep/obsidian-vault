# Retell v51 (sobre v50 publicada): naturalidad, pedido por Manu (14-sep).
#  1) Tildes en las frases que se pronuncian LITERALES: "Cuidate" en `despedida` (static_text, sale asi
#     en 3 de las ultimas 20 llamadas reales), "cuidate" en la FRASE fija de `cierre_cita` y "telefono"
#     en la frase de deletreo del global_prompt. Las frases PROHIBIDAS sin tilde ("si, aqui estoy",
#     "una ultima cosa") no se pronuncian: se quedan.
#  2) [RETIRADO, ver abajo] Una linea en "## Tono": enganche "vale" / "claro", solo en lo practico,
#     nunca tras algo doloroso, nunca dos turnos seguidos con la misma, nunca en crisis ni presentacion.
# Descartado por Manu: speech_normalization, bajar voice_temperature, acortar el prompt, backchannel.
# Sin cambios de nodos, aristas, tools, variables ni cifras.
import json, os
S = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(f"{S}/snapshots/flow-PROD-v50.json", encoding="utf-8"))
base = json.loads(json.dumps(f))
N = {n["id"]: n for n in f["nodes"]}

def sust(texto, viejo, nuevo):
    assert texto.count(viejo) == 1, f"ancla aparece {texto.count(viejo)} veces: {viejo[:70]}"
    return texto.replace(viejo, nuevo)

d = N["despedida"]["instruction"]
assert d["type"] == "static_text"
d["text"] = sust(d["text"], "Cuidate, hasta pronto.", "Cuídate, hasta pronto.")

cc = N["cierre_cita"]["instruction"]
cc["text"] = cc["text"].replace('"Perfecto. Gracias por llamar a Centro Elphis, cuidate."',
                                '"Perfecto. Gracias por llamar a Centro Elphis, cuídate."')
assert "cuidate." not in cc["text"] and cc["text"].count("cuídate.") >= 1

gp = f["global_prompt"]
gp = sust(gp, '"Perdona, por telefono no lo he cogido bien. ¿Me lo deletreas?"',
              '"Perdona, por teléfono no lo he cogido bien. ¿Me lo deletreas?"')
# 2) "vale"/"claro" RETIRADO de la v51. Con "a veces": 5% vs 5% de turnos (sin efecto). Con "uno de cada
#    tres o cuatro turnos": 8%, pero "CR harto de vivir asi" cayo a 0/4 (v50 8/9 en las mismas tandas:
#    runs r51-ctl, r51b-cand, harto51-*). Una linea que no hace nada o rompe crisis no entra.
f["global_prompt"] = gp

# 3) intake: pedir "informacion" a secas ES una pregunta. Llamadas de Manu 14-sep 13:30 y 13:32 (v50):
#    "queria informacion" -> para quien -> que te ha hecho llamar -> "pues informacion" -> que te preocupa. Cuelga.
#    La cabecera decia "recoge contexto ANTES de ofrecer informacion" y la EXCEPCION del punto 3 solo
#    cubria preguntas concretas (tratamientos, precio...).
it = N["intake"]["instruction"]
it["text"] = sust(it["text"],
  "Escucha y recoge contexto ANTES de ofrecer información. Sigue este orden, uno por turno:\n",
  "Escucha y recoge contexto mientras le informas. Sigue este orden, uno por turno:\n"
  "ANTES DEL ORDEN: SI PIDE INFORMACION EN GENERAL sin decir de que (\"queria informacion\", \"informacion sobre el centro\",\n"
  "   \"que haceis\"), eso ES una pregunta y manda sobre el orden de abajo: contestala YA, en dos frases cortas.\n"
  "   Que aqui se tratan adicciones con terapia individual, grupos, centro de dia o ingreso residencial, y que\n"
  "   la primera visita con el director es gratuita y de media hora. Termina con UNA sola pregunta para\n"
  "   concretar: si es para el o para alguien cercano, o por que sustancia o conducta.\n"
  "   Si despues vuelve a decir \"informacion\" o contesta con vaguedades, NO repitas la pregunta ni le\n"
  "   preguntes que le ha hecho llamar o que le preocupa: dale otro dato concreto (como es la terapia, en que\n"
  "   consiste la primera visita) y ofrecele esa primera visita.\n")

# Invariantes: solo cambian esos tres textos
assert [n["id"] for n in f["nodes"]] == [n["id"] for n in base["nodes"]]
for a, b in zip(f["nodes"], base["nodes"]):
    if a["id"] in ("despedida", "cierre_cita", "intake"):
        a2 = dict(a); b2 = dict(b); a2.pop("instruction"); b2.pop("instruction"); assert a2 == b2
    else:
        assert a == b, a["id"]
for k in f:
    if k not in ("global_prompt", "nodes"): assert f[k] == base[k], k
json.dump(f, open(f"{S}/flow_r51_naturalidad.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK flow_r51_naturalidad.json | global_prompt", len(base["global_prompt"]), "->", len(gp))
