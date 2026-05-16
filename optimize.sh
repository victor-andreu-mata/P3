#!/bin/bash
GETF0="get_pitch"
best_score=0
best_pot=0
best_r1=0
best_rm=0

for pot in -43 -44 -45 -46 -47; do
  for r1 in 0.50 0.52 0.55 0.57 0.60; do
    for rm in 0.35 0.37 0.40 0.42 0.45; do
      for fwav in pitch_db/train/*.wav; do
        ff0=${fwav/.wav/.f0}
        $GETF0 -p $pot -1 $r1 -M $rm $fwav $ff0 > /dev/null 2>&1
      done
      score=$(pitch_evaluate pitch_db/train/*.f0ref 2>/dev/null | grep "TOTAL" | grep -oP '\d+\.\d+(?= %)' )
      echo "pot=$pot r1=$r1 rm=$rm -> $score %"
      if [ ! -z "$score" ] && (( $(echo "$score > $best_score" | bc -l) )); then
        best_score=$score
        best_pot=$pot
        best_r1=$r1
        best_rm=$rm
      fi
    done
  done
done

echo ""
echo "=== MEJOR RESULTADO ==="
echo "pot=$best_pot r1norm=$best_r1 rmaxnorm=$best_rm -> $best_score %"