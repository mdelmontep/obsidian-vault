---
title: un aviso que explica toda anomalía como ruido esconde lo deliberado
date: 2026-09-13
source: centro-elphis
tags: [alerting, guardianes, n8n, despliegue]
---
`guard-retell-pin` (T3) vigila versiones del agente de voz por encima del pin y avisa con este
texto fijo: *«Informativo, no hay nada que hacer: son autoguardados del editor»*. El 13-sep había
arriba un candidato ya verificado esperando despliegue — no un autoguardado. El aviso lo presentó
como ruido y además **se silencia 7 días mientras el conjunto no cambie**, así que el recordatorio
de la entrega pendiente desaparecía una semana.

El fallo no es detectar de más: es que el texto **afirma la causa** cuando el chequeo solo observa
el síntoma (existe versión > pin). Un aviso que no puede distinguir «ruido del editor» de «entrega
en cola» no debe escribir ninguna de las dos.

Patrón: en la plantilla de un aviso, la conclusión («no hay nada que hacer») solo puede ser tan
fuerte como lo que el check mide. Si hay varias causas posibles, **enumerarlas** y decir cuál se
distingue mirando qué. Y el auto-silencio largo es más peligroso cuanto más tranquilizador es el
texto: silencia también el caso que sí requería acción.

Ver [[elphis-guard-retell-pin]] · [[aviso-de-modulo-sin-gatear-por-feature-es-ruido-con-pinta-de-error]]
