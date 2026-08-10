---
title: estado cargado por effect usado como precondición de una escritura descarta el gesto del usuario
date: 2026-08-11
source: claude-code-session
tags: [react, carreras, ux, patron-bug]
---
Patrón, con dos extremos y los dos silenciosos (issue #1595 de TuFacturaIA):

```tsx
const [rec, setRec] = useState(null)          // lo llena un effect asíncrono
useEffect(() => { ... setRec(await fetch()) }, [id])

async function onSave(v) {
  const id = rec?.id                          // ← null MIENTRAS CARGA
  if (!id) return toast('No encontramos el registro')   // mentira: existe
  ...
}
```

`null` de «aún no ha cargado» es **indistinguible** de `null` de «no existe». Quien
escribe dentro de esa ventana pierde el dato y recibe un error falso. Y por el otro
extremo: la lectura en vuelo aterriza **después** del PATCH y pisa lo recién
guardado — el usuario ve su valor revertirse con la BD ya correcta.

Los dos arreglos van juntos: **la escritura resuelve el id por su cuenta** (casi
siempre ya está en memoria, sin ir a red) y **la lectura en vuelo se invalida al
guardar** (`const gen = ++ref.current` en el effect; `ref.current++` tras escribir;
`if (ref.current !== gen) return` antes de `setState`). Un `cancelado` de cleanup no
basta: solo cubre el cambio de dependencias, no la escritura.

Olor a este bug: un test de UI que falla ~2 de cada 3 veces y «va bien aislado».
Ver [[al-provocar-una-carrera-con-page-route-retrasa-la-entrega-no-el-envio]].
