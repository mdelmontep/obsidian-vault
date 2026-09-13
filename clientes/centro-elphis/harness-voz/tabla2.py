"""Agrega TODAS las corridas de una rama, sea cual sea el sufijo (-r1, -c1, ...)."""
import json,glob,os,sys,collections
H=os.path.expanduser("~/Projects/obsidian-vault/clientes/centro-elphis/harness-voz/runs")
ramas=sys.argv[1:]
tab=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0,0]))
nr={}; shas=collections.defaultdict(set)
for rama in ramas:
    fs=sorted(glob.glob(f"{H}/{rama}-*.json"))
    nr[rama]=[os.path.basename(x)[:-5] for x in fs]
    for f in fs:
        d=json.load(open(f))
        if d.get("flow_sha"): shas[rama].add(d["flow_sha"])
        for r in d["runs"]:
            nom=r["test_case_definition_snapshot"].get("name","?")
            c=tab[nom][rama]
            if r["status"]=="error": c[2]+=1; continue
            c[1]+=1
            if r["status"]=="pass": c[0]+=1
for r in ramas: print(f"{r}: {len(nr[r])} corridas {nr[r]} | sha {sorted(shas[r]) or '(sin sello)'}")
w=max([len(n) for n in tab]+[10])+1
print(f"\n{'caso':<{w}}"+" ".join(f"{r:<14}" for r in ramas))
tot=collections.Counter()
for nom in sorted(tab):
    fila=""
    for r in ramas:
        a,b,e=tab[nom][r]; tot[r+"_ok"]+=a; tot[r+"_n"]+=b; tot[r+"_e"]+=e
        fila+=f"{f'{a}/{b}'+(f' e{e}' if e else ''):<14} "
    print(f"{nom:<{w}}{fila}")
print(f"{'TOTAL':<{w}}"+" ".join(f"{f'{tot[r+chr(95)+chr(111)+chr(107)]}/{tot[r+chr(95)+chr(110)]}'+(f' e{tot[r+chr(95)+chr(101)]}' if tot[r+'_e'] else ''):<14}" for r in ramas))
