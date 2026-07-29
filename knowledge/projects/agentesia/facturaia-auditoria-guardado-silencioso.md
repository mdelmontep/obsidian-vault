---
title: facturaia — auditoría de guardado silencioso (super prompt)
date: 2026-07-29
source: claude-code-session
tags: [facturaia, auditoria, calidad, prompt]
---

Prompt listo para lanzar en **sesión fresca**. Nace del ticket #104 (Chivite): un campo que mostraba
`dd/mm/aaaa` y guardaba ISO descartaba la edición con un `return` mudo. La pregunta es dónde más pasa.
Contexto del bug → [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]] · [[facturaia]]

Pendiente de lanzar a 2026-07-29. No arregla nada: es inventario + juicio, el plan de arreglo se acuerda después.

---

```
Auditoría de robustez de TuFacturaIA — "lo que el usuario cree que guardó, ¿se guardó?"

CONTEXTO (el bug que la motiva)
Ticket #104 (Pescados Chivite, factura 10422P de DAORO). En el panel de revisión de /ingesta la fila
"Fecha emisión" PINTABA la fecha en dd/mm/aaaa (fmtDate) pero se editaba con un <input type="text">
libre cuyo guardado solo aceptaba ISO:

    if (dateFields.has(field)) {
      if (rawValue && !/^\d{4}-\d{2}-\d{2}$/.test(rawValue)) return   // descarte SILENCIOSO
    }

El usuario tecleó "23/06/2026" (el formato que veía), el guardado hizo `return` sin toast ni error,
datos_extraidos se quedó con la fecha del OCR y la factura se aprobó con ella. Verificado en prod:
ni facturas.fecha ni datos_extraidos->>'fecha' registraron el intento. Y tras aprobar no había ninguna
vía para corregirlo. Arreglado en el PR #1349 (DatePicker compartido + el guard deja de tragarse el valor).

OBJETIVO
Encontrar TODAS las demás instancias de esa familia de fallo, no solo del mismo campo. La familia:

  F1. Descarte silencioso — un handler hace `return` / `catch {}` / ignora un error de Supabase o un
      !res.ok sin decírselo al usuario, y el dato no se guarda.
  F2. Formato mostrado ≠ formato aceptado — se pinta dd/mm/aaaa, %, €, miles con coma… y el parser
      exige otra cosa. Incluye numericFields con `if (isNaN(num)) return`.
  F3. Falso éxito — se pinta "Guardado"/optimista y el write falló, no llegó, o el UPDATE afectó 0
      filas por RLS (PostgREST NO devuelve error en ese caso).
  F4. Control nativo o bespoke donde hay componente compartido (CLAUDE.md §Inviolables Frontend):
      <input type="date">, <input type="checkbox">, <select>, .tab/.subTab a mano, overlay propio…
  F5. Campo editable que no persiste donde el usuario cree — se escribe en un JSONB espejo
      (datos_extraidos) y no en la tabla owner, o al revés, y el otro camino lo pisa.
  F6. Callejón sin salida — el dato queda mal y la UI no ofrece forma de corregirlo.

MÉTODO — agentes en paralelo, un dominio cada uno
Lanza los máximos agentes que el harness permita. Reparto de modelos (~/.claude/CLAUDE.md): Fable
planea el reparto · Sonnet barre código (maker) · Haiku lo mecánico y de volumen · Opus JUZGA cada
hallazgo (real vs falso positivo). El juicio de evidencia nunca al modelo más débil. Filtra: ~50% son
falsos positivos.

Un agente por dominio, ruta absoluta + scope + qué NO entra:
  ingesta/bandeja · recibidas · emitidas y /generar · presupuestos · clientes y contactos · obras y
  partes · conciliación bancaria · cobros y remesas · inventario · fiscal y declaraciones · settings
  y onboarding · copiloto y WhatsApp

Cada hallazgo: ruta:línea, familia (F1-F6), gesto de usuario que lo dispara, qué cree el usuario que
pasó, qué pasó de verdad, severidad (pierde dato fiscal > pierde dato > solo confunde).

VERIFICACIÓN — obligatoria, con navegador
Nada se reporta como confirmado sin conducir la UI. agent-browser (perfil `fia`: `agent-browser auth
login fia`, NO `--session/--restore`) o Playwright contra localhost:3001 con "TuFacturaIA E2E principal
— .env.test" (1Password, vault FacturAIA). Un curl con 200 o una fila correcta en Postgres NO valen.
Para cada hallazgo severo: reproducir el gesto y comprobar en BD si el dato quedó o no.

REGLAS DURAS
- SOLO la org sandbox is_test=true (E2E_ORG_NAME="FacturaIA Sandbox"). Nunca escribir en org de cliente.
- Lee CLAUDE.md, AGENTS.md y el gotchas.md del área ANTES de proponer nada: Read explícito.
- No arreglar nada todavía. Inventario + juicio; el plan de arreglo se acuerda después, priorizado.
- Cero refactors, cero features.

ENTREGABLE
1. Tabla priorizada de hallazgos CONFIRMADOS con su evidencia de navegador.
2. Los descartados y por qué.
3. Arreglo agrupado por PATRÓN, no por fichero: dónde un cambio en un componente compartido mata N
   instancias (como type:'date' en EsencialList mató 2).
4. Qué merece hook o test de regresión permanente (p. ej. lint rule contra <input type="date">/<select>
   nativos, o test que exija feedback en toda rama de error de guardado).
5. Escríbelo en docs/architecture/auditoria-guardado-silencioso.md y resúmelo en 15 líneas.
```
