import os
"""Contadores sobre las transcripciones de las corridas. No pregunta al juez:
el juez ya mintio una vez (dijo 'insiste en pedir el nombre' sobre una llamada
donde el nombre no se pidio nunca). Todo lo de aqui se mide sobre el texto y
sobre los node_transition reales.
"""
import json,glob,re,sys,unicodedata,collections

def norm(s):
    s=unicodedata.normalize("NFKD",s or "")
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[¿?¡!\"'“”]","",s)
    return re.sub(r"\s+"," ",s).strip().lower()

COSTE   = re.compile(r"\b(60|sesenta)\b|gratuit|gratis")
PIDE_NOM= re.compile(r"como te llamas|tu nombre|me dices tu nombre|cual es tu nombre")
ADIOS   = re.compile(r"cuidate|gracias por llamar|hasta luego|un saludo|que vaya bien|estamos en contacto")
SUST    = ["alcohol","cocain","cannabis","porro","juego","ludopat","apuesta","heroin","tabaco","opiac","benzodiac"]

def analiza(run):
    ts=run.get("transcript_snapshot") or {}
    tr=ts.get("transcript") or []
    dv=ts.get("dynamicVariables") or {}
    ag=[(i,norm(e.get("content"))) for i,e in enumerate(tr) if e.get("role")=="agent"]
    ruta=[(i,e.get("new_node_id")) for i,e in enumerate(tr) if e.get("role")=="node_transition"]
    idx={n:i for i,n in ruta}

    r={"caso":run.get("test_case_definition_id"),"status":run.get("status"),
       "relacion":dv.get("dv_relacion"),"nombre":dv.get("dv_nombre"),
       "nodo_final":ts.get("currentNodeId"),
       "ruta":[n for _,n in ruta]}

    # 1. nombre perdido pese a que el usuario lo dijo
    dicho=any(re.search(r"me llamo|mi nombre es|soy [a-z]{3,}",norm(e.get("content")))
              for e in tr if e.get("role")=="user")
    r["nombre_dicho_por_usuario"]=dicho
    r["nombre_perdido"]=bool(dicho and (not r["nombre"] or r["nombre"]=="Sin nombre"))

    # 2/3. aviso de coste: antes del consentimiento, y si cae en el mismo turno que el nombre
    llega=idx.get("consentimiento")
    r["llega_consentimiento"]=llega is not None
    if llega is not None:
        r["coste_antes_consentimiento"]=any(COSTE.search(t) for i,t in ag if i<llega)
    else:
        r["coste_antes_consentimiento"]=None
    r["coste_en_turno_del_nombre"]=any(COSTE.search(t) and PIDE_NOM.search(t) for _,t in ag)

    # 4. despedidas: cuantos turnos del agente se despiden
    r["turnos_despedida"]=sum(1 for _,t in ag if ADIOS.search(t))

    # 5. enumeracion de sustancias sin que se la pidan
    r["max_sustancias_en_un_turno"]=max((sum(1 for s in SUST if s in t) for _,t in ag), default=0)

    # 6. guion literal que se retiro en v30
    r["guion_encantada"]=any(re.search(r"\bencantada,? [a-z]",t) for _,t in ag)

    # 7. cuantos turnos se queda explorando en intake
    ent=idx.get("intake")
    if ent is not None:
        sale=min([i for i,n in ruta if i>ent and n!="intake"], default=len(tr))
        r["turnos_en_intake"]=sum(1 for i,_ in ag if ent<i<sale)
    else:
        r["turnos_en_intake"]=None
    return r

def resume(etiq,files):
    filas=[]
    for f in files:
        d=json.load(open(f))
        for run in d["runs"]: filas.append(analiza(run))
    n=len(filas); ok=[x for x in filas if x["status"]!="error"]
    def pct(sel,base):
        b=[x for x in filas if base(x)]
        return (sum(1 for x in b if sel(x)), len(b))
    print(f"\n=== {etiq}  ({n} llamadas, {n-len(ok)} error)")
    a,b=pct(lambda x:x["nombre_perdido"], lambda x:x["nombre_dicho_por_usuario"])
    print(f"  nombre PERDIDO pese a decirlo ....... {a}/{b}   (objetivo 0)")
    a,b=pct(lambda x:x["coste_antes_consentimiento"], lambda x:x["llega_consentimiento"])
    print(f"  coste dicho ANTES de consentimiento . {a}/{b}   (objetivo b/b)")
    a,b=pct(lambda x:x["coste_en_turno_del_nombre"], lambda x:True)
    print(f"  coste en el MISMO turno del nombre .. {a}/{b}   (objetivo 0)")
    a,b=pct(lambda x:x["turnos_despedida"]>1, lambda x:True)
    print(f"  DOBLE despedida ..................... {a}/{b}   (objetivo 0)")
    a,b=pct(lambda x:x["max_sustancias_en_un_turno"]>=3, lambda x:True)
    print(f"  enumera >=3 sustancias en un turno .. {a}/{b}   (objetivo 0)")
    a,b=pct(lambda x:x["guion_encantada"], lambda x:True)
    print(f"  guion literal 'Encantada, X' ........ {a}/{b}   (objetivo 0)")
    t=[x["turnos_en_intake"] for x in filas if x["turnos_en_intake"] is not None]
    print(f"  turnos en intake .................... media {sum(t)/len(t):.1f} max {max(t)}" if t else "  turnos en intake .... sin datos")
    return filas

if __name__=="__main__":
    # La raiz se deriva del propio fichero: este arnes vive en el vault, no en un scratchpad.
S=os.path.dirname(os.path.abspath(__file__))
    for etiq,pat in [("v29 (control)",f"{S}/runs/reg-v29-*.json"),
                     ("v30 (candidato)",f"{S}/runs/reg-v30-*.json"),
                     ("crisis v30",f"{S}/runs/crisis-v30.json")]:
        fs=sorted(glob.glob(pat))
        if fs: resume(etiq,fs)
        else:  print(f"\n=== {etiq}: sin corridas todavia")
