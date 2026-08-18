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
