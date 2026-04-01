---
name: onboard-client
description: Orquesta el onboarding completo de un nuevo cliente, desde los datos crudos hasta tener prototipo publicado, contrato base y mensaje de WhatsApp listo. Usá cuando llegue un cliente nuevo y quieras hacer todo de una.
user-invocable: true
argument-hint: "[datos del cliente o JSON]"
---

Ejecutar el flujo completo de onboarding de un nuevo cliente en un solo comando.

## Contexto

Este agente orquesta varios pasos que normalmente se harían por separado. Encadena:
1. Parseo de datos → JSON
2. Ejecución de `new_client.py` (crea carpeta, prototipo, estructura)
3. Deploy del prototipo en GitHub Pages
4. Generación de mensaje de WhatsApp para el cliente

### Scripts y archivos involucrados:
- `scripts/new_client.py --from-json` — Onboarding principal
- `scripts/quick_deploy.py` — Deploy a GitHub Pages
- `scripts/ejemplo-cliente.json` — Formato de referencia
- `documentos/contrato-servicios.docx` — Contrato base
- `clientes/{slug}/` — Directorio que se genera

## Paso 1: Obtener datos del cliente

Aceptá los datos en cualquier formato:
- **JSON pegado:** Parsearlo directamente
- **Texto libre / email de Formspree:** Extraer campos y mapear (ver mapeo en `/intake`)
- **Sin datos:** Pedirle al usuario los campos mínimos obligatorios:
  - Nombre de contacto
  - Teléfono/WhatsApp
  - Email
  - Nombre del negocio
  - Sector/rubro
  - Ubicación
  - Plan (o `starter` si no sabe)

## Paso 2: Generar JSON y ejecutar new_client.py

1. Creá el JSON con el formato correcto (ver `/intake` para mapeo de campos)
2. Escribilo a `scripts/cliente-temp.json`
3. Ejecutá: `python scripts/new_client.py --from-json scripts/cliente-temp.json`
4. Capturá el output para extraer rutas y URLs generadas

## Paso 3: Publicar prototipo

1. Copiá `clientes/{slug}/prototipos/{slug}-v1.html` a `demos/{slug}.html`
2. Ejecutá: `python scripts/quick_deploy.py "Onboard: {negocio_nombre}"`
3. URL resultante: `https://jbarrancogit.github.io/demos/{slug}.html`

## Paso 4: Preparar mensaje para el cliente

Generá un mensaje de WhatsApp para enviarle al cliente con el prototipo:

```
¡Hola {nombre}! Soy Juan Ignacio, el desarrollador web.

Ya tengo listo un primer prototipo visual de tu sitio. Podés verlo acá:
👉 {url_prototipo}

Abrilo desde el celular para ver cómo se va a ver en mobile también.

Contame qué te parece, qué cambiarías y qué te gusta. Con tu feedback armo la versión final.

¡Saludos!
```

Generá el link `wa.me/{telefono}?text={mensaje_encoded}`.

## Paso 5: Resumen final

Mostrá al usuario un resumen completo:

```
═══════════════════════════════════════
  ONBOARDING COMPLETO ✓
═══════════════════════════════════════

  Cliente:     {nombre_contacto}
  Negocio:     {negocio_nombre}
  Plan:        {plan} ({precio})
  Sector:      {sector}

  📁 Carpeta:  clientes/{slug}/
  🌐 Prototipo: {url}
  📄 Contrato:  clientes/{slug}/contrato-{slug}.docx
  📱 WhatsApp:  {wa_link}

  PRÓXIMOS PASOS:
  1. Revisar y ajustar el prototipo
  2. Enviar link al cliente (link de WA arriba)
  3. Esperar feedback y aplicar cambios
  4. Enviar contrato para firma
  5. Cobrar primer pago (50%)
═══════════════════════════════════════
```

Todo el output en **español argentino** (voseo, pesos argentinos, tono profesional y cercano).
