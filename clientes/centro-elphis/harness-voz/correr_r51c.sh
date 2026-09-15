#!/bin/zsh
# v51c (tildes + intake "informacion a secas", sin vale/claro). Control v50 de las 16 = rondas r51-ctl;
# aqui el control solo corre los 2 casos IG nuevos. Al final, 3 rondas extra del caso de crisis fragil.
cd "$(dirname "$0")"
TF=conversation_flow_b857e417f7f8
carga(){ python3 tf.py $1 >/dev/null || { echo "TF FALLO $1"; exit 1; } }
mide(){ python3 medir.py $1 $2 $TF || { echo "MEDIR FALLO $1"; exit 1; } }
for r in 1 2; do
  carga flow_r51_naturalidad.json; mide r51c-cand-r$r batch-r51.json
  carga snapshots/flow-PROD-v50.json; mide r51c-ctlinfo-r$r batch-r51-info.json
done
carga flow_r51_naturalidad.json
for r in 1 2 3; do mide harto51c-cand-r$r batch-harto.json; done
echo TANDA_OK
