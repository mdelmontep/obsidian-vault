#!/usr/bin/env node
/**
 * Gate del buscador: consultas reales → la nota que DEBE salir arriba.
 *
 * Sin esto, cada ajuste del ranking es una apuesta: el tuning que arregla una
 * consulta rompe otra en silencio. Se corre con `npm test`-menos: `node
 * scripts/vault-find.test.mjs`. Exit 1 si alguna regresiona.
 */
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const VAULT = join(dirname(fileURLToPath(import.meta.url)), '..')

// [consulta, slug esperado, posición máxima aceptable, {prohibido: ruta}]
//
// Los casos NO son decorativos: cada bloque cubre una pieza del scoring, y se
// eligieron mutando esa pieza y quedándose con las consultas que cambiaban de
// resultado. Un caso que sigue verde con la pieza anulada no prueba nada.
const CASOS = [
  ['verificar que un test tiene dientes con una mutacion', 'verificar-que-un-test-tiene-dientes-con-una-mutacion', 1],
  ['migracion supabase falla al hacer push', 'migracion-aplicada-fuera-de-historial-supabase', 3],
  ['rls sobre tabla vacia', 'verificar-rls-en-tabla-vacia-no-discrimina', 2],
  ['test verde que no prueba nada', 'una-suite-en-verde-no-prueba-el-camino-real', 3],
  ['worktree symlink node_modules next', 'worktree-qa-next-standalone-symlink-node-modules', 3],
  ['bucket s3 con puntos en el nombre', 'buckets-con-puntos-obligan-a-path-style-por-el-wildcard-tls', 2],
  ['guard que decide por mencion', 'un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro', 2],
  ['borrar la rama encadenado al merge', 'el-borrado-de-rama-nunca-va-encadenado-al-merge', 3],

  // Cubren la COBERTURA de términos: sin ella, el documento con la palabra más
  // rara gana aunque ignore el resto de la consulta.
  ['un endpoint devuelve 200 pero no escribe nada', 'update-que-afecta-cero-filas-no-devuelve-error-en-postgrest', 1],
  ['el deploy dice ok y la version vieja sigue arriba', 'verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado', 1],

  // Cubre la penalización ANTI-HUB: sin ella, un archivo de incidencias de
  // 26.000 tokens se cuela en el top por acumular menciones.
  ['incidente chatwoot whatsapp', 'chatwoot-whatsapp-cloud-requiere-redirigir-webhook-meta', 1,
    { prohibido: 'Stack/incidents-archive-2026-06.md' }],
]

let fallos = 0

// Antes que el ranking: que el índice sobreviva a un REINDEXADO. La primera
// versión creaba el índice bien y reventaba al actualizarlo ("cannot DELETE from
// contentless fts5 table"), porque una corrida sobre índice inexistente no pasa
// por ese camino. Se fuerza aquí, no se supone.
try {
  execFileSync('node', [join(VAULT, 'scripts/vault-index.mjs'), '--full'], { stdio: 'pipe' })
  execFileSync('touch', [join(VAULT, 'Stack/index.md')])
  execFileSync('node', [join(VAULT, 'scripts/vault-index.mjs')], { stdio: 'pipe' })
  console.log('ok   reindexado incremental sobre índice existente')
} catch (e) {
  fallos++
  console.log(`FALLO reindexado incremental: ${String(e.stderr || e).split('\n').find((l) => l.includes('Error')) || e}`)
}

// stdout es el resultado, stderr es el progreso. En una máquina nueva hay que
// construir el índice, y ese aviso caía en stdout: `--paths | xargs cat` intentaba
// abrir un fichero llamado "indexadas". Se fuerza el arranque en frío aquí.
try {
  execFileSync('rm', ['-f', join(VAULT, '.vault-index.db'), join(VAULT, '.vault-index.db-wal'), join(VAULT, '.vault-index.db-shm')])
  const salida = execFileSync('node', [join(VAULT, 'scripts/vault-find.mjs'), '-n', '3', '--paths', 'rls tabla vacia'], {
    encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
  })
  const sucias = salida.trim().split('\n').filter((l) => l && !l.endsWith('.md'))
  if (sucias.length) throw new Error(`stdout contaminado: ${JSON.stringify(sucias[0])}`)
  console.log('ok   --paths en frío devuelve sólo rutas .md')
} catch (e) {
  fallos++
  console.log(`FALLO --paths en frío: ${e.message}`)
}

for (const [consulta, esperado, maxPos, extra] of CASOS) {
  let salida = ''
  try {
    salida = execFileSync('node', [join(VAULT, 'scripts/vault-find.mjs'), '-n', '10', '--paths', consulta], {
      encoding: 'utf8',
    })
  } catch { /* exit 1 = sin resultados; se trata como fallo abajo */ }
  const paths = salida.trim().split('\n').filter(Boolean)
  const pos = paths.findIndex((p) => p.endsWith(`/${esperado}.md`)) + 1
  let ok = pos > 0 && pos <= maxPos
  let nota = pos ? `(pos ${pos}, max ${maxPos})` : '(NO aparece en top 10)'
  if (ok && extra?.prohibido) {
    const colado = paths.slice(0, maxPos + 2).indexOf(extra.prohibido) + 1
    if (colado) { ok = false; nota = `(prohibido ${extra.prohibido} colado en pos ${colado})` }
  }
  if (!ok) fallos++
  console.log(`${ok ? 'ok  ' : 'FALLO'} "${consulta}" → ${esperado} ${nota}`)
}

const total = CASOS.length + 2  // +2: reindexado y stdout limpio en frío
console.log(`\n${total - fallos}/${total} comprobaciones en verde`)
process.exit(fallos ? 1 : 0)
