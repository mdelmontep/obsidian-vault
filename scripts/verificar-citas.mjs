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
 *   node scripts/verificar-citas.mjs             # comprueba
 *   node scripts/verificar-citas.mjs --corregir  # y las pone al día
 *
 * Las citas caducaron TRES veces en un mismo día, siempre por ediciones del
 * código que nadie relacionaría con una lección (quitar un import, añadir un
 * bloque). Corregirlas a mano cada vez es la garantía de que un día no se hará:
 * por eso el gate sabe además arreglarlas.
 */
import { readFileSync, existsSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const HOME = process.env.HOME
const LECCION = join(HOME, 'Projects/learn-agentesia/content/0002-memoria-del-vault.html')
const VAULT = join(HOME, 'Projects/obsidian-vault')
const TOLERANCIA = 3

// [cita tal como aparece en la lección, ruta absoluta, fragmento esperado]
const CITAS = [
  ['vault-find.mjs:94', join(VAULT, 'scripts/vault-find.mjs'), 'bm25(fts, 10.0'],
  ['scripts/vault-find.mjs:138-140', join(VAULT, 'scripts/vault-find.mjs'), 'final: (((d.suma'],
  ['scripts/vault-index.mjs:121', join(VAULT, 'scripts/vault-index.mjs'), "delete-all"],
  ['scripts/vault-find.test.mjs:20-39', join(VAULT, 'scripts/vault-find.test.mjs'), 'const CASOS = ['],
  ['learning-dup-guard.sh:16', join(HOME, '.claude/hooks/learning-dup-guard.sh'), 'TTL_MIN='],
  ['learning-dup-guard.sh:41-53', join(HOME, '.claude/hooks/learning-dup-guard.sh'), 'sin_ruido=$(printf'],
]

const CITAS_ACTUALIZADAS = []
const leccion = existsSync(LECCION) ? readFileSync(LECCION, 'utf8') : ''
if (!leccion) { console.error(`no existe la lección: ${LECCION}`); process.exit(1) }

const CORREGIR = process.argv.includes('--corregir')
let fallos = 0, arregladas = 0
let texto = leccion

for (const [cita, fichero, fragmento] of CITAS) {
  if (!texto.includes(cita)) {
    fallos++; console.log(`FALLO la lección ya no contiene la cita "${cita}"`); continue
  }
  if (!existsSync(fichero)) {
    fallos++; console.log(`FALLO ${cita} → el fichero no existe`); continue
  }
  const lineas = readFileSync(fichero, 'utf8').split('\n')
  const [ruta, rango] = cita.split(':')
  const declarada = Number(rango.split('-')[0])
  const real = lineas.findIndex((l) => l.includes(fragmento)) + 1

  if (real === 0) { fallos++; console.log(`FALLO ${cita} → "${fragmento}" ya no aparece en el fichero`); continue }
  if (Math.abs(real - declarada) <= TOLERANCIA) { console.log(`ok    ${cita}`); continue }

  if (CORREGIR) {
    // Se conserva el ancho del rango: una cita a 3 líneas sigue citando 3.
    const ancho = rango.includes('-') ? Number(rango.split('-')[1]) - declarada : 0
    const nueva = ancho ? `${ruta}:${real}-${real + ancho}` : `${ruta}:${real}`
    texto = texto.split(cita).join(nueva)
    CITAS_ACTUALIZADAS.push([cita, nueva])
    arregladas++
    console.log(`ok    ${cita} → ${nueva} (corregida)`)
  } else {
    fallos++
    console.log(`FALLO ${cita} → "${fragmento}" está en la línea ${real}`)
  }
}

if (CORREGIR && arregladas) {
  writeFileSync(LECCION, texto)
  // El propio gate guarda las citas: si no se actualiza, mañana vuelve a fallar.
  let self = readFileSync(new URL(import.meta.url), 'utf8')
  for (const [v, n] of CITAS_ACTUALIZADAS) self = self.split(`'${v}'`).join(`'${n}'`)
  writeFileSync(new URL(import.meta.url), self)
  console.log(`\n${arregladas} cita(s) actualizadas en la lección y en este gate`)
}

console.log(`\n${CITAS.length - fallos}/${CITAS.length} citas resuelven`)
process.exit(fallos ? 1 : 0)
