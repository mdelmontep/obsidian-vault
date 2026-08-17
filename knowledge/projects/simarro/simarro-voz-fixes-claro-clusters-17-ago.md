---
title: Simarro — fix guard teléfono, "Claro" parado, clústeres de zona y bugs de rebote (17-ago)
date: 2026-08-17
source: claude-code-session
tags: [simarro, retell, n8n, kommo, voz]
---

# Contexto

Sesión de seguimiento a los fixes del 13-ago (chatbot WA + preferencias). Arrancó con una llamada
real donde el cliente reportó: (1) confusión entre "nombre" y "teléfono" al reservar por voz — el
WhatsApp de confirmación nunca llegó, (2) el agente se quedaba parado tras decir "Claro." hasta
que el cliente insistía, (3) con la tele puesta, el agente se cortaba y volvía a saludar varias
veces. Cada punto se investigó con evidencia (transcripción real de Retell + ejecuciones n8n +
estado real en Kommo), no se asumió nada.

# 1. Guard de teléfono en `Edit Fields3` (`iMoTKZWxYLymGuHF`) — endurecido

El guard existente (de mayo) solo descartaba el placeholder viejo sin sustituir
(`"+34{{from_number}}"`, detectado por contener `{`). El modelo, en la llamada real de hoy, puso
literalmente el nombre del cliente en el campo teléfono (`"phone":"nombre de prueba, dos"`) — no
contenía `{` ni `from_number`, así que el guard lo dejó pasar. Llegó hasta Kommo (contacto real
con teléfono `+34nombredeprueba,dos`) y el salesbot de confirmación falló.

**Fix**: el guard ahora valida que el valor tenga PINTA de teléfono real (solo dígitos/+/espacios/
guiones/paréntesis, entre 9 y 15 dígitos) en vez de solo excluir el patrón conocido. Subsume el
caso viejo (el placeholder con `{}` no pasa el regex tampoco) y cubre cualquier otra basura no
numérica. Probado offline con 11 casos antes de tocar producción, y confirmado end-to-end con un
lead de prueba real (`34951946`, contacto `39121946`): teléfono quedó `+34617314938`, correcto.

Efecto colateral bueno: `Get list of contacts1` busca el contacto existente por este mismo campo
— con basura, nunca encontraba al contacto real y creaba uno duplicado cada vez.

# 2. "Claro." + transición en el mismo turno — causa raíz oficial, fix aplicado

Reincidencia del bug ya conocido de mayo/junio, esta vez confirmada con la documentación y
soporte oficiales de Retell (ver [[Stack/retell/conversation-flow-outbound-gotchas]] punto 5):
los edges tipo "prompt" solo se evalúan tras un turno NUEVO del usuario, nunca justo tras la
propia frase del agente. Un nodo que dice "Claro." y pretende transicionar "en el mismo turno" se
queda sin ningún disparador hasta que el cliente dice cualquier cosa.

**Fix entrada** (`conversation_flow_19ca70e19b3f`, v23→v24): nuevo edge directo desde `n_start` a
`n_buscar` cuando el cliente ya da un criterio en su primer mensaje — salta `n_brief_comprador`
entero en el caso más común (justo el de la llamada real de hoy). `n_brief_comprador` se
simplificó (1916→1129 caracteres) y ahora solo maneja el caso "sin ningún criterio", donde
preguntar y esperar SÍ es el patrón sano (la transición reacciona a un turno real del cliente).

**Fix salida** (`conversation_flow_29839e6fd152`, v0→v1): `n_descubrir` es multi-turno por
diseño, no hay un "nodo anterior" limpio al que saltar — se aplicó solo la mitigación oficial de
Retell (acortar/simplificar la instrucción, quitar el paso de "elegir palabra de acuse").

Confirmado con 2 llamadas reales de prueba tras el fix: la segunda pasó de "el presupuesto son
cuatrocientos mil," directo a "Perfecto, pues busco ahora mismo viviendas..." sin ninguna pausa,
encadenado en la misma respuesta.

# 3. Ruido de fondo — denoising_mode ausente en el agente de salida

`agent_042b9fbc990838ae4117315440` (Ana Outbound) no tenía `denoising_mode` configurado (`None`),
mientras que el de entrada sí (`noise-cancellation`). Con la tele puesta, esto causó cortes
repetidos a media frase y reinicios completos del saludo (3 intentos de la misma frase de
presentación en una sola llamada). Igualado al valor del agente de entrada. No se pudo confirmar
al 100% en una prueba controlada (sin ruido de fondo real para repetir el test).

# 4. Clústeres de proximidad geográfica — feature nueva

El cliente preguntó si decir "Majadahonda" ofrece automáticamente Las Rozas/Pozuelo/Boadilla.
Investigado el código real de búsqueda (`Buscar_viviendas_catalogo`, nodo `Router`): el
`ZONE_FIX` existente es solo corrección ortográfica ASR (variantes mal transcritas → nombre
correcto del MISMO sitio), no proximidad geográfica. El filtro real es texto exacto contra la
población pedida.

**Descubierto de paso**: ya existía un intento de esto en `Build Zones` — un único clúster plano
mezclando núcleo (Majadahonda/Las Rozas/Pozuelo/Boadilla) con Madrid capital, sin la sierra
(Collado Villalba/San Lorenzo/Guadarrama) en absoluto. Decisión con el cliente: sustituido por 2
clústeres comerciales reales, sin mezclarse entre sí y sin Madrid capital:
- **Núcleo NO Madrid**: Majadahonda, Las Rozas, Pozuelo de Alarcón, Boadilla del Monte.
- **Sierra NO Madrid**: Collado Villalba, San Lorenzo de El Escorial, Guadarrama, Villaviciosa de
  Odón.

Sin coordenadas reales (no hay lat/lng en `properties`) — geocodificar ~10 pueblos fijos para un
km "real" era desproporcionado; agrupación comercial a mano, cero mantenimiento, ampliable con un
clúster nuevo el día que Simarro tenga cartera en otra región de España.

Verificado con 4 casos reales contra el catálogo real (precios reales, no simulados): Majadahonda
≤900k sugiere Boadilla (núcleo); Guadarrama 316-400k sugiere San Lorenzo + Collado Villalba
(sierra); Majadahonda ≤350k no sugiere nada aunque la sierra sí tenga algo a ese precio (sin
mezclar clústeres); Montuiri nunca inventa vecinos.

## Bug de rebote: el mensaje con la sugerencia nunca llegaba a la llamada

`Format For Voice` (en el wrapper `Voz_buscar_viviendas`, no en `Buscar_viviendas_catalogo`)
tenía un `if (!found)` que SIEMPRE devolvía un mensaje genérico fijo, ignorando por completo los
campos `zones`/`message` que el sub-workflow ya calculaba bien — tanto con la lógica vieja como
con la nueva. Bug preexistente, no introducido hoy. Ver [[Stack/n8n]] (nueva entrada: "nodo con
lógica correcta pero sin conexión de salida"). Corregido: si `zones.length > 0`, usa el mensaje
enriquecido; si no, cae al genérico de siempre. Confirmado con los mismos 4 casos, ahora sí
reflejados en la respuesta real del webhook de voz.

# 5. Zona rechazada no debe capturarse como interés

Efecto colateral de la función nueva: ahora Ana puede proponer por su cuenta una zona que el
cliente no pidió. Si el cliente la rechaza, los campos de análisis post-llamada (`zona_interes`
en entrada, `perfil_zona` en salida) decían "tal como lo dijo" sin distinguir propuesta-rechazada
de interés real — riesgo de que esa zona quedara guardada en Kommo y el matching semanal
insistiera con algo ya descartado. Añadida instrucción explícita en los dos campos (agentes v25 y
v2 respectivamente) para excluir zonas propuestas por el agente y rechazadas por el cliente. Sin
validar aún con una llamada real que dispare ese caso concreto — se confirma en la próxima que
pase.

# 6. Clústeres ampliados a toda la Comunidad de Madrid (mismo día, segunda vuelta)

Tras validar los 2 clústeres iniciales, pregunta directa del cliente vía Manu: "¿y si dice un
pueblo de otro lado, Alcalá de Henares, o Benidorm en Alicante?". Aclarado el alcance real
("actualiza la lista con todo Madrid", confirmado que cubre TANTO el diccionario de reconocimiento
ASR como los clústeres de cercanía): ampliar a la Comunidad de Madrid entera, resto de España sigue
sin clúster (solo coincidencia exacta, sin inventar vecinos).

**Fuente**: los 179 municipios oficiales / 9 comarcas de la Comunidad de Madrid (Wikipedia,
recuento verificado 179/179 antes de tocar código). Reestructurados en **12 clústeres comerciales**
partiendo la comarca oficial "Área Metropolitana y Corredor del Henares" en 4 subzonas
(noroeste/henares/sur/norte metropolitano) — la comarca oficial mezclaba puntas opuestas de Madrid
(ej. Boadilla y Alcalá de Henares) bajo una sola etiqueta, inútil para "cercanía" real de comprador.

**Corrección de paso**: Villaviciosa de Odón estaba mal en el clúster "sierra" desde el diseño de
hoy (§4) — la fuente oficial la sitúa en el área metropolitana noroeste, junto a Boadilla. Verificado
en vivo: Boadilla + presupuesto 500-650k ahora sugiere Villaviciosa, cosa que no hacía antes.

**2 nodos tocados** en `Buscar_viviendas_catalogo` (`5NRXALN9lBVE9fTs`):
- `Router` → `fixZone()`: los ~25 patrones `ZONE_FIX` existentes (correcciones de ASR reales,
  validadas con llamadas de clientes) se dejan intactos; se añade un fallback nuevo, un lookup
  plano de los 179 municipios (nombre correcto, con o sin acentos → forma canónica de la BD). No
  intenta adivinar variantes de mala transcripción para pueblos sin historial de llamadas — si
  aparece un caso real de ASR roto en un municipio nuevo, se añade como patrón `ZONE_FIX`, igual
  que los 25 ya existentes.
- `Build Zones`: los 2 clústeres antiguos sustituidos por los 12 nuevos.

**Mensaje "fuera de zona" (nuevo, mismo commit)**: si el pueblo pedido no aparece ni en coincidencia
exacta ni en ningún clúster con cartera activa (ej. Alcalá de Henares, Benidorm), la respuesta ya no
es el genérico "no tengo con esos criterios, ¿ampliamos?" (que sugiere que insistiendo puede
aparecer algo) sino un aviso honesto de que Simarro no opera ahí. Distinción clave: "el pueblo se
reconoce" (ahora toda Madrid) ≠ "Simarro tiene cartera ahí" (sigue siendo solo ~10 poblaciones) — la
búsqueda nunca debe confundir ambas cosas.

**Bug de rebote, 2ª vuelta**: el primer fix de `Format For Voice` (§4) condicionaba usar
`item.message` a `zones.length > 0` — correcto para "hay vecinos con algo", pero el caso nuevo
"fuera de zona" no tiene vecinos que listar y aun así trae un mensaje válido. Detectado probando en
vivo Benidorm/Alcalá y viendo que seguía saliendo el genérico. Fix: confiar siempre en
`item.message` cuando está presente, sin condicionarlo — `Build Zones` ya calcula el mensaje
correcto en las 4 variantes (vecinos, fuera de zona, passthrough, sin criterio). Lección: un gate
que depende de una señal correlacionada con el caso viejo se rompe en cuanto aparece un caso nuevo
legítimo sin esa señal.

Verificado con 5 casos reales adicionales contra el catálogo real: Alcorcón (reconocido, fuera de
zona por falta de cartera), Boadilla 500-650k (ahora sugiere Villaviciosa — antes no), Majadahonda
≤900k (regresión: sigue igual, ahora Boadilla+Villaviciosa en vez de solo un pueblo), Guadarrama
316-400k (regresión: sin cambios, San Lorenzo + Collado Villalba), Alcalá de Henares (fuera de
zona, mensaje nuevo).

# 7. Precio antes/después visual — investigado, aplazado

Petición de Dani en su lista de 8 puntos: mostrar de forma visual cuando un piso baja de precio
(ej. 300.000€ → 290.000€). Investigado antes de prometer nada:
- `properties_price_history` **existe** en Supabase (creada en la DDL original de `properties`,
  workflow `Y2BqlEDl51KyqVmT`) pero `Sync_catalogo_idealista` nunca escribe en ella — 0 histórico
  real capturado hasta hoy.
- El badge `highlight: "rebajado"` en `simarro_web` (`PropertyCard.astro`) es **puramente
  decorativo** — texto fijo, sin comparar precio actual contra ninguno anterior. La fuente real de
  datos (`properties-source.ts`, feed de Idealista vía Supabase) nunca calcula ni asigna ese campo.
- Implementarlo de verdad exige: (1) que el sync empiece a escribir en `properties_price_history`
  cada vez que el precio cambia, (2) tocar el schema/tipo `Property` (sin campo `previousPrice` hoy),
  (3) cambios en el repo **aparte** `simarro_web` (Astro, GitHub `AgentesIA-MAdrid/simarro_web`).

Presentado el alcance real al usuario (toca BD de producción + un segundo repo) — **aplazado
explícitamente**: "de momento lo dejamos así ahora". No construir sin que se pida de nuevo.

# Pendiente

- Confirmar en llamada real (no sintética) que la regla de "zona rechazada" funciona.
- Limpieza en Kommo UI: leads de test `34951382` (TEST E2E Phone Guard), `34951644`/`34951946`
  (TEST E2E/E2E Outbound), sumados a la lista ya existente en el hub.
- Corregir la afirmación desactualizada del hub ("lanzador `2LqwDgLecHwjgIQl` INACTIVO") — está
  activo, verificado hoy; el bloqueante real sigue siendo el consentimiento (0 leads marcados).
- Precio antes/después: retomar solo si el usuario lo repide explícitamente (ver §7).
