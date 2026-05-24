---
title: Reglas aprendidas de confirmación manual — cierre del loop de aprendizaje
date: 2026-05-24
source: FacturaIA mig 155 + Sprint C conciliación v3
tags: [facturaia, learning-loops, ux, matching]
---

# Reglas aprendidas de confirmación manual

Cuando un sistema de matching automatizado se queda corto en un caso real, lo natural es bajar el umbral para que pille más cosas — y eso introduce falsos positivos. La alternativa: dejar que el USUARIO complete la información que al sistema le falta, **una sola vez por patrón**, y aplicarla automáticamente desde entonces.

## El patrón

1. Usuario confirma manualmente un match con score bajo (el sistema decía "posible" o "probable", no automatizó).
2. El sistema le ofrece: *"Esto que has confirmado, ¿quieres que lo recuerde para futuras veces?"*
3. Extrae los candidatos legibles de la información que sí tiene (descripción del movimiento bancario en este caso) y deja que el usuario elija el token correcto.
4. Guarda como regla: `(org, contraparte_id, patron_token) → veces_confirmada=1`.
5. La próxima vez que aparezca un movimiento con ese token en la descripción y el cliente/proveedor matchee, suma +30 al score automáticamente, lo que sube la confianza a "segura" y auto-confirma.

## Por qué funciona mejor que bajar el umbral

- **Score multi-señal**: la regla aprendida es UNA señal de muchas. No sustituye al importe ni a la fecha. Solo añade información.
- **Específica por contraparte**: el patrón "GESTORÍA X" puede ser correcto para Pepito SL pero ambiguo si también factura a María SL. El sistema detecta esa ambigüedad (mismo patrón → 2+ contrapartes) y marca la regla como `es_ambigua = true`, dejando de aplicarla.
- **Audit del aprendizaje**: el usuario sabe qué patrones ha enseñado. Si uno deja de ser correcto (cambia la gestoría, cambia el concepto del banco), puede borrarlo.

## Anti-pattern: aprendizaje implícito sin consentimiento

Algunos sistemas tipo "machine learning" guardan patrones sin pedir permiso — *"hemos visto que sueles aceptar matches con X, así que ya los confirmamos solos"*. Problema: el usuario no sabe qué ha "enseñado" y no puede corregir. Cuando el sistema empieza a equivocarse, no hay forma de auditar el origen.

El opt-in explícito ("¿guardar esta coincidencia?") con elección del token es 10× mejor UX que el implícito. La fricción de 1 click vale por años de confianza.

## Detalles de implementación que importan

- **Token normalizado**: lowercase, sin acentos, alfanumérico. Permite matchear "PEPITO-SL" con "pepito sl" sin sufrir variaciones cosméticas del banco.
- **Mínimo 4 chars**: tokens cortos ("LA", "SL", "DE") son ruidosos. No se aceptan.
- **No solo dígitos**: descartar tokens tipo "12345678" (que pueden ser IDs aleatorios del banco, no del cliente).
- **UPSERT con counter**: si el usuario confirma el mismo patrón 3 veces, incrementar `veces_confirmada`. Útil para UI futura tipo "patrones de alta confianza".
- **Trigger de ambigüedad**: cuando se inserta una regla con patrón ya existente para otra contraparte, marcar ambas como `es_ambigua = true`. No suman score hasta desambiguar.

## Conexión

Va con [[conciliacion-multi-señal-vs-importe-bruto-falsos-positivos]] — el sistema multi-señal es el lienzo, las reglas son la pincelada del usuario.
