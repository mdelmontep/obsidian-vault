---
title: frontend — motion y performance
date: 2026-04-20
source: claude-md-migration
tags: [frontend, motion, performance, framer]
---

# Frontend / Motion & Performance

## Reglas al depurar jank de scroll o animaciones

- **Invocar siempre el skill `fixing-motion-performance` primero** (instalado en `~/.claude/skills/`). Tiene checklist por prioridades (never patterns, measurement, scroll, paint, layers, blur, view transitions).
- **`useMotionValueEvent` corre por frame**. Los `setState` dentro cuestan aunque React haga bail-out al mismo valor. Gatear con refs y llamar a React **solo cuando el valor realmente cambia**:
  ```tsx
  const lastIdxRef = useRef(-1)
  useMotionValueEvent(progress, "change", p => {
    const idx = calc(p)
    if (idx === lastIdxRef.current) return
    lastIdxRef.current = idx
    setActiveIdx(idx)
  })
  ```
- **No promover más de 1-2 layers grandes con `willChange`**. N capas full-viewport = N × memoria GPU → asesino en móvil. Añadir `willChange` por reflejo a una lista de elementos iguales suele ser regresión, no optimización. Rule 6 del skill.
- **`contain: layout paint size`** en contenedores full-bleed hermanos aísla su árbol de renderizado: el navegador puede saltar layout/paint de los ocultos sin necesidad de `willChange`.

## motion/react — pausar animaciones ocultas

- **`motion.div` con `opacity: 0` NO pausa las `repeat: Infinity`** — motion no sabe que el elemento está visualmente oculto, sigue ejecutando el loop. Para desactivarlas de verdad: desmontar el subtree **o** gatear el `animate` por una flag (`animate={isActive ? [...] : {}}`).
- **Patrón "mount-all scenes" (sticky scroll multi-escena)**: pasar de `AnimatePresence key={i}` a todas las escenas montadas con opacity toggle **elimina el coste de remount** pero **mantiene vivas todas las infinite loops**. Renderizar solo vecinos (`|active - i| <= 1`) limita a 3 escenas vivas en memoria en vez de N, sin pop-in visible.
- **Pasar de `AnimatePresence` remount a opacity + CSS `transition`** es mejor para crossfades de secciones pesadas, pero hay que **auditar `repeat: Infinity` antes** de aplicar el cambio — si no, cambias coste de remount por coste de N loops infinitos en paralelo.

## Hero split "antes/después" con foto real

- **Foto real de fondo + mock flotante encima necesita 3 capas obligatorias**: (1) gradiente blanco vertical `rgba(255,255,255,0.2) → 0.85` encima de la foto para legibilidad, (2) mock con `boxShadow: "0 16px 44px rgba(0,0,0,0.14)"` + borde sutil, (3) mock anclado al borde inferior (`bottom-5 left-5 right-5`) para sensación de flotación. Sin los tres, el mock parece pegado en Paint y la foto compite con el contenido.

## SVG charts responsive

- **`viewBox` normalizado (`0 0 100 100`) + `preserveAspectRatio="none"` distorsiona `<circle>` y markers** — el radio escala con factores X≠Y y queda ovalado. `vector-effect="non-scaling-stroke"` solo preserva el grosor del stroke, no la geometría del elemento. Fix: medir el contenedor con `useLayoutEffect` + `ResizeObserver` síncrono antes del primer paint y usar coordenadas en píxeles reales en el viewBox para que todos los elementos compartan el mismo sistema de coordenadas.

## CSS stagger animation sin JS

- **Patrón**: asignar `animation-delay` por elemento vía selectores CSS directos. Cero JS, cero re-renders. Ejemplo: `.auth-card h1 { animation-delay: 0s }`, `.auth-card .subtitle { animation-delay: 0.07s }`, etc.
- **`prefers-reduced-motion` debe listar cada selector animado explícitamente** — no basta con deshabilitar un keyframe global. Cada `animation` declarada en otro selector debe ser reseteada individualmente en el bloque `@media (prefers-reduced-motion: reduce)`.
- **Easing recomendado**: `cubic-bezier(0.22,1,.36,1)` (ease-out-expo) a 450-550ms para entradas. Para pings/loops infinitos: `animation-iteration-count: infinite` animando solo `opacity` y `transform`.

## Auditoría rápida de una sección con jank

1. Grep `repeat:\s*Infinity` y `filter:\s*["`]?blur` en los archivos de la sección
2. Contar cuántas `motion.div` full-viewport tienen `willChange`
3. Verificar que los `useEffect` de cada escena hacen `if (!isActive) { ...reset; return }`
4. Ver si el scroll handler dispara `setState` en cada frame
