---
name: intake
description: Convierte datos de un formulario de Formspree (email o texto pegado) en un JSON compatible con new_client.py y ejecuta el onboarding automático del cliente. Usá cuando llega un nuevo lead desde la landing page.
user-invocable: true
argument-hint: "[datos del formulario pegados]"
---

Convertir datos de formulario en un cliente onboarded con prototipo y estructura de carpetas.

## Contexto

- **Script de onboarding:** `scripts/new_client.py` — acepta `--from-json archivo.json`
- **Ejemplo de JSON válido:** `scripts/ejemplo-cliente.json`
- **Directorio de clientes:** `clientes/{slug}/`
- **Templates disponibles:** `templates/` (restaurante, bodega, alojamiento, peluquería, profesional)

## Paso 1: Obtener los datos

Si el usuario no pegó datos como argumento, pedile que pegue el contenido del email de Formspree o los datos del cliente. Los campos que llegan del formulario de la landing son:

| Campo del form | Descripción |
|---|---|
| `nombre` | Nombre completo del contacto |
| `telefono` | Teléfono/WhatsApp |
| `email` | Email |
| `negocio_nombre` | Nombre del negocio |
| `rubro` | Sector (gastronomia, bodega, alojamiento, salud, belleza, comercio, profesional, turismo, educacion, otro) |
| `ubicacion` | Localidad, Mendoza |
| `descripcion` | Descripción breve del negocio |
| `horarios` | Horarios de atención |
| `direccion` | Dirección física |
| `plan` | Plan elegido (starter, profesional, premium, analytics_setup, data_pro, data_enterprise, no_se) |
| `secciones` | Secciones deseadas del sitio (checkbox múltiple) |
| `objetivo` | Objetivo del sitio web |
| `contenido` | Material que ya tiene listo |
| `dominio_actual` | Dominio actual (puede estar vacío) |
| `dominio_deseado` | Dominio que quiere |
| `referencias` | Sitios de referencia |
| `colores` | Preferencia de colores (texto libre) |
| `notas` | Notas adicionales |

## Paso 2: Mapear campos y generar JSON

Convertir los datos del formulario al formato que espera `new_client.py`:

```json
{
  "nombre_contacto": "[nombre]",
  "telefono": "[telefono]",
  "email": "[email]",
  "negocio_nombre": "[negocio_nombre]",
  "sector": "[rubro]",
  "ubicacion": "[ubicacion]",
  "descripcion": "[descripcion]",
  "horarios": "[horarios]",
  "direccion": "[direccion]",
  "plan": "[plan]",
  "color_preset": "[inferido de colores]",
  "dominio": "[dominio_deseado]"
}
```

### Mapeo de colores (texto libre → preset)

El campo `colores` del form es texto libre. Mapeá al preset más cercano:

| Palabras clave | Preset |
|---|---|
| azul, blue, moderno, tecnología | `azul` |
| verde, green, natural, eco, orgánico | `verde` |
| rojo, red, energía, pasión | `rojo` |
| dorado, gold, elegante, luxury, premium | `dorado` |
| violeta, purple, morado, creativo | `violeta` |
| teal, turquesa, agua, fresco | `teal` |
| vino, bordo, burgundy, burdeos, granate | `vino` |

Si no podés inferir, usá `azul` como default.

### Plan "no_se"

Si el plan es `no_se`, usá `starter` como default y anotá en las notas que el cliente pidió asesoramiento.

## Paso 3: Guardar JSON y ejecutar onboarding

1. Escribí el JSON a `scripts/cliente-temp.json` usando la herramienta Write
2. Ejecutá: `python scripts/new_client.py --from-json scripts/cliente-temp.json`
3. Leé el output del script para obtener las URLs y datos generados

## Paso 4: Resumen para el usuario

Mostrá un resumen con:

- **Cliente:** nombre y negocio
- **Plan:** plan seleccionado con precio
- **Prototipo:** URL del prototipo en GitHub Pages (si se publicó)
- **Carpeta:** ruta del directorio del cliente en `clientes/`
- **WhatsApp:** link wa.me para enviar mensaje al cliente
- **Próximos pasos:**
  1. Revisar y personalizar el prototipo
  2. Enviar link del prototipo por WhatsApp
  3. Generar contrato con datos del cliente
  4. Agendar llamada de revisión

Todo el output debe ser en **español argentino** (voseo, pesos argentinos).
