---
title: cancelar cita debe borrar evento de google calendar
date: 2026-04-20
source: claude-code-session
tags: [clinica-zen, google-calendar, n8n]
---

Actualmente el workflow "Leads cambio de fecha o anulacion" (`DkueIeGFWLKh8nTj`) cambia el status del lead en Kommo pero NO borra/modifica el evento en Google Calendar. El paciente queda con una cita fantasma en el calendario.

Pendiente: añadir nodo Google Calendar Delete Event (o Update para cambio de fecha) al workflow.
