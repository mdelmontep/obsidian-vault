#!/usr/bin/env node
// Trinquete de presupuesto de contexto del vault.
//
// Los ficheros de ARRANQUE (los que se leen antes de saber qué se va a tocar) se pagan
// en tokens en cada sesión, vengan al caso o no. Este vault tenía tres reglas de tamaño
// escritas y ninguna se cumplía: `hot.md` declaraba "tope duro de 25 entradas" con 73,
// el hub prometía "arranque barato ~6-8K tokens" costando 13K, y `top-of-mind.md` tenía
// 39 KB con un target de 3 KB. Una regla sin máquina detrás no se cumple.
//
// Es un TRINQUETE, no un tope: el baseline es el tamaño de hoy y solo puede BAJAR.
// Así nunca falla en falso (que es lo que hace que un check se ignore) pero bloquea el
// crecimiento. Mismo patrón que `inline-style-ratchet.mjs` en el repo de facturaia, que
// es el único de los tres que sí ha funcionado.
//
//   node scripts/context-budget.mjs           → comprueba (exit 1 si algo creció)
//   node scripts/context-budget.mjs --write   → baja el baseline a los tamaños actuales
//
// El baseline vive en scripts/context-budget.json (git-trackeado: el diff enseña la mejora).

import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')
const BASELINE = join(VAULT, 'scripts', 'context-budget.json')

// Aproximación de tokens para prosa técnica en español (medida sobre este vault: los
// ficheros con mucho `código`/wikilinks salen algo más caros que la regla de 4 chars).
const CHARS_POR_TOKEN = 3.7

/**
 * Qué se mide. `hasta` acota la parte del fichero que de verdad se lee al arrancar:
 * el hub es de 2 niveles y su promesa de coste aplica solo al bloque de arriba, así que
 * medir el fichero entero (146 KB) no diría nada útil.
 */
const OBJETIVOS = [
  { id: 'hot', ruta: 'Stack/hot.md', nota: 'se carga por defecto cuando no hay disparador' },
  { id: 'top-of-mind', ruta: '00-home/top-of-mind.md', nota: 'índice de arranque cross-cliente' },
  {
    id: 'hub-facturaia',
    ruta: '00-home/facturaia.md',
    hasta: '⬇️',
    nota: 'dashboard del hub (hasta el separador ⬇️); promete 6-8K tokens',
  },
  { id: 'hub-agh', ruta: '00-home/agh-iberica.md', hasta: '⬇️', nota: 'dashboard del hub' },
  { id: 'hub-clinica-zen', ruta: '00-home/clinica-zen.md', hasta: '⬇️', nota: 'dashboard del hub' },
]

/** Bytes del tramo que se lee al arrancar. Si `hasta` no aparece, el fichero entero. */
function medir(obj) {
  const p = join(VAULT, obj.ruta)
  if (!existsSync(p)) return null
  const txt = readFileSync(p, 'utf8')
  if (!obj.hasta) return Buffer.byteLength(txt, 'utf8')
  const i = txt.indexOf(obj.hasta)
  return Buffer.byteLength(i === -1 ? txt : txt.slice(0, i), 'utf8')
}

const write = process.argv.includes('--write')
const base = existsSync(BASELINE) ? JSON.parse(readFileSync(BASELINE, 'utf8')) : { objetivos: {} }
const actual = {}
const subidas = []
const bajadas = []

for (const obj of OBJETIVOS) {
  const bytes = medir(obj)
  if (bytes === null) continue
  actual[obj.id] = bytes
  const antes = base.objetivos?.[obj.id]
  if (antes === undefined) continue
  if (bytes > antes) subidas.push({ ...obj, antes, bytes })
  else if (bytes < antes) bajadas.push({ ...obj, antes, bytes })
}

const tok = (b) => Math.round(b / CHARS_POR_TOKEN / 100) / 10 // en miles, 1 decimal
const kb = (b) => (b / 1024).toFixed(1)

if (write) {
  writeFileSync(
    BASELINE,
    JSON.stringify({ actualizado: new Date().toISOString().slice(0, 10), objetivos: actual }, null, 2) + '\n',
  )
  const total = Object.values(actual).reduce((a, b) => a + b, 0)
  console.log(`baseline escrito · ${Object.keys(actual).length} objetivos · arranque total ${kb(total)} KB (~${tok(total)}K tokens)`)
  process.exit(0)
}

const total = Object.values(actual).reduce((a, b) => a + b, 0)
console.log(`Presupuesto de contexto — arranque total ${kb(total)} KB (~${tok(total)}K tokens)\n`)
for (const obj of OBJETIVOS) {
  const b = actual[obj.id]
  if (b === undefined) continue
  const antes = base.objetivos?.[obj.id]
  const delta = antes === undefined ? ' (nuevo)' : b === antes ? '' : b > antes ? ` ▲ +${kb(b - antes)} KB` : ` ▼ −${kb(antes - b)} KB`
  console.log(`  ${kb(b).padStart(7)} KB  ~${String(tok(b)).padStart(4)}K tok  ${obj.id}${delta}`)
}

if (bajadas.length > 0) {
  console.log(`\n${bajadas.length} objetivo(s) han BAJADO. Consolida el baseline:`)
  console.log('  node scripts/context-budget.mjs --write')
}

if (subidas.length > 0) {
  console.log('\nTRINQUETE: el contexto de arranque ha CRECIDO.\n')
  for (const s of subidas) {
    console.log(`  ${s.id}: ${kb(s.antes)} → ${kb(s.bytes)} KB (+${kb(s.bytes - s.antes)} KB, ~+${tok(s.bytes - s.antes)}K tokens por sesión)`)
    console.log(`    ${s.ruta} — ${s.nota}`)
  }
  console.log('\nEsto se paga en CADA sesión que lea ese fichero. Antes de subir el baseline:')
  console.log('  · lo cerrado (✅ / EN PROD / ~~tachado~~) va al histórico del cliente, condensado a 1-2 líneas;')
  console.log('  · un learning nuevo NO obliga a una entrada nueva en hot.md — solo si es método transversal;')
  console.log('  · si de verdad hay que crecer, `--write` y que el diff del baseline lo deje por escrito.')
  process.exit(1)
}

console.log('\ntrinquete OK · el arranque no ha crecido')
