#!/usr/bin/env node
/**
 * Gate de las citas `fichero:línea` de una lección de Aula.
 *
 * El repo de Aula exige que cada afirmación traiga su cita, pero una cita por
 * número de línea CADUCA en silencio: al limpiar código muerto de vault-find.mjs
 * dos citas de esta lección pasaron a apuntar a líneas que ya no eran las suyas,
 * y nada avisó. Esto lo convierte en un gate.
 *
 * Cada cita se declara junto a un fragmento que DEBE aparecer en esa línea (±3).
 * Comprobar sólo que el fichero existe no probaría nada.
 *
 *   node scripts/verificar-citas.mjs
 */
import { readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const HOME = process.env.HOME
const LECCION = join(HOME, 'Projects/learn-agentesia/content/0002-memoria-del-vault.html')
const VAULT = join(HOME, 'Projects/obsidian-vault')
const TOLERANCIA = 3

// [cita tal como aparece en la lección, ruta absoluta, fragmento esperado]
const CITAS = [
  ['vault-find.mjs:87', join(VAULT, 'scripts/vault-find.mjs'), 'bm25(fts, 10.0'],
  ['scripts/vault-find.mjs:131-133', join(VAULT, 'scripts/vault-find.mjs'), 'final: (((d.suma'],
  ['scripts/vault-index.mjs:121', join(VAULT, 'scripts/vault-index.mjs'), "delete-all"],
  ['scripts/vault-find.test.mjs:20-39', join(VAULT, 'scripts/vault-find.test.mjs'), 'const CASOS = ['],
  ['learning-dup-guard.sh:16', join(HOME, '.claude/hooks/learning-dup-guard.sh'), 'TTL_MIN='],
  ['learning-dup-guard.sh:41-53', join(HOME, '.claude/hooks/learning-dup-guard.sh'), 'sin_ruido=$(printf'],
]

const leccion = existsSync(LECCION) ? readFileSync(LECCION, 'utf8') : ''
if (!leccion) { console.error(`no existe la lección: ${LECCION}`); process.exit(1) }

let fallos = 0
for (const [cita, fichero, fragmento] of CITAS) {
  if (!leccion.includes(cita)) {
    fallos++; console.log(`FALLO la lección ya no contiene la cita "${cita}"`); continue
  }
  if (!existsSync(fichero)) {
    fallos++; console.log(`FALLO ${cita} → el fichero no existe`); continue
  }
  const lineas = readFileSync(fichero, 'utf8').split('\n')
  const declarada = Number(cita.split(':')[1].split('-')[0])
  const real = lineas.findIndex((l) => l.includes(fragmento)) + 1
  const ok = real > 0 && Math.abs(real - declarada) <= TOLERANCIA
  if (!ok) fallos++
  console.log(
    ok ? `ok    ${cita}` : `FALLO ${cita} → "${fragmento}" está en la línea ${real || '(no aparece)'}`
  )
}

console.log(`\n${CITAS.length - fallos}/${CITAS.length} citas resuelven`)
process.exit(fallos ? 1 : 0)
