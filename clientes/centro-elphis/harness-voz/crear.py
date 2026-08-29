"""Crea un borrador del agente a partir de una base, le aplica los parches y lo
verifica CONTRA EL SERVIDOR. No publica nunca: publicar es un paso aparte y a mano.
"""
import json,os,sys,copy,time,urllib.request,urllib.error
# La raiz se deriva del propio fichero: este arnes vive en el vault, no en un scratchpad.
S=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,f"{S}/v30"); import patches
TOK=open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()
PF="conversation_flow_a42bf76dcfa0"; AG="agent_e21120298343bc2ef8b4a535c9"
def api(m,p,b=None):
    r=urllib.request.Request("https://api.retellai.com"+p,method=m,
        headers={"Authorization":f"Bearer {TOK}","Content-Type":"application/json"},
        data=json.dumps(b).encode() if b is not None else None)
    try: return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:300]); raise
def sirviendo():
    return max(v["version"] for v in api("GET",f"/get-agent-versions/{AG}") if v.get("is_published"))

base=int(sys.argv[1]); saltar=tuple(sys.argv[2].split(",")) if len(sys.argv)>2 and sys.argv[2] else ()
antes=sirviendo(); print("produccion antes: v%d"%antes)
v=api("POST",f"/create-agent-version/{AG}",{"base_version":base})
nv=v["response_engine"]["version"]; print(f"borrador creado: v{nv} (NO publicado)  base=v{base}  saltando={saltar or 'nada'}")
orig=api("GET",f"/get-conversation-flow/{PF}?version={nv}")
nuevo,hechos=patches.aplicar(copy.deepcopy(orig),saltar=saltar)
for h in hechos: print("   ",h)
api("PATCH",f"/update-conversation-flow/{PF}?version={nv}",
    {"global_prompt":nuevo["global_prompt"],"nodes":nuevo["nodes"]})
time.sleep(2)
srv=api("GET",f"/get-conversation-flow/{PF}?version={nv}")
print("global_prompt identico:",srv["global_prompt"]==nuevo["global_prompt"],
      "| nodos identicos:",json.dumps(srv["nodes"],sort_keys=True)==json.dumps(nuevo["nodes"],sort_keys=True))
desp=sirviendo(); print("produccion despues: v%d"%desp)
assert desp==antes, f"PRODUCCION MOVIDA: {antes} -> {desp}"
json.dump(srv,open(f"{S}/flow-v{nv}-servidor.json","w"),ensure_ascii=False)
open(f"{S}/.draft","w").write(str(nv))
print("--- gate contra el flow REAL del servidor ---")
import subprocess
ec=subprocess.call(["python3",f"{S}/gate.py",f"{S}/flow-v{nv}-servidor.json"])
sys.exit(ec)
