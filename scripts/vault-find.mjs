#!/usr/bin/env node
/**
 * Búsqueda en el vault — FTS5 con ranking bm25, cero tokens, cero API.
 *
 *   vault-find "guard que no discrimina"      # top 10 con score y contexto
 *   vault-find -n 5 --carpeta learnings rls   # acotar
 *   vault-find --tag supabase migracion       # filtrar por tag
 *   vault-find --cat "worktree symlink"       # imprime el top-1 entero
 *   vault-find --paths "worktree"             # solo rutas (para pipe a cat)
 *
 * Sustituye a `grep -ril` sobre knowledge/: un grep de "test" devuelve 479
 * ficheros (30% del corpus); esto devuelve los 10 que importan, ordenados.
 */
import { DatabaseSync } from 'node:sqlite'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { execFileSync } from 'node:child_process'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DB_PATH = join(VAULT, '.vault-index.db')

// Palabras que en un vault en español aparecen en casi toda nota: no discriminan
// y ensucian el ranking. Se quitan de la consulta, nunca del índice.
const VACIAS = new Set(`a al algo ante antes aqui asi aun aunque cada como con contra cual cuando de
del desde donde dos el ella ellas ello ellos en entre era eran es esa ese eso esta estan este esto
ha han hace hacer hasta hay la las le les lo los mas me mi mientras muy no nos o os para pero poco
por porque que se sea segun ser si sin sobre solo son su sus tan te tiene todo todos tras un una
uno unos vez y ya`.split(/\s+/))

const argv = process.argv.slice(2)
const opt = (n, def) => { const i = argv.indexOf(n); return i === -1 ? def : argv.splice(i, 2)[1] }
const flag = (n) => { const i = argv.indexOf(n); if (i === -1) return false; argv.splice(i, 1); return true }

const N = Number(opt('-n', opt('--num', 10)))
const CARPETA = opt('--carpeta', null)
const TAG = opt('--tag', null)
const CAT = flag('--cat')
const DUP = flag('--dup')
const SOLO_PATHS = flag('--paths')
const consulta = argv.join(' ').trim()

if (!consulta) {
  console.error('uso: vault-find [-n 10] [--carpeta learnings] [--tag supabase] [--cat|--paths] "consulta"')
  process.exit(2)
}

// El índice se mantiene solo: si algo cambió en disco, reindexa antes de buscar.
//
// Su salida va SIEMPRE a stderr, nunca a stdout. En una máquina nueva el índice
// no existe y hay que construirlo, y con `stdio: 'inherit'` ese "indexadas 1805
// notas" caía en stdout: un `vault-find --paths X | xargs cat` intentaba abrir un
// fichero llamado "indexadas". stdout es el resultado; el progreso es stderr.
const reindex = execFileSync('node', [join(VAULT, 'scripts/vault-index.mjs')], { encoding: 'utf8' })
if (reindex && !reindex.startsWith('índice al día')) process.stderr.write(reindex)

const db = new DatabaseSync(DB_PATH, { readOnly: true })

/** Frase entre comillas → literal. El resto → términos con prefijo, unidos por OR. */
function construirMatch(q) {
  const frases = [...q.matchAll(/"([^"]+)"/g)].map((m) => `"${m[1]}"`)
  const sueltos = q.replace(/"[^"]*"/g, ' ')
    .toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .split(/[^a-z0-9ñ]+/).filter((t) => t.length > 2 && !VACIAS.has(t))
  // Prefijo: "migracion" casa "migraciones", "guard" casa "guards".
  const terminos = [...frases, ...sueltos.map((t) => `${t}*`)]
  if (!terminos.length) throw new Error('la consulta se queda vacía tras quitar palabras huecas')
  return terminos
}

let terminos
try { terminos = construirMatch(consulta) } catch (e) { console.error(e.message); process.exit(2) }

// Scoring propio en dos partes, porque ni AND ni OR solos sirven:
//   · AND exige que coexistan todos los términos → devuelve 0 demasiado a menudo.
//   · OR premia al documento con el término más raro aunque ignore el resto.
// Aquí se puntúa cada término por separado y se PREMIA LA COBERTURA: un
// documento que casa 2 de 2 términos gana a uno que casa 1 de 2 clavadísimo.
// bm25 pondera slug 10x, título 8x, tags 5x sobre el cuerpo — en este vault el
// nombre-frase del fichero es la señal más fuerte que existe.
const filtros = []
const paramsFiltro = []
if (CARPETA) { filtros.push('n.carpeta LIKE ?'); paramsFiltro.push(`%${CARPETA}%`) }
if (TAG) { filtros.push('n.tags LIKE ?'); paramsFiltro.push(`%${TAG}%`) }

const sql = `
  SELECT n.path, n.titulo, n.tags, n.fecha, n.bytes,
         bm25(fts, 10.0, 8.0, 5.0, 1.0) AS score,
         snippet(fts, 3, '«', '»', ' … ', 14) AS ctx
  FROM fts JOIN notas n ON n.rowid = fts.rowid
  WHERE fts MATCH ? ${filtros.length ? 'AND ' + filtros.join(' AND ') : ''}
  ORDER BY score LIMIT 2000
`
const stmt = db.prepare(sql)
const acum = new Map()

for (const t of terminos) {
  let hits
  try { hits = stmt.all(t, ...paramsFiltro) } catch { continue }
  if (!hits.length) continue
  // bm25 es negativo y sin escala fija: normalizar por término para poder sumar.
  const mejor = hits[0].score, peor = hits[hits.length - 1].score
  const rango = (peor - mejor) || 1
  for (const h of hits) {
    const norm = (peor - h.score) / rango           // 1 = el mejor de este término
    const prev = acum.get(h.path) || { ...h, suma: 0, cobertura: 0, ctxs: [] }
    prev.suma += norm
    prev.cobertura += 1
    if (h.ctx && prev.ctxs.length < 2) prev.ctxs.push(h.ctx)
    acum.set(h.path, prev)
  }
}

// Bonus por coincidencia en el NOMBRE. bm25 ya pondera el slug x10, pero al
// normalizar contra 500 documentos esa señal se diluye: la nota que se llama
// literalmente como lo que buscas quedaba sepultada bajo otras 30 que hablan de
// lo mismo. En este vault el nombre-frase ES el resumen, así que cuenta aparte.
const raiz = (t) => t.replace(/[*"]/g, '')
const enNombre = (d) => {
  const campo = `${d.path.replace(/.*\//, '').replace(/-/g, ' ')} ${d.titulo}`
    .toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  return terminos.filter((t) => raiz(t) && campo.includes(raiz(t))).length
}

const filas = [...acum.values()]
  .map((d) => ({
    ...d,
    nombre: enNombre(d),
    // ^1.6: cubrir un término más pesa más que puntuar muy alto en uno solo.
    // Y penalización suave por tamaño: quien busca quiere la nota atómica que
    // responde, no el hub de 35.000 tokens que menciona el término 34 veces.
    final: (((d.suma / terminos.length) * Math.pow(d.cobertura / terminos.length, 1.6)) +
            0.9 * Math.pow(enNombre(d) / terminos.length, 2)) /
           (1 + Math.max(0, Math.log10((d.bytes || 1000) / 4000))),
  }))
  .sort((a, b) => b.final - a.final)
  .slice(0, N)

if (!filas.length) { console.log(`sin resultados para: ${consulta}`); process.exit(1) }

// --dup: antes de escribir un learning nuevo, enseñar los que ya lo dicen.
// El vault crece a 24 notas/día y el 53% no se relee nunca; el filo de este
// comando es que AMPLIAR una nota existente casi siempre gana a crear la 1.606.
if (DUP) {
  const umbral = 0.35
  const fuerte = filas.filter((f) => f.final >= umbral)
  console.log(`\n¿Ya existe algo sobre "${consulta}"?\n`)
  for (const [i, f] of filas.slice(0, 8).entries()) {
    const marca = f.final >= umbral ? '⚠︎' : ' '
    console.log(`${marca} ${String(i + 1).padStart(2)}. [${f.final.toFixed(2)}] ${f.titulo}`)
    console.log(`      ${f.path}`)
  }
  console.log(
    fuerte.length
      ? `\n→ ${fuerte.length} nota(s) muy cercanas. AMPLÍA la de arriba antes de crear una nueva:\n` +
        `   cat >> ${fuerte[0].path}`
      : '\n→ nada suficientemente cercano. Crear nota nueva está justificado.'
  )
  process.exit(fuerte.length ? 1 : 0)
}

if (SOLO_PATHS) { console.log(filas.map((f) => f.path).join('\n')); process.exit(0) }

if (CAT) {
  const { readFileSync } = await import('node:fs')
  console.log(`─── ${filas[0].path} ───\n`)
  console.log(readFileSync(join(VAULT, filas[0].path), 'utf8'))
  if (filas.length > 1) console.log(`\n─── otros ${filas.length - 1}: ` + filas.slice(1).map((f) => f.path.replace(/^.*\//, '')).join(' · '))
  process.exit(0)
}

for (const [i, f] of filas.entries()) {
  const cob = `${f.cobertura}/${terminos.length}`
  const tags = f.tags ? ` [${f.tags.split(' ').slice(0, 4).join(' ')}]` : ''
  console.log(`${String(i + 1).padStart(2)}. ${f.titulo}${tags}`)
  void cob
  console.log(`    ${f.path}${f.fecha ? '  ·  ' + f.fecha : ''}`)
  if (f.ctxs?.[0]) console.log(`    ${f.ctxs[0].replace(/\s+/g, ' ').trim().slice(0, 160)}`)
}
