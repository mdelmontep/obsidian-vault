#!/usr/bin/env node
/**
 * Índice invertido del vault — SQLite FTS5, cero dependencias.
 *
 * Construye/actualiza `.vault-index.db` (gitignored) con una fila por nota .md.
 * Incremental: solo reindexa lo que cambió de mtime.
 *
 *   node scripts/vault-index.mjs           # incremental
 *   node scripts/vault-index.mjs --full    # reconstruye de cero
 *   node scripts/vault-index.mjs --stats   # no indexa, solo informa
 */
import { DatabaseSync } from 'node:sqlite'
import { readdirSync, statSync, readFileSync } from 'node:fs'
import { join, relative, basename, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DB_PATH = join(VAULT, '.vault-index.db')
const EXCLUIR = new Set(['.git', '.obsidian', '.trash', 'node_modules', '.next'])

const args = new Set(process.argv.slice(2))
const FULL = args.has('--full')
const SOLO_STATS = args.has('--stats')

function* recorrer(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (EXCLUIR.has(e.name) || e.name.startsWith('.')) continue
    const p = join(dir, e.name)
    if (e.isDirectory()) yield* recorrer(p)
    else if (e.isFile() && e.name.endsWith('.md')) yield p
  }
}

/** Frontmatter YAML plano — suficiente para title/date/tags/source. */
function parsearFrontmatter(txt) {
  if (!txt.startsWith('---\n')) return { meta: {}, cuerpo: txt }
  const fin = txt.indexOf('\n---', 4)
  if (fin === -1) return { meta: {}, cuerpo: txt }
  const meta = {}
  for (const linea of txt.slice(4, fin).split('\n')) {
    const m = linea.match(/^([a-zA-Z_-]+):\s*(.*)$/)
    if (m) meta[m[1].toLowerCase()] = m[2].trim().replace(/^["']|["']$/g, '')
  }
  return { meta, cuerpo: txt.slice(fin + 4) }
}

const normalizarTags = (v) =>
  !v ? '' : v.replace(/[[\]]/g, '').split(',').map((s) => s.trim()).filter(Boolean).join(' ')

const db = new DatabaseSync(DB_PATH)
db.exec('PRAGMA journal_mode = WAL')

if (FULL) db.exec('DROP TABLE IF EXISTS notas; DROP TABLE IF EXISTS fts')

db.exec(`
  CREATE TABLE IF NOT EXISTS notas (
    path TEXT PRIMARY KEY, slug TEXT, titulo TEXT, tags TEXT, fecha TEXT,
    carpeta TEXT, mtime INTEGER, bytes INTEGER, enlaces_salientes INTEGER
  );
  CREATE INDEX IF NOT EXISTS idx_notas_slug ON notas(slug);
  CREATE INDEX IF NOT EXISTS idx_notas_carpeta ON notas(carpeta);
  -- remove_diacritics 2: "migración" encuentra "migracion" y viceversa.
  CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
    slug, titulo, tags, cuerpo,
    content='', tokenize="unicode61 remove_diacritics 2"
  );
`)

// FTS5 contentless no soporta UPDATE por rowid arbitrario: reconstruimos el
// índice textual entero cuando hay cualquier cambio. A 1.800 notas cuesta <1s.
const previas = new Map(
  db.prepare('SELECT path, mtime FROM notas').all().map((r) => [r.path, r.mtime])
)

// Primera pasada: solo stat (barato). Leer los 1.800 ficheros solo si algo cambió.
const ficheros = [...recorrer(VAULT)]
const vistos = new Set()
let cambios = 0
for (const abs of ficheros) {
  const path = relative(VAULT, abs)
  vistos.add(path)
  if (previas.get(path) !== Math.floor(statSync(abs).mtimeMs)) cambios++
}
const borradas = [...previas.keys()].filter((p) => !vistos.has(p))

if (SOLO_STATS) {
  console.log(`notas en disco: ${ficheros.length} | indexadas: ${previas.size}`)
  console.log(`cambiadas: ${cambios} | borradas: ${borradas.length}`)
  process.exit(0)
}
if (cambios === 0 && borradas.length === 0 && previas.size === ficheros.length) {
  console.log(`índice al día — ${ficheros.length} notas`)
  process.exit(0)
}

// Segunda pasada: ahora sí, leer y parsear.
const filas = []
for (const abs of ficheros) {
  const path = relative(VAULT, abs)
  const st = statSync(abs)
  const mtime = Math.floor(st.mtimeMs)
  const txt = readFileSync(abs, 'utf8')
  const { meta, cuerpo } = parsearFrontmatter(txt)
  const slug = basename(path, '.md')
  filas.push({
    path, slug,
    titulo: meta.title || slug.replace(/-/g, ' '),
    tags: normalizarTags(meta.tags),
    fecha: meta.date || '',
    carpeta: dirname(path),
    mtime, bytes: st.size,
    enlaces: (cuerpo.match(/\[\[/g) || []).length,
    cuerpo: cuerpo.replace(/\s+/g, ' ').slice(0, 20000),
  })
}
db.exec('BEGIN')
// Una tabla FTS5 contentless NO admite DELETE: se vacía con su comando especial
// 'delete-all'. El bug solo aparecía al REINDEXAR, no al crear el índice de cero,
// así que la primera corrida en verde no probaba nada de este camino.
db.exec('DELETE FROM notas')
db.exec("INSERT INTO fts(fts) VALUES('delete-all')")
const insNota = db.prepare(
  'INSERT INTO notas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
)
const insFts = db.prepare('INSERT INTO fts (rowid, slug, titulo, tags, cuerpo) VALUES (?, ?, ?, ?, ?)')
let rowid = 0
for (const f of filas) {
  insNota.run(f.path, f.slug, f.titulo, f.tags, f.fecha, f.carpeta, f.mtime, f.bytes, f.enlaces)
  // El slug va con guiones Y con espacios: así "worktree" casa en
  // `qa-next-worktree-symlink` sin depender de que el tokenizador parta guiones.
  insFts.run(++rowid, `${f.slug} ${f.slug.replace(/-/g, ' ')}`, f.titulo, f.tags, f.cuerpo)
}
db.exec('COMMIT')
db.exec("INSERT INTO fts(fts) VALUES('optimize')")

console.log(`indexadas ${filas.length} notas (${cambios} nuevas/cambiadas, ${borradas.length} borradas)`)
