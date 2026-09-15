#!/bin/zsh
# Tanda v51 (naturalidad: tildes + vale/claro) vs control v50. Misma suite batch-r50.json.
cd "$(dirname "$0")"
TF=conversation_flow_b857e417f7f8
for r in ${=RONDAS:-1 2 3}; do
  for rama in ctl cand; do
    [[ $rama == ctl ]] && src=snapshots/flow-PROD-v50.json || src=flow_r51_naturalidad.json
    python3 tf.py $src || { echo "TF FALLO $rama r$r"; exit 1; }
    python3 medir.py ${ETQ:-r51}-$rama-r$r batch-r50.json $TF; ec=$?
    [[ $ec -ne 0 ]] && { echo "MEDIR FALLO $rama r$r ec=$ec"; exit 1; }
  done
done
echo TANDA_OK
