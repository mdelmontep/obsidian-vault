---
title: un test que ESCRIBE para probar una frontera verifica antes que la frontera existe
date: 2026-08-10
source: claude-code-session
tags: [testing, qa, multi-org, seguridad, metodo]
---
FacturaIA 10-ago: eje que comprobaba fugas cross-org lanzando escrituras con sesión de la
org A contra ids de la org B. Marcó **12 fugas**. Las 12 falsas: el usuario de `.env.test`
es `propietario` de **las dos** orgs sandbox, así que no cruzaba ninguna frontera —
escribía en su propia org. Una consulta a `org_members` lo habría dicho **antes** de tocar
un dato.

**El coste no fue el informe equivocado.** Al ejercer contra datos reales se archivaron 2
contactos, se desactivó un producto, se validaron 2 teléfonos, se marcó un principal
inexistente y se reasignaron cliente y fecha de cobro de 2 facturas — una quedó **sin
cliente**. Recuperable solo porque `audit_log` guardaba el estado anterior
(`cliente_id_anterior`, `de:`/`a:` de la fecha): sin eso, no había vuelta.

**Reglas:**
- La precondición de un test destructivo se comprueba con una LECTURA, y es un `beforeAll`
  que aborta, no un comentario.
- Un test de frontera con actor multi-org no mide nada: para cross-org hace falta un actor
  que **no** pertenezca a la otra parte.
- Sin frontera comprobable, **no lo dejes con `skip` en verde**: pon un caso que EXIJA la
  precondición y falle el día que se cumpla — así el hueco se cierra solo y no se olvida.
- Corolario de diseño: esto es un argumento a favor de guardar el valor ANTERIOR en el
  registro de auditoría, no solo el nuevo. Fue lo que permitió revertir.

Hermano de [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] (allí el test no muerde;
aquí muerde a quien no debe).
