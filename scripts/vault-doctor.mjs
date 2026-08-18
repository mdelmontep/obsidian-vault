#!/usr/bin/env node
/**
 * Salud del vault: enlaces rotos, notas aisladas y desfase del índice temático.
 *
 *   vault-doctor            # informe
 *   vault-doctor --rotos    # solo los wikilinks que no resuelven, para arreglarlos
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join, dirname, relative, basename } from 'node:path'
import { fileURLToPath } from 'node:url'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')
const EXCLUIR = new Set(['.git', '.obsidian', '.trash', 'node_modules', '.next'])
const SOLO_ROTOS = process.argv.includes('--rotos')

function* recorrer(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (EXCLUIR.has(e.name) || e.name.startsWith('.')) continue
    const p = join(dir, e.name)
    if (e.isDirectory()) yield* recorrer(p)
    else if (e.isFile() && e.name.endsWith('.md')) yield p
  }
}

const ficheros = [...recorrer(VAULT)]
const existentes = new Set(ficheros.map((f) => basename(f, '.md')))
const entrantes = new Map()
const rotos = []
let sinSalientes = 0

for (const abs of ficheros) {
  const rel = relative(VAULT, abs)
  const txt = readFileSync(abs, 'utf8')
  const links = [...txt.matchAll(/\[\[([^\]|#]+)/g)].map((m) => basename(m[1].trim()))
  if (!links.length) sinSalientes++
  for (const l of links) {
    if (!l || l.includes(':')) continue
    if (existentes.has(l)) entrantes.set(l, (entrantes.get(l) || 0) + 1)
    else rotos.push({ desde: rel, hacia: l })
  }
}

if (SOLO_ROTOS) {
  for (const r of rotos) console.log(`${r.desde}\t[[${r.hacia}]]`)
  process.exit(rotos.length ? 1 : 0)
}

// El MOC declaraba 973 notas cuando había 1.605: un índice escrito a mano
// envejece en silencio y sigue pareciendo completo. Aquí se mide, no se cree.
const learnings = ficheros.filter((f) => f.includes('/learnings/')).map((f) => basename(f, '.md'))
const moc = readFileSync(join(VAULT, 'knowledge/learnings-index.md'), 'utf8')
const enMoc = new Set([...moc.matchAll(/\[\[([^\]|#]+)/g)].map((m) => m[1].trim()))
const fueraMoc = learnings.filter((l) => !enMoc.has(l))

const huerfanos = learnings.filter((l) => !entrantes.has(l) || (entrantes.get(l) === 1 && enMoc.has(l)))

console.log(`notas .md            ${ficheros.length}`)
console.log(`learnings            ${learnings.length}`)
console.log(`wikilinks rotos      ${rotos.length}   (vault-doctor --rotos para verlos)`)
console.log(`sin enlaces salientes ${sinSalientes}   (${Math.round((sinSalientes / ficheros.length) * 100)}% del vault)`)
console.log(`learnings fuera del índice temático  ${fueraMoc.length} de ${learnings.length}  (cobertura ${Math.round((1 - fueraMoc.length / learnings.length) * 100)}%)`)
console.log(`learnings que solo enlaza el índice  ${huerfanos.length}`)

// Uso real del buscador. Es lo que faltaba en el diagnóstico original: sin esto
// no hay forma de saber si el vault ACIERTA, sólo de cuánto crece.
try {
  const log = readFileSync(join(VAULT, '.vault-queries.log'), 'utf8')
    .split('\n').filter(Boolean).map((l) => JSON.parse(l))
  const secas = log.filter((q) => q.n === 0)
  const dias = new Set(log.map((q) => q.t.slice(0, 10))).size
  console.log(`\nconsultas registradas   ${log.length} en ${dias} día(s)`)
  console.log(`sin resultados          ${secas.length}   ← cada una es una nota que falta`)
  if (secas.length) for (const q of secas.slice(-5)) console.log(`   · ${q.q}`)
  const top = {}
  for (const q of log) for (const t of q.top || []) top[t] = (top[t] || 0) + 1
  const mas = Object.entries(top).sort((a, b) => b[1] - a[1]).slice(0, 3)
  if (mas.length) {
    console.log('notas más devueltas:')
    for (const [t, n] of mas) console.log(`   ${String(n).padStart(3)}×  ${t.replace(/\.md$/, '')}`)
  }
} catch { console.log('\nconsultas registradas   0 (aún no se ha usado vault-find)') }
