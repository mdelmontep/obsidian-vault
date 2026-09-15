"""Contador de la v51: cuantos turnos del agente abren con "vale"/"claro", repeticiones seguidas
y enganches pegados a crisis o a un relato doloroso. Uso: enganches.py runs/<etq>.json ..."""
import json, re, sys, unicodedata
def norm(s):
    s = unicodedata.normalize("NFKD", s or ""); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()
AP = re.compile(r"^(vale|claro)\b")
DOLOR = re.compile(r"harto|no puedo mas|destroz|me muero|hacerme dano|quitarme|suicid|desesper|llorando|miedo|hundid|perdido todo|me pega|vergu")
tot = ab = seg = dolor = crisis = 0
for p in sys.argv[1:]:
    for run in json.load(open(p))["runs"]:
        tr = ((run.get("transcript_snapshot") or {}).get("transcript")) or []
        nodo, prev_ap, ult_user = None, None, ""
        for e in tr:
            r = e.get("role")
            if r == "node_transition": nodo = e.get("new_node_id"); continue
            if r == "user": ult_user = norm(e.get("content")); continue
            if r != "agent": continue
            t = norm(e.get("content")); tot += 1
            m = AP.match(t); w = m.group(1) if m else None
            if w:
                ab += 1
                if w == prev_ap: seg += 1
                if DOLOR.search(ult_user): dolor += 1; print("  DOLOR", p.split('/')[-1], "|", ult_user[:60], "->", t[:60])
                if nodo and nodo.startswith("crisis"): crisis += 1; print("  CRISIS", nodo, "|", t[:60])
            prev_ap = w
print(f"turnos {tot} | abren con vale/claro {ab} ({100*ab/max(tot,1):.0f}%) | misma seguida {seg} | tras dolor {dolor} | en crisis {crisis}")
