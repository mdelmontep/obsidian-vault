import json, subprocess, urllib.request, datetime
key = subprocess.run(["opsa","read","op://qyjirginrmbgq7yeryhzjeaunu/zlc3safbuuxyrxlpcum5vcpdea/credential"],capture_output=True,text=True).stdout.strip()
nums = {"+34910052164":("AGH","agent_b219606dd26c8acadd91168aca"),"+34910054813":("EcoBox","agent_250ae0d683b8086fdcaaed9027"),"+34910059223":("Elphis Psico","agent_e1bcfd03c86219bf10e002d26f"),"+34910052668":("Admicom","agent_befaed76ddc7124b4f9d69d03d"),"+34910054675":("Simarro","agent_0df7f123e7e3c24d99c9152358"),"+34910054950":("Elphis","agent_e21120298343bc2ef8b4a535c9")}
since = int(datetime.datetime(2026,10,12,22,10,tzinfo=datetime.UTC).timestamp()*1000)
for n,(name,a) in nums.items():
    r = urllib.request.Request("https://api.retellai.com/v3/list-calls", data=json.dumps({"filter_criteria":{"agent":[{"agent_id":a}],"start_timestamp":{"type":"number","op":"ge","value":since}},"limit":5,"sort_order":"descending"}).encode(), headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    items = [c for c in json.load(urllib.request.urlopen(r))["items"] if c.get("to_number")==n]
    if not items: print(f"{name:13} {n}  sin llamadas desde la migración"); continue
    for c in items[:2]:
        h = c.get("custom_sip_headers") or {}
        ts = datetime.datetime.fromtimestamp(c["start_timestamp"]/1000, datetime.UTC).strftime("%H:%M:%S")
        via = "LIVEKIT (vieja)" if any(k.startswith("x-lk") for k in h) else "sip.retellai.com"
        print(f"{name:13} {n}  {ts} UTC  {c.get('call_status')}  {round((c.get('duration_ms') or 0)/1000)}s  vía {via}  {c['call_id']}")
