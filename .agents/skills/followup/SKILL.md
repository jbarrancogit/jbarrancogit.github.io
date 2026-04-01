---
name: followup
description: Escanea todos los clientes activos y prospectos para generar un dashboard de seguimiento con acciones pendientes priorizadas. Usá para revisar qué leads o clientes necesitan atención.
user-invocable: true
argument-hint: ""
---

Generar un dashboard de seguimiento con todas las acciones pendientes priorizadas.

## Contexto

- **Clientes activos:** `landing-page/clientes/*/datos-cliente.json` y `README.md`
- **Prospectos:** `KIT_OPERATIVO/prospectos_*.csv`
- **Fecha de hoy:** usá la fecha actual del sistema

## Paso 1: Escanear clientes activos

Para cada directorio en `landing-page/clientes/`:

1. Leé `datos-cliente.json` → extraé: nombre, negocio, teléfono, plan, fecha_inicio
2. Leé `README.md` → buscá checkboxes:
   - `[ ]` = pendiente
   - `[x]` = completado
3. Calculá **días desde inicio** (fecha_inicio vs hoy)

### Items críticos a detectar:
- `[ ] Contenido recibido` + más de 3 días → **URGENTE: pedir contenido**
- `[ ] Contenido recibido` + más de 5 días → **CRÍTICO: cláusula 4 del contrato (5 días hábiles)**
- `[ ] Primer pago recibido` → **Seguimiento de pago**
- `[ ] Prototipo aprobado` + más de 5 días desde envío → **Seguimiento de aprobación**
- `[ ] Sitio entregado` + todo lo demás completo → **Listo para entregar**

## Paso 2: Escanear prospectos

1. Leé todos los CSVs en `KIT_OPERATIVO/prospectos_*.csv`
2. Para cada prospecto con teléfono disponible que NO tenga una carpeta en `clientes/`:
   - Es un lead no contactado o sin cerrar
3. Contá: total prospectos, con teléfono, sin contactar (estimado)

## Paso 3: Generar dashboard

Presentá el output organizado por prioridad:

### 🔴 URGENTE (requiere acción hoy)
- Clientes con contenido vencido (>5 días)
- Pagos pendientes con más de 7 días

### 🟡 SEGUIMIENTO (esta semana)
- Clientes esperando contenido (3-5 días)
- Prototipos enviados sin respuesta (>3 días)
- Clientes en período de soporte que termina pronto

### 🟢 EN CURSO (todo bien)
- Clientes con trabajo en progreso normal
- Items completados recientemente

### 📋 PROSPECTOS SIN CONTACTAR
- Total de prospectos en CSVs
- Cuántos tienen teléfono (contactables)
- Sugerencia: `/outreach [nombre]` para el primero de la lista

## Paso 4: Links de acción rápida

Para cada item urgente o de seguimiento, generá:
- **Link de WhatsApp** con mensaje pre-armado relevante (recordatorio de contenido, seguimiento de aprobación, etc.)
- **Comando sugerido** (`/outreach`, `/deploy-client`, etc.)

### Mensajes pre-armados por situación:

**Pedir contenido (día 3):**
```
Hola [nombre]! Te escribo para ver cómo venís con el material para tu sitio (fotos, textos, logo). Cualquier duda que tengas me avisás y te ayudo. ¡Saludos!
```

**Pedir contenido (día 5+, urgente):**
```
Hola [nombre], te comento que para poder avanzar con tu sitio necesito el material que hablamos (fotos, textos, logo). Sin eso no puedo seguir con el desarrollo. ¿Necesitás ayuda con algo? ¡Avisame!
```

**Seguimiento de prototipo:**
```
Hola [nombre]! ¿Pudiste ver el prototipo que te mandé? Acá te lo dejo de nuevo: [url]. Contame qué te parece y si querés algún cambio. ¡Saludos!
```

**Seguimiento de pago:**
```
Hola [nombre]! Te escribo por el tema del pago del proyecto. ¿Pudiste avanzar con eso? Cualquier duda sobre los medios de pago me avisás. ¡Saludos!
```

Todo el output en **español argentino** (voseo, trato cercano pero profesional).
