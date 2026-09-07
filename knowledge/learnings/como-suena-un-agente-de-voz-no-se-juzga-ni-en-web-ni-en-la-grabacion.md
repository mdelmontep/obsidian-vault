---
title: cómo suena un agente de voz no se juzga ni en llamada web ni en la grabación
date: 2026-09-07
source: elphis-psicologia
tags: [retell, agentes-voz, medicion, audio]
---
Dos trampas medidas con la **primera llamada telefónica real** de un agente que llevaba tres
semanas «ajustado» en pruebas web.

1. **La prueba web es banda ancha.** Los ajustes de voz salieron de `web_call`; la línea es
   G.711 de 8 kHz. Separando los canales de la grabación: el canal del llamante muere a
   3,4 kHz (−72 dB) y es silencio digital (−91 dB) por encima de 6 kHz. Una conclusión sacada
   en web **no se transfiere** al teléfono, y la pata de salida es el mismo tubo.
2. **La grabación no lleva el `ambient_sound`.** Entre frases el canal del agente está a
   −91,0 dB, silencio absoluto: el ruido de fondo que oye quien llama **no está en el fichero**.
   Juzgar ese campo por la grabación es imposible; hay que llamar.

Medir bandas sin numpy: `ffmpeg -i ch.wav -af "highpass=f=LO,lowpass=f=HI,volumedetect" -f null -`
y leer `mean_volume`. **Necesita `-v info`**: con `-v error` el resumen de `volumedetect` no se
imprime y el script devuelve vacío pareciendo que no hay señal.

Ver [[copiar-la-config-de-un-agente-vivo-copia-una-version-que-sigue-moviendose]]
