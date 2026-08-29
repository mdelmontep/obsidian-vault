"""Pone el flow de TEST en un estado concreto. El transfer de crisis del flow de
test se queda SIEMPRE en el numero neutro: una suite de crisis que marque el 717
real llama al Telefono de la Esperanza de verdad."""
import json,os,sys,copy,urllib.request,urllib.error
# La raiz se deriva del propio fichero: este arnes vive en el vault, no en un scratchpad.
S=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,f"{S}/v30"); import patches
TOK=open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()
TF="conversation_flow_b857e417f7f8"
def api(m,p,b=None):
    r=urllib.request.Request("https://api.retellai.com"+p,method=m,
        headers={"Authorization":f"Bearer {TOK}","Content-Type":"application/json"},
        data=json.dumps(b).encode() if b is not None else None)
    try: return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:300]); raise
modo=sys.argv[1]                      # "base" | "P1,P3,P4,P5,P6"
base=json.load(open(f"{S}/snapshots/flow-TEST-antes.json"))
if modo=="base":
    g=base
else:
    todos={"P1","P2","P3","P3c","P4","P5","P6"}
    g,h=patches.aplicar(copy.deepcopy(base),saltar=tuple(todos-set(modo.split(","))))
    print("  aplicados:",h)
api("PATCH",f"/update-conversation-flow/{TF}",{"global_prompt":g["global_prompt"],"nodes":g["nodes"]})
srv=api("GET",f"/get-conversation-flow/{TF}")
ct=json.dumps(next(n for n in srv["nodes"] if n["id"]=="crisis_transfer"),ensure_ascii=False).replace(" ","")
assert "600000000" in ct and "717003717" not in ct, "TEST con transfer REAL: abortado"
assert srv["global_prompt"]==g["global_prompt"], "el servidor no aplico el global_prompt"
print(f"  flow de TEST en modo '{modo}' | transfer neutro OK")
