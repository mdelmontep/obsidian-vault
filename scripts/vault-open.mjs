#!/usr/bin/env node
/**
 * Lector por secciones — sirve el NIVEL 1 de un hub, no el fichero entero.
 *
 * El hub de FacturaIA ya declara "arranque de sesión, barato ~6-8K tokens: leer
 * solo Estado + NOW + Bloqueos + Decisiones + Índice de áreas". Ese diseño
 * existía y nadie lo cumplía, porque abrir el fichero significaba leer sus
 * 35.500 tokens. Esto lo cumple.
 *
 *   vault-open 00-home/facturaia.md            # nivel 1 + menú del resto con su coste
 *   vault-open 00-home/facturaia.md --sec NEXT # una sección concreta
 *   vault-open 00-home/facturaia.md --all      # el fichero entero (lo de antes)
 *   vault-open --mapa                          # los ficheros más caros del vault
 */
import { readFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { DatabaseSync } from 'node:sqlite'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')
const CFG_PATH = join(VAULT, 'scripts/vault-open.json')
const cfg = existsSync(CFG_PATH) ? JSON.parse(readFileSync(CFG_PATH, 'utf8')) : { hubs: {} }

// ~3,6 bytes por token en prosa técnica española con acentos. Suficiente para
// decidir si abrir algo; no pretende ser exacto.
const tok = (s) => Math.round(s.length / 3.6)

const argv = process.argv.slice(2)
const opt = (n) => { const i = argv.indexOf(n); return i === -1 ? null : argv.splice(i, 2)[1] }
const flag = (n) => { const i = argv.indexOf(n); if (i === -1) return false; argv.splice(i, 1); return true }

const MAPA = flag('--mapa')
const ALL = flag('--all')
const SEC = opt('--sec')
const rel = argv[0]

if (MAPA) {
  const db = new DatabaseSync(join(VAULT, '.vault-index.db'), { readOnly: true })
  const filas = db.prepare('SELECT path, bytes FROM notas ORDER BY bytes DESC LIMIT 20').all()
  const total = db.prepare('SELECT SUM(bytes) t, COUNT(*) n FROM notas').get()
  console.log(`vault: ${total.n} notas, ~${tok('x'.repeat(total.t)).toLocaleString('es')} tokens en total\n`)
  console.log('los 20 ficheros más caros de abrir:\n')
  for (const f of filas) console.log(`${String(tok('x'.repeat(f.bytes))).padStart(7)} tok  ${f.path}`)
  process.exit(0)
}

if (!rel) {
  console.error('uso: vault-open <ruta.md> [--sec NOMBRE] [--all] | vault-open --mapa')
  process.exit(2)
}

const abs = join(VAULT, rel)
if (!existsSync(abs)) { console.error(`no existe: ${rel}`); process.exit(1) }
const txt = readFileSync(abs, 'utf8')

if (ALL) { process.stdout.write(txt); process.exit(0) }

/** Parte por H2 conservando el bloque de cabecera (frontmatter + H1 + intro). */
function seccionar(t) {
  const lineas = t.split('\n')
  const cabecera = []
  const secs = []
  let actual = null
  for (const l of lineas) {
    if (l.startsWith('## ')) {
      if (actual) secs.push(actual)
      actual = { titulo: l.slice(3).trim(), lineas: [l] }
    } else if (actual) actual.lineas.push(l)
    else cabecera.push(l)
  }
  if (actual) secs.push(actual)
  return { cabecera: cabecera.join('\n'), secs: secs.map((s) => ({ ...s, texto: s.lineas.join('\n') })) }
}

const { cabecera, secs } = seccionar(txt)
const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')

if (SEC) {
  const q = norm(SEC)
  const hit = secs.find((s) => norm(s.titulo).startsWith(q)) || secs.find((s) => norm(s.titulo).includes(q))
  if (!hit) {
    console.error(`sección "${SEC}" no encontrada. Disponibles:`)
    for (const s of secs) console.error(`  · ${s.titulo.slice(0, 70)}`)
    process.exit(1)
  }
  process.stdout.write(hit.texto)
  process.exit(0)
}

// Nivel 1: cabecera + las secciones declaradas de arranque en vault-open.json.
// Sin declaración, solo la cabecera: abrir a ciegas no debe costar 35.000 tokens.
const arranque = cfg.hubs?.[rel]?.arranque ?? []
const esArranque = (s) => arranque.some((a) => norm(s.titulo).startsWith(norm(a)))

let salida = cabecera.trimEnd() + '\n'
let servidos = tok(cabecera)
for (const s of secs) if (esArranque(s)) { salida += '\n' + s.texto.trimEnd() + '\n'; servidos += tok(s.texto) }

const resto = secs.filter((s) => !esArranque(s))
const totalTok = tok(txt)

salida += `\n---\n\n## Secciones NO servidas (${resto.length}) — ábrelas solo si tocan\n\n`
for (const s of resto) {
  salida += `- \`--sec "${s.titulo.split(/[(—]/)[0].trim().slice(0, 40)}"\` · ~${tok(s.texto)} tok · ${s.titulo.slice(0, 60)}\n`
}
salida += `\nServido ~${servidos} tok de ~${totalTok} tok del fichero`
salida += ` (ahorro ${Math.round((1 - servidos / totalTok) * 100)}%). \`--all\` para el fichero entero.\n`

process.stdout.write(salida)
