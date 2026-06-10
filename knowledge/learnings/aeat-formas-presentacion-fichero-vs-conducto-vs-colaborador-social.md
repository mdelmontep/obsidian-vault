---
title: formas de presentar un modelo aeat — fichero vs conducto (cert cliente) vs colaborador social
date: 2026-06-10
source: claude-code-session
tags: [fiscal, aeat, espana, saas]
---
Presentar un modelo (303/130/…) ante la AEAT es siempre electrónico con identidad (certificado/Cl@ve). Tres niveles para un SaaS:
1. **Fichero oficial + guía** — generas el fichero importable (formato BOE, diseño de registro `DRxxx.xlsx`); el cliente lo importa en la sede y firma él. Cero responsabilidad de presentar. Paridad Contasimple/Quipu/Anfix.
2. **3b conducto (modelo Holded)** — el cliente sube su `.p12` una vez y presentas con SU certificado. **Esquiva la figura de colaborador social** porque actúas como conducto técnico, no en nombre propio. Custodias el cert (riesgo + seguro RC prudente). Reaprovecha cert+firma de Verifactu (`certificate.ts`/`sign.ts`).
3. **Colaborador social** (RD 1065/2007 art 79) — alta + convenio con AEAT, RC obligatorio, responsabilidad solidaria art 92 LGT. Figura de gestorías; un SaaS pure-play no la necesita si usa nivel 2 o 3b.
Verifactu ≠ presentar modelos: es otro web service. El fichero oficial hace falta igual para nivel 2 y 3b. Ver [[verifactu-xml-desglose-obligatorio-xsd-rechaza-sin-el]] · [[aeat-disenos-registro-en-xlsx-no-html-mirror-mit]].
