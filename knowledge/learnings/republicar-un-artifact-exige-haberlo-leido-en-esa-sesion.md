---
title: republicar un artifact exige haberlo leído EN ESA sesión, y `updated` del listado no dice el contenido
date: 2026-09-21
source: agentesia-crm · agh-iberica
tags: [claude-code, artifacts, coste-contexto]
---
Dos cosas distintas, y confundirlas es lo que hace que una URL de tablero cambie cada pocas sesiones:

1. **La lectura previa es POR SESIÓN.** El tool rechaza pisar un artifact que *esta* sesión no ha
   leído. Una sesión anterior concluyó «lo que pide es la dirección, no la lectura» — era cierto
   sólo porque ya lo había leído. Un tablero de 290 KB son ~72k tokens en el hilo principal.
2. **`updated` en `action:"list"` es la fecha del REGISTRO, no la del contenido.** Un artifact salía
   «actualizado hoy» y su contenido era de diez iteraciones antes. Fiarse del listado es una forma
   nueva de republicar contra un tablero muerto sin que se note.

3. **Un `/login` a mitad de sesión cambia la CUENTA y el artifact pasa a ser ajeno** (21-sep-2026):
   el `publish` se deniega con *«could not verify the target page is not a review page»* —que no
   habla de identidad— y el `read` ya no devuelve HTML sino un **resumen marcado como contenido de
   terceros**. Antes falla, en silencio, el aviso de que se cerraron los watches. No reintentar ni
   publicar copia nueva: fragmenta el tablero. Volver a la cuenta que lo publicó.

**Antes de pagar los 72k, medir si renunciar cuesta algo**: `diff <(sort publicado) <(sort local)` y
mirar sólo las líneas `<`. Si son el envoltorio de la plataforma y valores ya superados, no hay nada
que fusionar —un documento REGENERADO no tiene ediciones propias— y publicar nuevo sale gratis.
Ver [[artifact-publicar-sin-leer-lo-que-se-pisa]].
