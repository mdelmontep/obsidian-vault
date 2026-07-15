---
title: AGH — guion de QA en llamada real (agente de voz)
date: 2026-07-15
source: https://claude.ai/code/artifact/da626c8d-ffc3-4dac-95b0-44b4167ed62c
tags: [agh, qa, voz, retell, agente]
---

Guion para probar en una **llamada real** (voz Retell) los cambios del agente entregados esta semana y verificar que funcionan. Formato por prueba: **decir** → *esperar* → ✓ **verificar**. Cubre #519 · #520/#527 · #514/#516 · #522/#524 · #511 · #482 · #485 · #452 · #118 · drill de voz #192. Versión interactiva (checkboxes + progreso, imprimible): ver `source`. Hub del proyecto: [[agh-iberica]].

**Leyenda:** ★ = #520 (corregir «lo último») · ⚠ = requiere M365 · ✓ = verificar en dashboard · ✆ = mira también WhatsApp.

## Antes de llamar (prep)
- [ ] Llamar desde un comercial **con M365 ya conectado** (uno de los 4 con `users.email` backfilleado) → prueba también self-recipient y prep de calendario.
- [ ] Abrir el **dashboard** (cartera · ficha · audit) y el **WhatsApp** ✆ de ese comercial (la voz empuja el contenido pesado ahí).
- [ ] Tener una **cita futura real** en el calendario M365 ⚠ con «Dragados» en el asunto (para el bloque F).
- [ ] Usar nombres de prueba (`Test Dragados`, `Test Endesa`) para no ensuciar datos reales.

## A · Altas · HITL · dedup (ClientIntake #451, audit #485)
- [ ] **«Apunta un cliente nuevo, Test Dragados»** → propone → «sí» → ✓ aparece en cartera + fila `create` en audit con procedencia **voz**.
- [ ] **«Apunta el cliente Test Dragados»** (otra vez) → dedup exacto: no duplica, avisa.
- [ ] **«Apunta Test Dragadoss»** (variante parecida) → dedup aproximado: pregunta si es el mismo.

## B · Reunión · recall · corrección post-confirm (★ #520)
- [ ] **«Apunta una reunión con Test Dragados: hablamos del kickoff, la próxima acción es enviarles la propuesta»** → «sí» → ✓ reunión en la ficha + tarea/hilo de la próxima acción.
- [ ] **«¿Qué hablé con Test Dragados?»** → recall: resume la reunión.
- [ ] ★ **«No, era con Test Endesa»** (justo tras confirmar) → reabre ESA reunión y propone reasignarla → «sí» → ✓ en dashboard pasa a Test Endesa.

## C · Nota suelta por voz (#522)
- [ ] **«Apúntame una nota sobre Test Dragados: han subido los precios un 10%»** → «sí» → ✓ nota en la ficha (no como reunión ni tarea).
- [ ] ★ **«No, era que bajaron los precios»** → corrige el texto de la nota.

## D · Oportunidad · anáfora · corrección (#118 L2, ★ #520)
- [ ] **«Crea una oportunidad para Test Dragados: perfiles Java, 50 mil»** → «sí».
- [ ] **«Súbela a 80 mil»** → anáfora: actualiza esa misma oportunidad sin renombrar el cliente.
- [ ] ★ **«No, eran 90 mil»** (tras confirmar) → corrige el valor.

## E · Tareas · recordatorios · temporal (#452)
- [ ] **«Apúntame llamar a Test Dragados el jueves a las 10»** → ✓ fecha/hora en Europe/Madrid correctas.
- [ ] **«Recuérdame mañana a las 9 enviar la propuesta»** → «sí».
- [ ] ★ **«No, era llamar a Test Endesa»** → corrige el título de la tarea.

## F · Prep de reunión · cita FORWARD (#514 / #519) ⚠
- [ ] **«Prepárame lo de Test Dragados»** → briefing: próxima cita futura + última reunión + oportunidades abiertas + tareas + contactos → ✓ la cita es la **FORWARD** (la del jueves), no solo la de hoy.

## G · Email · self-recipient · revisión en WhatsApp (#482) ✆
- [ ] **«Manda un correo a Test Dragados con el resumen de la reunión»** → voz: puntero corto + manda el borrador a tu WhatsApp → ✓ llega a WhatsApp.
- [ ] **«Mándamelo a mí» / «a mi correo»** ⚠ → resuelve TU propio email (no pide dirección); y un envío a terceros NO lo secuestra.

## H · Contacto (persona) · corrección (#156, ★ #520)
- [ ] **«La persona de contacto de Test Dragados es Marta, de compras, marta@test.com»** → «sí».
- [ ] ★ **«No, es directora financiera»** → corrige el cargo del contacto.

## I · Robustez de voz (drill #192)
- [ ] Responder solo **«sí»/«no»** a una propuesta (#411) → confirma/cancela bien.
- [ ] Repetir el mismo dictado en vez de responder (#436) → no ejecuta dos veces; re-propone.
- [ ] **«¿Qué clientes tengo?»** → luego **«el primero» / «los tres primeros» / «el último»** (#247/#403) ✆ → voz da puntero + WhatsApp; el subconjunto se resuelve sin re-listar en bucle.
- [ ] Forzar una petición ambigua y repetirla 2 veces igual (#511) → a la 3ª emisión escala a un **menú de capacidades**, no repite infinito.
- [ ] **«¿Qué tal?»** (#P2) → responde social, sin intentar escribir nada.

## J · Preferencias aprendidas (#P5)
- [ ] **«Mi firma de correo es: Manu, AGH Ibérica»** → guarda preferencia → manda un correo → ✓ usa la firma. ✆
- [ ] **«Por defecto agéndame las reuniones a las 9»** → **«agenda una reunión con Test Dragados el lunes»** (sin hora) → ✓ usa las 9:00. ⚠

## K · Verificación final (dashboard #485/#500, Langfuse #82)
- [ ] ✓ Cada write dejó fila en `audit_log` con procedencia **voice** (las de #520 como `update`).
- [ ] Revisar la **traza de la llamada en Langfuse** para ver el routing de cada turno.

## Caveats reales
- El **self-recipient** solo funciona con `users.email` poblado: los 4 con `entra-invite` sí; **Carlos aún no** (salvo reconectar M365).
- **Prep FORWARD** y **agendar en calendario** requieren M365 conectado en ese usuario.
- En voz, lo pesado (borradores, listas) va a **WhatsApp** → verifica ambos canales.
