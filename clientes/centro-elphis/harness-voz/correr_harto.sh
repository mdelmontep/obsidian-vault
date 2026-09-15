#!/bin/zsh
# Desempate del caso "CR harto de vivir asi": v50 vs v51b, rondas alternas de un solo caso.
cd "$(dirname "$0")"
TF=conversation_flow_b857e417f7f8
for r in ${=RONDAS:-1 2 3 4 5}; do
  for rama in ctl cand; do
    [[ $rama == ctl ]] && src=snapshots/flow-PROD-v50.json || src=flow_r51_naturalidad.json
    python3 tf.py $src >/dev/null || { echo "TF FALLO $rama r$r"; exit 1; }
    python3 medir.py harto51-$rama-r$r batch-harto.json $TF || { echo "MEDIR FALLO $rama r$r"; exit 1; }
  done
done
python3 tf.py flow_r51_naturalidad.json >/dev/null
echo TANDA_OK
