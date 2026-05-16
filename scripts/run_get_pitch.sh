#!/bin/bash

# Establecemos que el código de retorno de un pipeline sea el del último programa con código de retorno
# distinto de cero, o cero si todos devuelven cero.
set -o pipefail

# Put here the program (maybe with path)
GETF0="get_pitch"
POT=-46
R1NORM=0.55
RMAXNORM=0.40

for fwav in pitch_db/train/*.wav; do
    ff0=${fwav/.wav/.f0}
    echo "$GETF0 $fwav $ff0 ----"
	$GETF0 -p $POT -1 $R1NORM -M $RMAXNORM $fwav $ff0 > /dev/null || { echo -e "\nError in $GETF0 $fwav $ff0" && exit 1; } 
done

pitch_evaluate pitch_db/train/*.f0ref

exit 0
