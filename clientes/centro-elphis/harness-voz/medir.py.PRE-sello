"""Corre una suite contra un motor concreto y guarda el resultado CRUDO.
No decide nada: la lectura la hace contar.py sobre las transcripciones.
Se invoca:  medir.py <etiqueta> <suite> <flow_id> [version]
"""
import json,os,sys,time,urllib.request,urllib.error
# La raiz se deriva del propio fichero: este arnes vive en el vault, no en un scratchpad.
S=os.path.dirname(os.path.abspath(__file__))
TOK=open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()

def api(m,p,b=None,reintentos=3):
    for i in range(reintentos):
        r=urllib.request.Request("https://api.retellai.com"+p,method=m,
            headers={"Authorization":f"Bearer {TOK}","Content-Type":"application/json"},
            data=json.dumps(b).encode() if b is not None else None)
        try: return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            cuerpo=e.read().decode()[:300]
            if e.code>=500 and i<reintentos-1: time.sleep(5); continue
            print("HTTP",e.code,cuerpo,flush=True); raise

etiq,suite,flow=sys.argv[1],sys.argv[2],sys.argv[3]
ver=int(sys.argv[4]) if len(sys.argv)>4 else None
ids=json.load(open(suite))["test_case_definition_ids"]
eng={"type":"conversation-flow","conversation_flow_id":flow}
if ver is not None: eng["version"]=ver

b=api("POST","/create-batch-test",{"name":etiq,"test_case_definition_ids":ids,"response_engine":eng})
bid=b["test_case_batch_job_id"]; n=len(ids); t0=time.time()
while time.time()-t0<2400:
    b=api("GET",f"/get-batch-test/{bid}")
    h=b.get("pass_count",0)+b.get("fail_count",0)+b.get("error_count",0)
    if b.get("status") not in ("in_progress","pending") and h>=n: break
    time.sleep(15)
runs=api("GET",f"/v2/list-test-runs/{bid}?limit=60").get("items",[])
json.dump({"etiqueta":etiq,"batch":b,"runs":runs},
          open(f"{S}/runs/{etiq}.json","w"),ensure_ascii=False)
print(f"{etiq}: pass {b.get('pass_count')} fail {b.get('fail_count')} error {b.get('error_count')} de {n} | runs={len(runs)}",flush=True)
