---
title: daily briefing
date: 2026-08-10
tags: [home, briefing]
---

# 🌅 Briefing 10-ago

## ✅ Lo que cerraste ayer

**TuCRMIA — acceso verificado y plan agéntico reescrito de raíz**

Ayer hiciste dos entregas en TuCRMIA: primero, comprobaste en pantalla que las tres vías de acceso funcionan (contraseña con bloqueo, Google y enlace mágico) y que el registro público está cerrado. Segundo, reescribiste la capa agéntica del plan: 41 gates bien definidos, puerta de autonomía que ahora usa la cota de Wilson (antes era "95 % sobre 50", que nadie podía demostrar ni cerrar) y un contrato v1 que puede ejecutar un agente, no solo leerlo un humano.

**Cómo lo usas en la práctica:**
- Cuando alguien entra al CRM tiene tres vías y el registro público cerrado: ningún desconocido puede crearse una cuenta.
- La puerta de autonomía ya no es un objetivo vacío: cuando el sistema llega al umbral real puedes cerrarla y no volver a abrirla.
- El agente sabe exactamente qué queda en su caja negra y qué se registra fuera: sin ambigüedad de contrato.

Además: ticket IET #1537 (Excel de presupuesto de obra, el único que se saltó la tanda) cerrado y contestado en el día.

## 🎯 Hoy en orden de prioridad

1. **Elphis — bot WhatsApp rompe 1 de cada 5 veces** — `bigint: "null"` en `conv_state`, 65 errores acumulados con pacientes reales. Sin diagnosticar aún.
2. **Clínica Zen — fix del nombre inventado reincidió** — v64 volvió a escribir "Paciente nuevo" y "Polígono Európolis". Está en el Code node; tienes OK de Gonzalo para tocarlo.
3. **TuFacturaIA — confirmar tickets 142-145 con IET** — En prod (#1543). El 144 cambiaba el precio de la partida seleccionada; pídele que lo repase.
4. **TuFacturaIA — llamar a Natalia** — El §5 de la mig 656 (294 precios suben) sigue sin su OK y lo confunde con la conversión ya hecha.
5. **Simarro — 4 crons sin ejecutarse** — Confirmar retención de instancia antes (en CZ estaba en 7 h creyendo que eran días).

## ⏳ Pendientes y bloqueos

- **Esperando a notcapi**: Agentesia web PR #94 (H1 sin "en Madrid") — gates verdes desde hace una semana.
- **Esperando a Borja**: agency-portal PR #209 + 6 PRs AGH Ibérica + Actions muerto (41/41 runs con 0 pasos).
- **Tuyo — TuCRMIA**: 10 piezas sueltas antes de arrancar: `tucrmia.com`, Turnstile, buzón real, Supabase free (#32), 4 endpoints de facturaia (#33), techo de € IA (#13), rotar claves.

## 💡 Quick win sugerido

**Canal de aviso del check de efecto** — el script ya detecta fallos (pilló el de Elphis hace días). Solo falta una línea de config: Slack `#01-incidencias` o Telegram. 15 minutos y dejas de mirar el log a mano.

## ⚠️ Stale (>7 días)

- **SEPA y Stripe cobran importe bruto** (desde 25-jul, +16 días) — Remesas y Payment Link siguen usando el total con retención. Empujar `PR-0c` o decidir con Borja.
- **cryptobruj-bot en LIVE** (desde 03-ago, +7 días) — `scalp-5m` con posición abierta, sin `ADMIN_TOKEN` ni panel funcional. Primero `POST /strategies/scalp-5m/stop`; solo con posición cerrada, `TRADING_MODE=paper` + redeploy.

---

# 🌅 Briefing 09-ago

## ✅ Lo que cerraste ayer y anteayer

**Sprint de infra + horas reales en FacturaIA**

El 7 fue fontanería pura: parches de seguridad en cinco servidores Dokploy, SSH de cada host en 1Password y guardián de overlay instalado para que los contenedores vuelvan solos tras un reboot. También desbloqueaste el HTTPS de TuCRMIA —el límite era de traefik.me, no código tuyo— y cerraste la mig 656: la mano de obra en FacturaIA ya usa horas reales, no estimadas.

El 8 fue corto: el Excel del presupuesto de OBRA de IET arreglado y contestado en el día (#1537).

**Cómo lo usas en la práctica:**
- El próximo reboot de Tecnocloud o Simarro no te deja con Dokploy vacío: los contenedores arrancan solos.
- Cuando IET saca un presupuesto de obra, el Excel ya cuadra con el árbol de líneas completo.

## 🎯 Hoy en orden de prioridad

1. **Centro Elphis — bot WhatsApp falla 1 de cada 5 veces** — `invalid input syntax for type bigint: "null"` en `conv_state`. 65 errores en 7 días, los pacientes lo notan. Sin diagnosticar aún.
2. **Clínica Zen — el fix del nombre reincidió el 2-ago** — Con la v64 volvió a usar `"Paciente nuevo"` y "Polígono Európolis". El fallo está en el Code node. Tienes OK de Gonzalo para tocar el workflow.
3. **TuFacturaIA — confirmar tickets 142-145 con IET** — En prod (#1543). Pídele que los repase; el 144 cambiaba el precio de la partida seleccionada.

## ⏳ Pendientes y bloqueos

- **Esperando a notcapi**: PRs Agentesia web #97 y #99 — el #97 lleva el fix que oculta nombres reales en los audios. Urgente.
- **Esperando a Borja**: agency-portal PR #209 + 6 PRs de AGH Ibérica + CI muerto (41/41 runs con 0 pasos ejecutados).
- **Tuyo — Salt Edge PR #610**: sin tocar desde el 27-jul. Apruébalo o ciérralo hoy.

## 💡 Quick win sugerido

**Canal de aviso del check de efecto semanal** — El script ya detecta fallos (pilló el de Elphis). Solo falta una línea de config: Slack `#01-incidencias` o Telegram. 15 minutos.

## ⚠️ Stale (>7 días)

- **SEPA y Stripe cobran importe bruto** (desde 25-jul, +15 días) — Remesas y Payment Link siguen usando el total con retención. Empujar `PR-0c` o acordar con Borja quién lo cierra.
- **cryptobruj-bot en LIVE sin freno** (desde 03-ago) — Sigue en real. Primero `POST /strategies/scalp-5m/stop`; solo con la posición cerrada, `TRADING_MODE=paper` + redeploy.
