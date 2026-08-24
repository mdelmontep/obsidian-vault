---
title: una etiqueta de estado interno se tapa en el where, no en el render
date: 2026-08-24
source: tecnocloud
tags: [seguridad, prisma, multi-audiencia]
---

Una misma tabla sirve a dos audiencias (consola de soporte y portal del cliente). La etiqueta
`sin clasificar` la escribe la capa interna y el detalle del ticket del portal la pintaba: le decía
a quien había llamado que su aviso **seguía sin mirar**.

- Excluirla en el `where` de la consulta del cliente, **no en el componente**: el render es uno de
  N consumidores y la página siguiente se olvida. Si no sale del servidor, no hay nada que olvidar.
- El nombre de la etiqueta tiene dos dueños en capas distintas (el servicio que la escribe, el
  portal que la oculta) → módulo compartido, no literal duplicado.
- La lista de "internas" se deriva de un `Record<Union, true>`, así que **añadir una interna y
  olvidar taparla no compila** (el array suelto compila y se desincroniza en silencio).
- Señal de que existe el agujero: el mismo literal aparece en un camino de escritura y en uno de
  render. Y de paso, no mandes al cliente `id`s que no usa.
