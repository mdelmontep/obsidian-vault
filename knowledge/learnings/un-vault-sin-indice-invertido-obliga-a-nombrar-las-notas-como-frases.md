---
title: un vault sin índice invertido obliga a nombrar las notas como frases — y eso deja de escalar a ~1.000
date: 2026-08-18
source: obsidian-vault
tags: [vault, obsidian, busqueda, metodo, harness, fts5]
---

# Un vault sin índice invertido obliga a nombrar las notas como frases

**Síntoma.** Los nombres de fichero de `knowledge/learnings/` promedian **59 caracteres**
(`un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro.md`). No es
manía descriptiva: es una **compensación por no tener búsqueda**. Cuando la única forma de
encontrar algo es `ls | grep`, el nombre tiene que ser el resumen entero.

**La medida que lo destapa.** Buscar por contenido en 1.605 learnings:

| término | `grep -ril` devuelve | % del corpus |
|---|---|---|
| `test` | 479 ficheros | 30 % |
| `guard` | 360 | 22 % |
| `gate` | 263 | 16 % |

Un resultado de 479 ficheros no es un resultado: es el corpus otra vez. Por eso el acceso
real medido en 4.107 transcripts era **5.996 llamadas Bash contra 1.039 Read** — casi todo
`ls`, `cat` y `grep` sobre nombres, nunca sobre contenido.

**Dónde se rompe.** El nombre-frase escala hasta ~800 notas. A 1.605 (y creciendo a
**24/día**), ya no: hay 30 notas distintas sobre «un test que no prueba lo que crees», y
ninguna lista de nombres las ordena por cuál responde a tu pregunta de ahora.

**Fix.** Índice invertido local — SQLite **FTS5**, que viene en macOS y en `node:sqlite`
desde Node 22: cero dependencias, cero API, cero tokens.

```sh
vault-find "guard que no discrimina"   # 10 rankeados, no 360
vault-dup  "titulo que voy a escribir" # ¿ya existe? antes de crear
```

Tres piezas de scoring, y **las tres hacen falta** (verificado mutando cada una contra el
gate: anular cualquiera tumba casos):

1. **Cobertura de términos**, no `OR` a secas — el `OR` premia al documento que tiene la
   palabra más rara aunque ignore el resto de la consulta.
2. **Bonus por coincidencia en el nombre** — bm25 ya pondera el slug ×10, pero al
   normalizar contra 500 documentos esa señal se diluye y la nota que se llama
   literalmente como lo que buscas queda sepultada.
3. **Penalización por tamaño** — quien busca quiere la nota atómica que responde, no el
   hub de 39.000 tokens que menciona el término 34 veces.

**La regla.** En un vault de notas atómicas, **la búsqueda es infraestructura, no una
comodidad**. Sin ella el corpus sigue creciendo y su valor recuperable se estanca: aquí,
**el 53 % de los learnings se escribió y no se volvió a consultar nunca** (749 de 1.605
aparecen en ≥2 sesiones distintas; el resto solo en la que los creó). No era pereza —
era que crear la nota 1.606 siempre salía más barato que comprobar si ya existía.

Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] ·
[[una-suite-en-verde-no-prueba-el-camino-real]]
