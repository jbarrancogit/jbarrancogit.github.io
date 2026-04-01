---
name: outreach
description: Genera un mensaje personalizado de WhatsApp o email para contactar a un prospecto. Lee las plantillas de comunicación y adapta al negocio específico. Usá cuando quieras contactar un prospecto encontrado con /prospect.
user-invocable: true
argument-hint: "[nombre del negocio o datos del prospecto]"
---

Generar un mensaje de primer contacto personalizado y listo para enviar.

## Contexto

- **Plantillas base:** `KIT_OPERATIVO/01_PLANTILLAS_COMUNICACION.md`
- **CSVs de prospectos:** `KIT_OPERATIVO/prospectos_*.csv`
- **Demos por sector:** `landing-page/demos/` (restaurante, bodega, alojamiento, peluqueria, profesional, etc.)
- **URL base de demos:** `https://jbarrancogit.github.io/demos/`
- **WhatsApp de Juan:** +54 9 261 642-3730

## Paso 1: Identificar al prospecto

Si el usuario pasó solo un nombre:
1. Buscá en los CSVs de `KIT_OPERATIVO/prospectos_*.csv` (empezando por el más reciente)
2. Encontrá la fila que coincida con el nombre (búsqueda fuzzy: ignorar mayúsculas, acentos)
3. Extraé: Nombre, Teléfono, Rubro, Web actual, Ubicación (link Google Maps)

Si el usuario pasó datos completos (nombre, teléfono, rubro), usá esos directamente.

Si no se encuentra el prospecto, pedile los datos al usuario.

## Paso 2: Seleccionar plantilla

Leé `KIT_OPERATIVO/01_PLANTILLAS_COMUNICACION.md` y elegí la versión más adecuada:

| Rubro del prospecto | Plantilla recomendada |
|---|---|
| restaurant, cafe, bar, fast_food | **Versión C** (gastronomía, menciona menú digital y QR) |
| Cualquier otro | **Versión A** (directa) o **Versión B** (sutil, valor primero) |

Para email, usá la plantilla de la **sección 2** del archivo.

## Paso 3: Personalizar el mensaje

Reemplazá en la plantilla:
- **Nombre del negocio** en el texto (no genérico)
- **Rubro específico** (no decir "tu negocio" sino "tu restaurante", "tu consultorio", etc.)
- **Demo relevante:** incluí el link a la demo del sector → `https://jbarrancogit.github.io/demos/{sector}.html`
- **Dashboard del sector** (si existe): `https://jbarrancogit.github.io/demos/dashboard-{sector}.html`
- **Ubicación:** si sabés la zona, mencionala ("vi que están en Godoy Cruz")

**IMPORTANTE:** No exagerar con las credenciales. Mencionar Globant/Disney UNA sola vez, no repetir.

## Paso 4: Generar link de WhatsApp

Si tenemos teléfono del prospecto:

1. Limpiar el número: quitar espacios, guiones, paréntesis
2. Asegurar formato internacional: `549261XXXXXXX` (Argentina, Mendoza)
3. URL-encodear el mensaje
4. Generar: `https://wa.me/{telefono_limpio}?text={mensaje_encoded}`

Si NO hay teléfono: sugerir visita presencial o búsqueda del teléfono en Google Maps.

## Paso 5: Output

Presentá al usuario:

### Mensaje listo para enviar:
```
[el mensaje personalizado]
```

### Link de WhatsApp:
`https://wa.me/549261XXXXXXX?text=...`
(Click acá para abrir WhatsApp con el mensaje pre-cargado)

### Tips de envío:
- **Mejor horario:** Martes a Jueves, 10-12hs o 15-17hs
- **Evitar:** Lunes temprano, viernes tarde, fines de semana
- **Seguimiento:** Si no responde en 3 días, reenviar con `/followup`

Todo el output en **español argentino**.
