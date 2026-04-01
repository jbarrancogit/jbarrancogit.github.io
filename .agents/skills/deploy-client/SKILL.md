---
name: deploy-client
description: Publica el sitio de un cliente en GitHub Pages. Copia el HTML final a demos/ y ejecuta quick_deploy.py. Usá cuando un prototipo o sitio final esté listo para publicar.
user-invocable: true
argument-hint: "[nombre o slug del cliente]"
---

Publicar el sitio de un cliente en GitHub Pages.

## Contexto

- **Directorio de clientes:** `clientes/{slug}/`
- **Prototipos:** `clientes/{slug}/prototipos/{slug}-v1.html`
- **Entrega final:** `clientes/{slug}/entrega/` (si existe)
- **Directorio de demos público:** `demos/`
- **Script de deploy:** `scripts/quick_deploy.py`
- **URL base:** `https://jbarrancogit.github.io/demos/`

## Paso 1: Identificar al cliente

Si el usuario pasa un nombre, convertilo a slug (minúsculas, sin acentos, guiones en vez de espacios).

Verificá que exista el directorio `clientes/{slug}/`. Si no existe, listá los clientes disponibles.

## Paso 2: Encontrar el HTML a publicar

Buscá en este orden de prioridad:
1. `clientes/{slug}/entrega/*.html` — sitio final (mayor prioridad)
2. `clientes/{slug}/prototipos/{slug}-v*.html` — prototipo (elegir la versión más alta: v2 > v1)

Si no hay ningún HTML, informá al usuario que primero debe generar el prototipo con `/intake` o `new_client.py`.

## Paso 3: Copiar a demos/

1. Copiá el HTML a `demos/{slug}.html`
2. Si ya existe un `demos/{slug}.html`, avisá que se va a sobreescribir

## Paso 4: Deploy

Ejecutá:
```bash
python scripts/quick_deploy.py "Deploy: {negocio_nombre} ({slug})"
```

## Paso 5: Confirmar

Output:
- **URL en vivo:** `https://jbarrancogit.github.io/demos/{slug}.html`
- **Tiempo estimado:** 1-5 minutos para que GitHub Pages actualice
- **Tip:** Para forzar recarga, agregar `?v={timestamp}` a la URL

Sugerí al usuario:
- Verificar el sitio en mobile
- Enviar el link al cliente por WhatsApp con `/outreach`
- Si es prototipo, aclarar que es una preview y no el sitio final

Todo el output en **español argentino**.
