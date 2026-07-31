---
title: una constante "típica" sin fuente contamina todo lo que se calcule encima
date: 2026-07-31
source: claude-code-session
tags: [metodo, verificacion, datos]
---

Las constantes copiadas de memoria ("la comisión típica es 0.04%", "el timeout suele ser
30s") no fallan: sesgan. Y como nada peta, el sesgo viaja a cada número derivado hasta que
alguien va a la fuente.

Caso (cryptobruj-bot): `FEE_TAKER = 0.0004` como "taker típico de futuros". La tabla oficial
del exchange dice **0.05%**. Un 25% de subestimación que hacía optimista **todo** backtest
del repo — barrido de 480 configuraciones y banco de búsqueda incluidos. Corregirlo movió la
estrategia base de −0.158R a −0.180R y tumbó varias conclusiones.

Disciplina: toda constante que entre en un cálculo lleva **fuente + fecha de verificación**
en el comentario, y vive en un único sitio.

```python
# Verificado en la tabla oficial el 2026-07-31 (<url>): taker 0.05%, maker 0.02%.
FEE_TAKER = 0.0005
```

La señal de alarma es el adjetivo: "típico", "estándar", "suele ser", "aproximadamente".
Si está ahí, nadie lo comprobó.
