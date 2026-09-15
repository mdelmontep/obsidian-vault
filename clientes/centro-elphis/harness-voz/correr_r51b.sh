#!/bin/zsh
# v51b (vale/claro con frecuencia) solo candidato; el control v50 ya son las 3 rondas r51-ctl.
cd "$(dirname "$0")"
TF=conversation_flow_b857e417f7f8
python3 tf.py flow_r51_naturalidad.json || { echo "TF FALLO"; exit 1; }
for r in ${=RONDAS:-1 2}; do
  python3 medir.py r51b-cand-r$r batch-r50.json $TF || { echo "MEDIR FALLO r$r"; exit 1; }
done
echo TANDA_OK
