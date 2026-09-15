# Casos de la v51: pedir "informacion" a secas (llamadas de Manu 14-sep 13:30 y 13:32, v50).
import json,os,urllib.request
S=os.path.dirname(os.path.abspath(__file__))
TOK=open(os.path.expanduser("~/Projects/elphis-psicologia/infra/tests/.token-retell")).read().strip()
def api(m,p,b=None):
    r=urllib.request.Request("https://api.retellai.com"+p,method=m,headers={"Authorization":f"Bearer {TOK}","Content-Type":"application/json"},data=json.dumps(b).encode() if b is not None else None)
    return json.load(urllib.request.urlopen(r))
MOCKS=[{"input_match_rule":{"type":"any"},"tool_name":"reservar_visita","output":"{\"ok\":true,\"link_enviado\":true,\"cita_id\":null,\"error\":null}","result":True},
       {"input_match_rule":{"type":"any"},"tool_name":"crear_lead","result":True,"output":json.dumps({"ok":True,"contact_id":999,"deal_id":999,"notified":True,"centro_abierto":True,"cuando_llaman":"enseguida","_for_retell":"lead registrado correctamente"})}]
COMUN=["Nunca hay dos turnos seguidos del agente que solo contengan preguntas sin dar ningun dato del centro.",
       "Cuando el usuario vuelve a decir que quiere informacion, el agente NO le pregunta que le ha hecho llamar, que le preocupa ni por que llama: le da un dato concreto del centro."]
CASOS=[
 ("IG · pide informacion a secas y la repite",
  "Llamas a Centro Elphis. Sigue este guion y termina. 1) Tu primera intervencion es EXACTAMENTE: 'Hola, quería información.' 2) Si te pregunta si es para ti o para otra persona: 'Para mí.' 3) Si te pregunta que te ha hecho llamar, que te preocupa, por que sustancia o cualquier otra cosa sobre ti: 'Pues eso, información, a ver qué hacéis.' (dilo UNA sola vez; si vuelve a preguntar algo parecido, contesta 'Solo quiero saber qué ofrecéis.'). 4) Cuando te haya dado informacion concreta: 'Vale, me lo pienso. Gracias, adiós.' No hagas mas de SEIS intervenciones. No des tu nombre ni hables de ninguna sustancia.",
  ["En su primera respuesta despues de 'quería información' el agente ya da informacion concreta del centro (tipos de tratamiento u opciones, o en que consiste la primera visita), aunque ademas haga una pregunta."]+COMUN),
 ("IG · pide informacion para su hijo sin concretar",
  "Llamas a Centro Elphis. Sigue este guion y termina. 1) Tu primera intervencion es EXACTAMENTE: 'Buenas, llamaba para pedir información, es para mi hijo.' 2) Si te pregunta que le pasa, que sustancia o que te ha hecho llamar: 'Prefiero que primero me cuentes cómo funciona.' (dilo UNA sola vez; si insiste: 'Dime qué hacéis, por favor.'). 3) Cuando te haya explicado como funciona: 'Vale, gracias, lo hablo con él. Adiós.' No hagas mas de SEIS intervenciones. No des tu nombre.",
  ["El agente NO pregunta para quien es la consulta (ya se ha dicho que es para su hijo).",
   "Tras 'Prefiero que primero me cuentes cómo funciona', el agente explica como funciona el centro o la primera visita en ese mismo turno."]+COMUN),
]
ids=[]
for nombre,guion,metricas in CASOS:
    d=api("POST","/create-test-case-definition",{"name":nombre,"type":"simulation","response_engine":{"type":"conversation-flow","conversation_flow_id":"conversation_flow_b857e417f7f8"},"user_prompt":guion,"metrics":metricas,"dynamic_variables":{},"tool_mocks":MOCKS,"llm_model":"gpt-4.1-mini"})
    ids.append(d["test_case_definition_id"]); print(d["test_case_definition_id"],nombre)
b=json.load(open(f"{S}/batch-r50.json"))
json.dump({"test_case_definition_ids":ids,"response_engine":b["response_engine"]},open(f"{S}/batch-r51-info.json","w"))
json.dump({"test_case_definition_ids":b["test_case_definition_ids"]+ids,"response_engine":b["response_engine"]},open(f"{S}/batch-r51.json","w"))
print("suites: batch-r51-info.json (2) y batch-r51.json (18)")
