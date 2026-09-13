"""Tabla pass/fail/error por caso, agregando todas las rondas de cada rama.
`error` es fallo del arnes o del servicio, NO del agente: se cuenta aparte y se
excluye del denominador, porque meterlo penaliza a la rama que tuvo mala suerte."""
import json,glob,os,sys,collections
H=os.path.expanduser("~/Projects/obsidian-vault/clientes/centro-elphis/harness-voz/runs")
ramas=sys.argv[1:] or ["cmp-v48","cmp-v47"]
tab=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0,0]))  # pass, validas, error
nr={}
for rama in ramas:
    fs=sorted(glob.glob(f"{H}/{rama}-r*.json"))
    nr[rama]=len(fs)
    for f in fs:
        for r in json.load(open(f))["runs"]:
            nom=r["test_case_definition_snapshot"].get("name","?")
            c=tab[nom][rama]
            if r["status"]=="error": c[2]+=1; continue
            c[1]+=1
            if r["status"]=="pass": c[0]+=1
print("rondas:",dict(nr))
w=max([len(n) for n in tab]+[10])+1
print(f"{'caso':<{w}}"+" ".join(f"{r:<14}" for r in ramas))
tot=collections.Counter()
for nom in sorted(tab):
    fila=""
    for r in ramas:
        a,b,e=tab[nom][r]; tot[r+"_ok"]+=a; tot[r+"_n"]+=b; tot[r+"_e"]+=e
        fila+=f"{f'{a}/{b}'+(f' (e{e})' if e else ''):<14} "
    print(f"{nom:<{w}}{fila}")
print(f"{'TOTAL':<{w}}"+" ".join(f"{f'{tot[r+chr(95)+chr(111)+chr(107)]}/{tot[r+chr(95)+chr(110)]}'+(f' (e{tot[r+chr(95)+chr(101)]})' if tot[r+'_e'] else ''):<14}" for r in ramas))
