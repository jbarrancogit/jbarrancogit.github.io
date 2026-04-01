"""
new_client.py — Automatización del onboarding de clientes.

Uso:
  python scripts/new_client.py                     # Modo interactivo
  python scripts/new_client.py --from-json client.json  # Desde archivo JSON

Qué hace:
  1. Copia el template del sector al directorio de clientes
  2. Reemplaza los datos del CONFIG con la info del cliente
  3. Genera contrato DOCX/PDF con datos pre-llenados
  4. Crea estructura de carpeta del proyecto
  5. (Opcional) Publica prototipo en GitHub Pages
"""

import os
import sys
import json
import shutil
import re
import subprocess
from datetime import datetime
from pathlib import Path

# Fix encoding en Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ── Rutas ──
ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / 'templates'
CLIENTS_DIR = ROOT / 'clientes'
DOCS_DIR = ROOT / 'documentos'

# ── Mapeo sector → template ──
SECTOR_MAP = {
    'gastronomia': 'restaurante-template.html',
    'bodega': 'bodega-template.html',
    'alojamiento': 'alojamiento-template.html',
    'belleza': 'peluqueria-template.html',
    'salud': 'profesional-template.html',
    'profesional': 'profesional-template.html',
    'comercio': 'profesional-template.html',
    'turismo': 'alojamiento-template.html',
    'educacion': 'profesional-template.html',
    'otro': 'profesional-template.html',
}

PLAN_PRICES = {
    'starter': {'ars': '$79.200', 'usd': '~USD 65', 'list': '$99.000'},
    'profesional': {'ars': '$224.000', 'usd': '~USD 185', 'list': '$280.000'},
    'premium': {'ars': '$384.000', 'usd': '~USD 320', 'list': '$480.000'},
    'analytics_setup': {'ars': '$44.000', 'usd': '~USD 35', 'list': '$55.000'},
    'data_pro': {'ars': '$152.000', 'usd': '~USD 125', 'list': '$190.000'},
    'data_enterprise': {'ars': 'a convenir', 'usd': '~USD 250+', 'list': 'a convenir'},
}

# ── Paletas de colores predefinidas ──
COLOR_PRESETS = {
    'azul': {
        'accent': '#3b82f6', 'accentLight': '#60a5fa',
        'accentDark': '#2563eb', 'bgDark': '#09090b',
    },
    'verde': {
        'accent': '#22c55e', 'accentLight': '#4ade80',
        'accentDark': '#16a34a', 'bgDark': '#0a0f0d',
    },
    'rojo': {
        'accent': '#ef4444', 'accentLight': '#f87171',
        'accentDark': '#dc2626', 'bgDark': '#0f0909',
    },
    'dorado': {
        'accent': '#D4A853', 'accentLight': '#E8C97A',
        'accentDark': '#B08A3A', 'bgDark': '#0D0A0C',
    },
    'violeta': {
        'accent': '#8b5cf6', 'accentLight': '#a78bfa',
        'accentDark': '#7c3aed', 'bgDark': '#0b0a10',
    },
    'teal': {
        'accent': '#14b8a6', 'accentLight': '#2dd4bf',
        'accentDark': '#0d9488', 'bgDark': '#0a0f0e',
    },
    'vino': {
        'accent': '#8B1A4A', 'accentLight': '#A8325E',
        'accentDark': '#5E0F32', 'bgDark': '#0D0A0C',
    },
}


def slugify(text):
    """Convierte texto a slug para nombre de carpeta/archivo."""
    text = text.lower().strip()
    text = re.sub(r'[áàä]', 'a', text)
    text = re.sub(r'[éèë]', 'e', text)
    text = re.sub(r'[íìï]', 'i', text)
    text = re.sub(r'[óòö]', 'o', text)
    text = re.sub(r'[úùü]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def prompt_input(label, default=None, required=True):
    """Prompt interactivo con default."""
    suffix = f' [{default}]' if default else ''
    suffix += ' *' if required else ''
    val = input(f'  {label}{suffix}: ').strip()
    if not val and default:
        return default
    if not val and required:
        print(f'    ⚠ Campo obligatorio.')
        return prompt_input(label, default, required)
    return val


def prompt_choice(label, options):
    """Selector de opciones."""
    print(f'\n  {label}:')
    for i, (key, desc) in enumerate(options.items(), 1):
        print(f'    {i}. {desc}')
    while True:
        val = input('  Elegí (número): ').strip()
        try:
            idx = int(val) - 1
            if 0 <= idx < len(options):
                return list(options.keys())[idx]
        except ValueError:
            if val in options:
                return val
        print('    ⚠ Opción inválida.')


def gather_interactive():
    """Recolecta datos del cliente de forma interactiva."""
    print('\n' + '='*60)
    print('  NUEVO CLIENTE — Onboarding')
    print('='*60)

    data = {}

    # 1. Datos del cliente
    print('\n📋 Datos del cliente')
    data['nombre_contacto'] = prompt_input('Nombre completo')
    data['telefono'] = prompt_input('Teléfono/WhatsApp', default='+54 9 261 ')
    data['email'] = prompt_input('Email')

    # 2. Datos del negocio
    print('\n🏪 Datos del negocio')
    data['negocio_nombre'] = prompt_input('Nombre del negocio')
    data['sector'] = prompt_choice('Sector', {
        'gastronomia': 'Gastronomía',
        'bodega': 'Bodega / Viñedo',
        'alojamiento': 'Alojamiento',
        'salud': 'Salud',
        'belleza': 'Belleza / Peluquería',
        'comercio': 'Comercio',
        'profesional': 'Servicios profesionales',
        'turismo': 'Turismo',
        'educacion': 'Educación',
        'otro': 'Otro',
    })
    data['ubicacion'] = prompt_input('Ubicación', default='Mendoza')
    data['descripcion'] = prompt_input('Descripción breve del negocio')
    data['horarios'] = prompt_input('Horarios', required=False)
    data['direccion'] = prompt_input('Dirección', required=False)

    # 3. Plan
    print('\n💰 Plan')
    data['plan'] = prompt_choice('Plan contratado', {
        'starter': 'Starter ($79.200)',
        'profesional': 'Profesional ($224.000)',
        'premium': 'Premium ($384.000)',
        'analytics_setup': 'Analytics Setup ($44.000)',
        'data_pro': 'Data Pro ($152.000)',
        'data_enterprise': 'Data Enterprise (a convenir)',
    })

    # 4. Estilo
    print('\n🎨 Estilo')
    data['color_preset'] = prompt_choice('Paleta de colores', {
        'azul': 'Azul (moderno)',
        'verde': 'Verde (natural)',
        'rojo': 'Rojo (energético)',
        'dorado': 'Dorado (elegante)',
        'violeta': 'Violeta (creativo)',
        'teal': 'Teal (fresco)',
        'vino': 'Vino (premium)',
    })

    # 5. Dominio
    data['dominio'] = prompt_input('Dominio deseado', required=False)

    # Metadata
    data['fecha_inicio'] = datetime.now().strftime('%Y-%m-%d')
    data['slug'] = slugify(data['negocio_nombre'])

    return data


def gather_from_json(path):
    """Lee datos de un archivo JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Agregar campos computados
    if 'slug' not in data:
        data['slug'] = slugify(data.get('negocio_nombre', 'cliente'))
    if 'fecha_inicio' not in data:
        data['fecha_inicio'] = datetime.now().strftime('%Y-%m-%d')
    return data


def create_project_structure(data):
    """Crea la carpeta del proyecto del cliente."""
    client_dir = CLIENTS_DIR / data['slug']
    client_dir.mkdir(parents=True, exist_ok=True)

    # Subcarpetas
    (client_dir / 'contenido').mkdir(exist_ok=True)
    (client_dir / 'prototipos').mkdir(exist_ok=True)
    (client_dir / 'entrega').mkdir(exist_ok=True)

    # Guardar JSON de referencia
    with open(client_dir / 'datos-cliente.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # README del proyecto
    plan_info = PLAN_PRICES.get(data['plan'], {})
    with open(client_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(f"""# {data['negocio_nombre']}

**Cliente:** {data['nombre_contacto']}
**Contacto:** {data['telefono']} · {data['email']}
**Sector:** {data['sector']}
**Plan:** {data['plan']} ({plan_info.get('ars', '')})
**Fecha inicio:** {data['fecha_inicio']}

## Estado
- [ ] Contenido recibido
- [ ] Prototipo enviado
- [ ] Prototipo aprobado
- [ ] Contrato firmado
- [ ] Primer pago recibido
- [ ] Desarrollo en curso
- [ ] Sitio entregado
- [ ] Pago completo

## Archivos
- `datos-cliente.json` — Datos del formulario
- `prototipos/` — Versiones del prototipo
- `contenido/` — Textos, fotos, logo del cliente
- `entrega/` — Archivos finales

## Notas
_Agregar notas del proyecto acá._
""")

    print(f'\n  ✅ Carpeta creada: clientes/{data["slug"]}/')
    return client_dir


def generate_prototype(data, client_dir):
    """Copia y personaliza el template para el cliente."""
    template_file = SECTOR_MAP.get(data['sector'], 'profesional-template.html')
    template_path = TEMPLATES_DIR / template_file

    if not template_path.exists():
        print(f'  ⚠ Template no encontrado: {template_file}')
        return None

    # Leer template
    content = template_path.read_text(encoding='utf-8')

    # Reemplazar nombre del negocio en el CONFIG
    # Los templates usan CONFIG.nombre como primer campo
    negocio = data['negocio_nombre']

    # Reemplazar el nombre en el CONFIG (primer string después de "nombre:")
    content = re.sub(
        r"(nombre:\s*['\"])([^'\"]+)(['\"])",
        f"\\g<1>{negocio}\\3",
        content,
        count=1
    )

    # Reemplazar slogan si hay descripción
    if data.get('descripcion'):
        desc_short = data['descripcion'][:80]
        content = re.sub(
            r"(slogan:\s*['\"])([^'\"]+)(['\"])",
            f"\\g<1>{desc_short}\\3",
            content,
            count=1
        )

    # Reemplazar WhatsApp
    wa_number = re.sub(r'[^0-9]', '', data.get('telefono', ''))
    if not wa_number:
        wa_number = '5492616423730'  # Default: Juan
    content = re.sub(
        r"(whatsapp:\s*['\"])([^'\"]+)(['\"])",
        f"\\g<1>{wa_number}\\3",
        content,
        count=1
    )

    # Reemplazar colores si el template tiene CONFIG.colores
    colors = COLOR_PRESETS.get(data.get('color_preset', 'azul'), COLOR_PRESETS['azul'])
    for key, value in colors.items():
        # Reemplazar en el CONFIG JS object
        content = re.sub(
            rf"({key}:\s*['\"])([^'\"]+)(['\"])",
            f"\\g<1>{value}\\3",
            content
        )

    # Guardar prototipo
    proto_filename = f'{data["slug"]}-v1.html'
    proto_path = client_dir / 'prototipos' / proto_filename
    proto_path.write_text(content, encoding='utf-8')

    # También copiar a demos/ para preview en GitHub Pages
    demo_path = ROOT / 'demos' / f'{data["slug"]}.html'
    demo_path.write_text(content, encoding='utf-8')

    print(f'  ✅ Prototipo generado: clientes/{data["slug"]}/prototipos/{proto_filename}')
    print(f'  ✅ Demo publicable:    demos/{data["slug"]}.html')
    return proto_path


def generate_contract(data, client_dir):
    """Genera contrato pre-llenado con datos del cliente."""
    # Importar el generador existente
    sys.path.insert(0, str(DOCS_DIR))

    plan_info = PLAN_PRICES.get(data['plan'], {})

    # Crear un JSON con los datos para el contrato
    contract_data = {
        'cliente_nombre': data['nombre_contacto'],
        'cliente_email': data['email'],
        'cliente_telefono': data['telefono'],
        'negocio_nombre': data['negocio_nombre'],
        'sector': data['sector'],
        'plan': data['plan'],
        'precio': plan_info.get('ars', 'a convenir'),
        'fecha': datetime.now().strftime('%d/%m/%Y'),
    }

    contract_json = client_dir / 'contrato-datos.json'
    with open(contract_json, 'w', encoding='utf-8') as f:
        json.dump(contract_data, f, ensure_ascii=False, indent=2)

    # Copiar DOCX y PDF base al directorio del cliente
    for ext in ['docx', 'pdf']:
        src = DOCS_DIR / f'contrato-servicios.{ext}'
        dst = client_dir / f'contrato-{data["slug"]}.{ext}'
        if src.exists():
            shutil.copy2(src, dst)

    print(f'  ✅ Contrato base copiado a: clientes/{data["slug"]}/')
    print(f'  ✅ Datos del contrato:      clientes/{data["slug"]}/contrato-datos.json')
    print(f'     → Completar datos del cliente en el DOCX y firmar.')
    return contract_json


def deploy_prototype(data):
    """Push del prototipo a GitHub Pages."""
    demo_file = ROOT / 'demos' / f'{data["slug"]}.html'
    if not demo_file.exists():
        print('  ⚠ No hay demo para publicar.')
        return

    print(f'\n  📤 Publicando prototipo...')
    try:
        subprocess.run(['git', 'add', str(demo_file)], cwd=str(ROOT), check=True)
        msg = f'Agregar prototipo: {data["negocio_nombre"]}'
        subprocess.run(['git', 'commit', '-m', msg], cwd=str(ROOT), check=True)
        subprocess.run(['git', 'push'], cwd=str(ROOT), check=True)
        url = f'https://jbarrancogit.github.io/demos/{data["slug"]}.html'
        print(f'  ✅ Publicado: {url}')
        return url
    except subprocess.CalledProcessError as e:
        print(f'  ⚠ Error en git: {e}')
        return None


def print_summary(data, client_dir, url=None):
    """Resumen final del onboarding."""
    plan_info = PLAN_PRICES.get(data['plan'], {})

    print('\n' + '='*60)
    print('  ✅ ONBOARDING COMPLETO')
    print('='*60)
    print(f'''
  Cliente:    {data['nombre_contacto']}
  Negocio:    {data['negocio_nombre']}
  Plan:       {data['plan']} ({plan_info.get('ars', '')})
  Sector:     {data['sector']}
  Carpeta:    clientes/{data['slug']}/

  Archivos generados:
    📁 clientes/{data['slug']}/
    ├── README.md              ← Checklist del proyecto
    ├── datos-cliente.json     ← Datos completos
    ├── contrato-datos.json    ← Datos para contrato
    ├── contrato-*.docx/pdf    ← Contrato base
    ├── prototipos/
    │   └── {data['slug']}-v1.html
    ├── contenido/             ← Pedir al cliente
    └── entrega/               ← Archivos finales
''')

    if url:
        print(f'  🔗 Prototipo online: {url}')

    # Mensaje de WhatsApp sugerido
    wa_msg = (
        f'Hola {data["nombre_contacto"].split()[0]}! Soy Juan Barranco. '
        f'Ya tengo listo el prototipo de {data["negocio_nombre"]}. '
        f'Podés verlo acá: https://jbarrancogit.github.io/demos/{data["slug"]}.html '
        f'Contame qué te parece!'
    )
    wa_number = re.sub(r'[^0-9]', '', data.get('telefono', ''))
    if wa_number:
        print(f'  💬 WhatsApp sugerido:')
        print(f'     https://wa.me/{wa_number}?text={wa_msg.replace(" ", "%20")}')

    print(f'\n  📋 Próximos pasos:')
    print(f'     1. Revisar el prototipo generado')
    print(f'     2. Ajustar textos/imágenes del CONFIG')
    print(f'     3. Enviar link al cliente por WhatsApp')
    print(f'     4. Si aprueba → completar contrato y cobrar 50%')
    print()


def main():
    # Parsear argumentos
    if '--from-json' in sys.argv:
        idx = sys.argv.index('--from-json')
        json_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if not json_path or not os.path.exists(json_path):
            print('  ⚠ Archivo JSON no encontrado.')
            sys.exit(1)
        data = gather_from_json(json_path)
    else:
        data = gather_interactive()

    # Confirmar
    print(f'\n  → Creando proyecto para: {data["negocio_nombre"]} ({data["sector"]})')

    # 1. Estructura de carpetas
    client_dir = create_project_structure(data)

    # 2. Generar prototipo
    generate_prototype(data, client_dir)

    # 3. Generar contrato
    generate_contract(data, client_dir)

    # 4. Preguntar si publicar
    deploy_url = None
    if '--deploy' in sys.argv:
        deploy_url = deploy_prototype(data)
    else:
        resp = input('\n  ¿Publicar prototipo en GitHub Pages? (s/N): ').strip().lower()
        if resp in ('s', 'si', 'sí', 'y', 'yes'):
            deploy_url = deploy_prototype(data)

    # 5. Resumen
    print_summary(data, client_dir, deploy_url)


if __name__ == '__main__':
    main()
