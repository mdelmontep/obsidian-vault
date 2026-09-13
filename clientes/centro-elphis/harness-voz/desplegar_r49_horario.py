"""Despliega el candidato de horario (Retell v49, base v48; ver patch_r49_horario.py). NO se ejecuta solo: hay que pasarle --publicar
y luego --pin. Cada paso verifica contra el servidor y aborta si produccion se movio.

Paso 1 (sin flags): crea el borrador desde base 48, empuja el flow y pasa el gate.
Paso 2 (--publicar): publica la version creada.
Paso 3 (--pin): sube el pin del trinquete en Postgres. SIN ESTO NO HAY DESPLIEGUE:
                el DDI esta fijado al entero, no a 'latest_published'.
"""
import json,os,sys,copy,time,subprocess,urllib.request,urllib.error
S=os.path.dirname(os.path.abspath(__file__))
H="/Users/manueldelmonte/Projects/obsidian-vault/clientes/centro-elphis/harness-voz"
TOK=open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()
PF="conversation_flow_a42bf76dcfa0"; AG="agent_e21120298343bc2ef8b4a535c9"; DDI="+34910054950"
CAND=f"{S}/flow_r49_horario.json"
def api(m,p,b=None):
    r=urllib.request.Request("https://api.retellai.com"+p,method=m,
        headers={"Authorization":f"Bearer {TOK}","Content-Type":"application/json"},
        data=json.dumps(b).encode() if b is not None else None)
    try:
        # publish-agent-version responde 200/204 con CUERPO VACIO: json.load revienta
        # con "Expecting value: line 1 column 1". Un cuerpo vacio aqui es exito.
        cuerpo=urllib.request.urlopen(r).read()
        return json.loads(cuerpo) if cuerpo.strip() else {}
    except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:400]); raise
def sirviendo(): return max(v["version"] for v in api("GET",f"/get-agent-versions/{AG}") if v.get("is_published"))
def ddi_version():
    ph=api("GET",f"/get-phone-number/{DDI}")
    return (ph.get("inbound_agents") or [{}])[0].get("agent_version")

def sin_ruido(n):
    # PATCH /update-conversation-flow escribe skippable:false en TODOS los nodos (no documentado).
    return {k:v for k,v in n.items() if not (k=="skippable" and v is False)}

if "--pin" in sys.argv:
    nv=int(open(f"{S}/.r49h_version").read().strip())
    pub=[v for v in api("GET",f"/get-agent-versions/{AG}") if v["version"]==nv]
    assert pub and pub[0].get("is_published"), f"v{nv} no esta publicada: publica antes de subir el pin"
    sql=("UPDATE idempotency_log SET response = jsonb_set(response,'{pin}','%d'::jsonb), "
         "created_at = NOW() WHERE key = 'guard-retell-pin:config'") % nv
    c=["ssh","elphis","docker exec elphis-n8nwithpostgres-wtqddl-postgres-aux-1 "
       "psql -U elphis_app -d elphis_app -c \"%s\" -c \"SELECT response->>'pin' AS pin FROM idempotency_log "
       "WHERE key='guard-retell-pin:config'\"" % sql]
    print(subprocess.run(c,capture_output=True,text=True).stdout)
    print(f"pin subido a {nv}. T1 repone el DDI en <=5 min. DDI ahora: v{ddi_version()}")
    print(f"ROLLBACK: el mismo UPDATE con 48 en vez de {nv}.")
    sys.exit(0)

if "--publicar" in sys.argv:
    nv=int(open(f"{S}/.r49h_version").read().strip())
    antes=sirviendo(); ddi=ddi_version()
    # La version va en el CUERPO, no como query param: ?version= devuelve
    # 400 "Unknown query parameter 'version'". Verificado 13-sep-2026.
    api("POST",f"/publish-agent-version/{AG}",{"version":nv})
    time.sleep(2)
    ahora=sirviendo()
    assert ahora==nv, f"NO se publico: max publicada sigue en {ahora}, esperaba {nv}"
    print(f"publicada v{nv}. max publicada: {antes} -> {ahora}")
    print(f"DDI sigue en v{ddi_version()} (era v{ddi}) — correcto: publicar NO despliega. Falta --pin.")
    sys.exit(0)

# ---- paso 1: crear el borrador y empujar el candidato ----
antes=sirviendo(); ddi=ddi_version()
print(f"produccion antes: publicada v{antes} | DDI sirviendo v{ddi}")
assert ddi==48, f"el DDI no esta en 48 sino en {ddi}: parar y mirar"
g=json.load(open(CAND,encoding="utf-8"))
v=api("POST",f"/create-agent-version/{AG}",{"base_version":48})
nv=v["response_engine"]["version"]
print(f"borrador creado: v{nv} (NO publicado), base=v48")
api("PATCH",f"/update-conversation-flow/{PF}?version={nv}",
    {"global_prompt":g["global_prompt"],"nodes":g["nodes"],"tools":g["tools"],
     "start_node_id":g["start_node_id"],"default_dynamic_variables":g.get("default_dynamic_variables")})
time.sleep(2)
srv=api("GET",f"/get-conversation-flow/{PF}?version={nv}")
assert srv["global_prompt"]==g["global_prompt"], "el servidor no guardo el global_prompt"
a={n["id"]:sin_ruido(n) for n in g["nodes"]}; b={n["id"]:sin_ruido(n) for n in srv["nodes"]}
assert set(a)==set(b), f"nodos distintos: {sorted(set(a)^set(b))}"
dif=[i for i in a if json.dumps(a[i],sort_keys=True,ensure_ascii=False)!=json.dumps(b[i],sort_keys=True,ensure_ascii=False)]
assert not dif, f"el servidor guardo otra cosa en: {dif}"
assert json.dumps(srv.get("tools"),sort_keys=True)==json.dumps(g.get("tools"),sort_keys=True), "tools no coinciden"
assert srv.get("start_node_id")==g.get("start_node_id"), "start_node_id no coincide"
desp=sirviendo(); assert desp==antes, f"PRODUCCION MOVIDA: {antes} -> {desp}"
assert ddi_version()==48, "el DDI se movio durante el proceso"
json.dump(srv,open(f"{S}/flow_v{nv}_srv.json","w",encoding="utf-8"),ensure_ascii=False)
open(f"{S}/.r49h_version","w").write(str(nv))
print(f"verificado contra el servidor. produccion intacta (publicada v{desp}, DDI v48).")
print("--- gate contra el flow REAL del servidor ---")
sys.exit(subprocess.call(["python3",f"{H}/gate.py",f"{S}/flow_v{nv}_srv.json"]))
