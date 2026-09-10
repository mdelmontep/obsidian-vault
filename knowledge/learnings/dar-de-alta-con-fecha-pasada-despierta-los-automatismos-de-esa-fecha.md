---
title: dar de alta con fecha pasada despierta los automatismos de esa fecha
date: 2026-09-10
source: simarro
tags: [integraciones, backfill, recordatorios, kommo]
---
Un sync que importa citas de una agenda a un CRM leía una ventana de `ahora-24h` a `ahora+90d`. Las
24h hacia atrás parecían inofensivas (servían para reconocer lo ya procesado), pero también metían en
el plan **citas ya celebradas**. Al crear el lead, el CRM saludó a la clienta por una visita que
había sido una hora antes.

El automatismo no sabe que el alta llega tarde: hace la cuenta desde la fecha del registro, no desde
la fecha del alta. Una cita de anteayer importada hoy dispara el «¿qué te pareció?» de +48h mañana.

Reglas al hacer backfill contra un sistema con automatismos por fecha:
1. **Leer hacia atrás para deduplicar, planificar solo hacia delante.** Son dos ventanas distintas;
   reutilizar una para las dos cosas es el bug.
2. Lo ya creado con fecha pasada hay que desarmarlo a mano — mirar qué campo es el disparador
   (aquí `task_type_id`) y cambiarlo, no basta con marcar la tarea completada.
3. El primer write real va con límite de 1 registro y se audita entero antes de soltar el resto.

Ver [[el-inventario-de-automatismos-no-esta-solo-en-el-orquestador]] · [[recordatorios-visita-por-task-type]]
