"""
Genera contrato-servicios.docx y contrato-servicios.pdf
con formato profesional.
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── helpers ──────────────────────────────────────────────

def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    shading = cell._element.get_or_add_tcPr()
    shd = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): color_hex,
    })
    shading.append(shd)


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x5f)
    return h


def add_paragraph_justified(doc, text, bold=False, italic=False, size=10.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = Pt(14)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Calibri'
    run.bold = bold
    run.italic = italic
    return p


def add_checkbox_line(doc, text, checked=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5)
    mark = '\u2611' if checked else '\u2610'
    run = p.add_run(f'{mark}  {text}')
    run.font.size = Pt(10.5)
    run.font.name = 'Calibri'
    return p


def add_blank_field(doc, label, width_chars=40):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f'{label}: ')
    run.font.size = Pt(10.5)
    run.font.name = 'Calibri'
    run.bold = True
    run2 = p.add_run('_' * width_chars)
    run2.font.size = Pt(10.5)
    run2.font.name = 'Calibri'
    run2.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(1.0 + level * 0.8)
    for run in p.runs:
        run.font.size = Pt(10.5)
        run.font.name = 'Calibri'
    return p


# ── build DOCX ───────────────────────────────────────────

def build_docx():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10.5)

    # ── Title ──
    title = doc.add_heading('CONTRATO DE LOCACIÓN DE SERVICIOS\nDE DESARROLLO WEB', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x5f)
        run.font.size = Pt(18)

    # ── Separator ──
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('━' * 60)
    run.font.color.rgb = RGBColor(0x3b, 0x82, 0xf6)
    run.font.size = Pt(8)

    # ── Parties ──
    add_heading_styled(doc, 'Partes', level=2)

    add_paragraph_justified(doc,
        'EL PRESTADOR: Juan Ignacio Barranco, DNI N.° ____________, '
        'con domicilio en Maipú, Mendoza, correo electrónico jbarranco.sistemas@gmail.com, '
        'teléfono +54 9 261 642-3730, en adelante "EL DESARROLLADOR".')

    add_paragraph_justified(doc,
        'EL COMITENTE: ____________________________________________, '
        'DNI/CUIT N.° ____________, con domicilio comercial en '
        '____________________________________________, correo electrónico '
        '________________________, teléfono ________________________, en adelante "EL CLIENTE".')

    add_paragraph_justified(doc,
        'En la ciudad de Mendoza, a los ______ días del mes de ______________ de 20____, '
        'las partes acuerdan celebrar el presente contrato de locación de servicios conforme '
        'a los artículos 1251 a 1261 del Código Civil y Comercial de la Nación, sujeto a las '
        'siguientes cláusulas:')

    # ── CLÁUSULA 1 ──
    add_heading_styled(doc, 'Cláusula Primera — Objeto', level=2)
    add_paragraph_justified(doc,
        'El Desarrollador se compromete a diseñar, desarrollar y entregar al Cliente un sitio '
        'web profesional según las especificaciones detalladas en el Anexo A — Alcance del '
        'proyecto, que forma parte integrante de este contrato.')
    p = add_paragraph_justified(doc, 'El plan contratado es:')
    add_checkbox_line(doc, 'Starter ($99.000)')
    add_checkbox_line(doc, 'Profesional ($280.000)')
    add_checkbox_line(doc, 'Premium ($480.000)')

    # ── CLÁUSULA 2 ──
    add_heading_styled(doc, 'Cláusula Segunda — Alcance y exclusiones', level=2)
    add_paragraph_justified(doc, '2.1. Incluye:', bold=True)
    add_paragraph_justified(doc,
        'El trabajo comprende exclusivamente lo detallado en el Anexo A. '
        'A modo de referencia según el plan contratado:')

    add_paragraph_justified(doc, 'Plan Starter ($99.000):', bold=True)
    for item in [
        'Sitio web profesional a medida (hasta 5 secciones)',
        'Diseño responsive (celular, PC, tablet)',
        'Formulario de contacto funcional',
        'Botón de WhatsApp',
        'Configuración de Google My Business',
        'SEO básico (meta tags, estructura, schema local)',
        'Configuración de Google Analytics 4',
        'Registro de dominio .com.ar (primer año)',
        'Publicación en hosting sin costo mensual',
    ]:
        add_bullet(doc, item)

    add_paragraph_justified(doc, 'Plan Profesional ($280.000) — incluye todo lo anterior más:', bold=True)
    for item in [
        'Sitio de 5 o más secciones',
        'Sistema de reservas o turnos online integrado',
        'SEO avanzado + configuración completa de Google Analytics',
        'Capacitación básica para gestionar contenido',
    ]:
        add_bullet(doc, item)

    add_paragraph_justified(doc, 'Plan Premium ($480.000) — incluye todo lo anterior más:', bold=True)
    for item in [
        'Catálogo de productos/servicios con integración de Mercado Pago',
        'Versión bilingüe del sitio (español e inglés)',
        'Configuración avanzada de Google Analytics con eventos personalizados',
        'Formularios inteligentes con notificaciones automáticas por email',
    ]:
        add_bullet(doc, item)

    add_paragraph_justified(doc, '2.2. No incluye (salvo acuerdo escrito por separado):', bold=True)
    for item in [
        'Creación de contenido (textos, fotografías, logotipo) — el Cliente los provee',
        'Redacción o traducción de textos más allá de lo indicado en el plan',
        'Gestión de redes sociales',
        'Campañas de publicidad (Google Ads, Meta Ads, etc.)',
        'Funcionalidades no especificadas en el Anexo A',
        'Desarrollo de aplicaciones móviles nativas',
        'Integraciones con sistemas de terceros no mencionados',
        'Servicios de ingeniería de datos (pipelines, data warehouses) — se presupuestan a medida',
    ]:
        add_bullet(doc, item)

    # ── CLÁUSULA 3 ──
    add_heading_styled(doc, 'Cláusula Tercera — Precio y forma de pago', level=2)
    add_blank_field(doc, 'Precio total', 30)
    add_paragraph_justified(doc, 'Forma de pago acordada:')
    add_checkbox_line(doc, 'Pago único: 50% al aprobar el prototipo, 50% al recibir el sitio terminado.')
    add_checkbox_line(doc, '3 cuotas de $__________ cada una. Primera al aprobar el prototipo, las siguientes a 30 y 60 días.')
    add_checkbox_line(doc, 'Otra: ____________________________________________')
    add_paragraph_justified(doc,
        'Medios de pago aceptados: transferencia bancaria, efectivo, Mercado Pago.')
    add_paragraph_justified(doc,
        'El Desarrollador no emite factura fiscal al momento de la firma del presente contrato. '
        'Si en el futuro se inscribiera como contribuyente, podrá emitir el comprobante correspondiente. '
        'Esto no afecta la validez del presente contrato ni las obligaciones asumidas por las partes.')
    add_paragraph_justified(doc,
        'La falta de pago en los plazos acordados habilita al Desarrollador a suspender el trabajo '
        'en curso y retener la entrega de archivos hasta su regularización.')

    # ── CLÁUSULA 4 ──
    add_heading_styled(doc, 'Cláusula Cuarta — Plazos', level=2)
    add_paragraph_justified(doc,
        'Prototipo visual: El Desarrollador entregará un prototipo visual navegable dentro de las '
        '48 horas hábiles siguientes a la recepción del contenido completo por parte del Cliente.')
    add_paragraph_justified(doc, 'Sitio terminado (desde aprobación del prototipo):')
    add_bullet(doc, 'Plan Starter: 7 (siete) días hábiles')
    add_bullet(doc, 'Plan Profesional: 14 (catorce) días hábiles')
    add_bullet(doc, 'Plan Premium: 21 (veintiún) días hábiles')
    add_paragraph_justified(doc,
        'Los plazos se computan desde que el Cliente provee la totalidad del contenido y aprueba '
        'el prototipo. Demoras atribuibles al Cliente (falta de respuesta, contenido incompleto, '
        'cambios de alcance) suspenden el cómputo del plazo.')
    add_paragraph_justified(doc,
        'El Cliente dispone de 2 (dos) rondas de revisión incluidas en el precio. Cambios de '
        'estructura, funcionalidad o alcance se consideran trabajo adicional.')

    # ── CLÁUSULA 5 ──
    add_heading_styled(doc, 'Cláusula Quinta — Obligaciones del Cliente', level=2)
    add_paragraph_justified(doc, 'El Cliente se compromete a:')
    add_bullet(doc, 'Proveer todo el contenido necesario dentro de los 5 días hábiles posteriores a la firma.')
    add_bullet(doc, 'Designar una persona de contacto con capacidad de decisión.')
    add_bullet(doc, 'Responder consultas del Desarrollador en un plazo no mayor a 3 días hábiles.')
    add_bullet(doc, 'Facilitar acceso a cuentas necesarias (Google My Business, dominio, Mercado Pago, etc.).')
    add_bullet(doc, 'Abonar el precio en los plazos convenidos.')

    # ── CLÁUSULA 6 ──
    add_heading_styled(doc, 'Cláusula Sexta — Propiedad intelectual', level=2)
    add_paragraph_justified(doc,
        'Una vez cancelado el 100% del precio, la totalidad del código fuente, diseño, archivos '
        'y contenido desarrollado pasan a ser propiedad exclusiva del Cliente. El Cliente puede '
        'usarlo, modificarlo, transferirlo o contratar a otro desarrollador sin restricción alguna.')
    add_paragraph_justified(doc,
        'El Desarrollador se reserva el derecho de utilizar capturas del sitio en su portfolio '
        'profesional, salvo prohibición expresa por escrito del Cliente.')
    add_paragraph_justified(doc,
        'Las imágenes de stock utilizadas (Unsplash, Pexels, etc.) se rigen por sus propias '
        'licencias de uso libre. El Desarrollador informará qué imágenes se utilizaron.')
    add_paragraph_justified(doc,
        'Hasta la cancelación total del precio, el código fuente permanece bajo propiedad del Desarrollador.')

    # ── CLÁUSULA 7 ──
    add_heading_styled(doc, 'Cláusula Séptima — Soporte post-entrega', level=2)
    add_paragraph_justified(doc, 'Período de soporte incluido según plan:')
    add_bullet(doc, 'Plan Starter: no incluye soporte post-entrega.')
    add_bullet(doc, 'Plan Profesional: 3 (tres) meses desde la entrega.')
    add_bullet(doc, 'Plan Premium: 6 (seis) meses desde la entrega.')
    add_paragraph_justified(doc, 'El soporte incluido cubre:', bold=True)
    add_bullet(doc, 'Corrección de errores técnicos (bugs) del sitio entregado.')
    add_bullet(doc, 'Cambios menores de contenido: textos, precios, fotos e información de contacto.')
    add_bullet(doc, 'Asistencia técnica por consultas relacionadas al sitio.')
    add_paragraph_justified(doc, 'El soporte NO incluye:', bold=True)
    add_bullet(doc, 'Desarrollo de funcionalidades nuevas.')
    add_bullet(doc, 'Rediseño parcial o total del sitio.')
    add_bullet(doc, 'Cambios estructurales (agregar secciones, cambiar arquitectura).')
    add_bullet(doc, 'Gestión de campañas de marketing o redes sociales.')
    add_paragraph_justified(doc,
        'Finalizado el período de soporte, el Cliente puede contratar mantenimiento mensual '
        '(referencia: desde $15.000/mes al momento de la firma).')

    # ── CLÁUSULA 8 ──
    add_heading_styled(doc, 'Cláusula Octava — Hosting y dominio', level=2)
    add_paragraph_justified(doc,
        'El sitio se publicará en una plataforma de hosting profesional sin costo mensual para '
        'sitios estáticos (Vercel, Netlify, GitHub Pages o similar).')
    add_paragraph_justified(doc,
        'Si el proyecto requiere funcionalidades con servidor, el Desarrollador informará el costo '
        'mensual estimado antes de comenzar. Dicho costo será a cargo del Cliente.')
    add_paragraph_justified(doc,
        'El registro del dominio (primer año) está incluido. La renovación anual posterior es '
        'responsabilidad del Cliente. El dominio se registra a nombre del Cliente.')

    # ── CLÁUSULA 9 ──
    add_heading_styled(doc, 'Cláusula Novena — Prototipo gratuito', level=2)
    add_paragraph_justified(doc,
        'El Desarrollador ofrece un prototipo visual sin costo ni compromiso. Si el Cliente decide '
        'no continuar, no tiene obligación de pago. El prototipo es un diseño navegable que muestra '
        'la apariencia del sitio; no constituye el producto terminado. El prototipo y su código '
        'son propiedad del Desarrollador hasta la contratación formal.')

    # ── CLÁUSULA 10 ──
    add_heading_styled(doc, 'Cláusula Décima — Rescisión', level=2)
    add_paragraph_justified(doc,
        'Cualquiera de las partes puede rescindir el contrato mediante notificación escrita '
        '(email con acuse de recibo) con 7 días corridos de preaviso.')
    add_paragraph_justified(doc, 'En caso de rescisión por el Cliente:')
    add_bullet(doc, 'Antes de la aprobación del prototipo: sin costo.')
    add_bullet(doc, 'Después del prototipo: abona el trabajo realizado, mínimo 50% del precio total.')
    add_paragraph_justified(doc,
        'En caso de rescisión por el Desarrollador: reintegrará los montos por trabajo no realizado '
        'dentro de los 15 días hábiles.')
    add_paragraph_justified(doc,
        'El contrato se rescinde de pleno derecho si el Cliente no provee contenido dentro de los '
        '30 días corridos desde la firma, salvo acuerdo en contrario.')

    # ── CLÁUSULA 11 ──
    add_heading_styled(doc, 'Cláusula Undécima — Confidencialidad', level=2)
    add_paragraph_justified(doc,
        'Ambas partes se comprometen a mantener confidencial toda información del otro que no sea '
        'de conocimiento público, incluyendo datos comerciales, estrategias, información de clientes '
        'y documentación intercambiada durante la ejecución del contrato.')

    # ── CLÁUSULA 12 ──
    add_heading_styled(doc, 'Cláusula Duodécima — Responsabilidad', level=2)
    add_paragraph_justified(doc,
        'El Desarrollador garantiza que el sitio funcionará correctamente según las especificaciones '
        'al momento de la entrega.')
    add_paragraph_justified(doc, 'El Desarrollador no es responsable por:')
    add_bullet(doc, 'Contenido provisto por el Cliente que infrinja derechos de terceros.')
    add_bullet(doc, 'Interrupciones causadas por la plataforma de hosting de terceros.')
    add_bullet(doc, 'Resultados comerciales del sitio (ventas, posicionamiento, tráfico).')
    add_bullet(doc, 'Cambios realizados por el Cliente o terceros en el código post-entrega.')
    add_paragraph_justified(doc,
        'La responsabilidad total del Desarrollador se limita al monto efectivamente percibido.')

    # ── CLÁUSULA 13 ──
    add_heading_styled(doc, 'Cláusula Decimotercera — Resolución de conflictos', level=2)
    add_paragraph_justified(doc,
        'Para cualquier controversia, las partes se someten a la jurisdicción de los Tribunales '
        'Ordinarios de la ciudad de Mendoza, Provincia de Mendoza, República Argentina, renunciando '
        'a cualquier otro fuero o jurisdicción.')

    # ── CLÁUSULA 14 ──
    add_heading_styled(doc, 'Cláusula Decimocuarta — Disposiciones generales', level=2)
    add_paragraph_justified(doc,
        'El presente contrato constituye el acuerdo completo entre las partes y reemplaza cualquier '
        'acuerdo previo. Cualquier modificación debe constar por escrito. La nulidad de alguna '
        'cláusula no afecta las restantes. Se rige por las leyes de la República Argentina.')

    # ── Signatures ──
    doc.add_paragraph()
    add_paragraph_justified(doc,
        'En prueba de conformidad, se firman dos ejemplares de un mismo tenor y a un solo efecto.')
    doc.add_paragraph()
    doc.add_paragraph()

    # Signature table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.columns[0].width = Cm(7.5)
    table.columns[1].width = Cm(7.5)

    table.cell(0, 0).text = 'EL DESARROLLADOR'
    table.cell(0, 1).text = 'EL CLIENTE'
    table.cell(1, 0).text = ''
    table.cell(1, 1).text = ''
    table.cell(2, 0).text = '_________________________'
    table.cell(2, 1).text = '_________________________'
    table.cell(3, 0).text = 'Juan Ignacio Barranco\nDNI: _________________'
    table.cell(3, 1).text = 'Nombre: _______________\nDNI/CUIT: _____________'

    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.size = Pt(10.5)
                    run.font.name = 'Calibri'
            if row == table.rows[0]:
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.bold = True

    # ── Page break → Anexo A ──
    doc.add_page_break()

    title_a = doc.add_heading('ANEXO A — Alcance del proyecto', level=1)
    for run in title_a.runs:
        run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x5f)

    add_blank_field(doc, 'Nombre del negocio', 40)
    add_blank_field(doc, 'Rubro', 40)
    doc.add_paragraph()
    add_paragraph_justified(doc, 'Plan contratado:')
    add_checkbox_line(doc, 'Starter')
    add_checkbox_line(doc, 'Profesional')
    add_checkbox_line(doc, 'Premium')
    doc.add_paragraph()
    add_paragraph_justified(doc, 'Descripción del sitio:')
    for _ in range(3):
        add_paragraph_justified(doc, '_' * 80)
    doc.add_paragraph()
    add_paragraph_justified(doc, 'Secciones incluidas:', bold=True)
    for s in [
        'Página principal (hero, presentación)',
        'Sobre nosotros / Historia',
        'Servicios / Productos / Menú / Carta',
        'Galería de fotos',
        'Sistema de reservas / turnos online',
        'Catálogo con integración de pagos (Mercado Pago)',
        'Formulario de contacto',
        'Testimonios / Reseñas',
        'Ubicación y horarios',
        'Versión en inglés',
    ]:
        add_checkbox_line(doc, s)
    add_checkbox_line(doc, 'Otra: ________________________________________')

    doc.add_paragraph()
    add_paragraph_justified(doc, 'Funcionalidades especiales:')
    for _ in range(2):
        add_paragraph_justified(doc, '_' * 80)

    doc.add_paragraph()
    add_blank_field(doc, 'Dominio deseado', 35)

    doc.add_paragraph()
    add_paragraph_justified(doc, 'Contenido a cargo del Cliente:', bold=True)
    for item in [
        'Textos y descripciones',
        'Fotografías propias',
        'Logotipo',
        'Información de contacto y horarios',
        'Lista de productos/servicios con precios',
    ]:
        add_checkbox_line(doc, item)

    doc.add_paragraph()
    add_blank_field(doc, 'Fecha límite de entrega de contenido', 20)

    doc.add_paragraph()
    add_paragraph_justified(doc, 'Notas adicionales:')
    for _ in range(3):
        add_paragraph_justified(doc, '_' * 80)

    # ── Save ──
    path = os.path.join(OUT_DIR, 'contrato-servicios.docx')
    doc.save(path)
    print(f'DOCX saved: {path}')
    return path


# ── build PDF ────────────────────────────────────────────

def build_pdf():
    from fpdf import FPDF

    FONT_DIR = 'C:/Windows/Fonts/'

    class ContratoPDF(FPDF):
        def __init__(self):
            super().__init__()
            self.add_font('Cal', '', FONT_DIR + 'calibri.ttf', uni=True)
            self.add_font('Cal', 'B', FONT_DIR + 'calibrib.ttf', uni=True)
            self.add_font('Cal', 'I', FONT_DIR + 'calibrii.ttf', uni=True)
            self.add_font('Cal', 'BI', FONT_DIR + 'calibriz.ttf', uni=True)

        def header(self):
            if self.page_no() == 1:
                return
            self.set_font('Cal', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, 'Contrato de Locación de Servicios — Juan Barranco', align='C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Cal', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'Página {self.page_no()}/{self.pages_count}', align='C')

        def section_title(self, text):
            self.ln(4)
            self.set_font('Cal', 'B', 12)
            self.set_text_color(30, 58, 95)
            self.multi_cell(0, 7, text)
            self.ln(2)

        def body_text(self, text):
            self.set_font('Cal', '', 10)
            self.set_text_color(40, 40, 40)
            self.multi_cell(0, 5.5, text)
            self.ln(2)

        def bold_text(self, text):
            self.set_font('Cal', 'B', 10)
            self.set_text_color(40, 40, 40)
            self.multi_cell(0, 5.5, text)
            self.ln(1)

        def bullet(self, text):
            self.set_font('Cal', '', 10)
            self.set_text_color(40, 40, 40)
            x = self.get_x()
            self.cell(6, 5.5, '•')
            self.multi_cell(0, 5.5, text)
            self.ln(1)

        def checkbox(self, text):
            self.set_font('Cal', '', 10)
            self.cell(6, 5.5, '\u2610')
            self.cell(0, 5.5, f'  {text}')
            self.ln(6)

        def field_line(self, label, width=120):
            self.set_font('Cal', 'B', 10)
            self.cell(40, 6, f'{label}: ')
            self.set_font('Cal', '', 10)
            self.set_draw_color(180, 180, 180)
            x = self.get_x()
            y = self.get_y() + 5
            self.line(x, y, x + width, y)
            self.ln(8)

    pdf = ContratoPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font('Cal', 'B', 20)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'CONTRATO DE LOCACIÓN DE SERVICIOS', align='C')
    pdf.ln(10)
    pdf.set_font('Cal', 'B', 14)
    pdf.cell(0, 10, 'DE DESARROLLO WEB', align='C')
    pdf.ln(8)
    # Blue line
    pdf.set_draw_color(59, 130, 246)
    pdf.set_line_width(0.5)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(8)

    # Parties
    pdf.section_title('Partes')
    pdf.body_text(
        'EL PRESTADOR: Juan Ignacio Barranco, DNI N.° ____________, '
        'con domicilio en Maipú, Mendoza, correo electrónico jbarranco.sistemas@gmail.com, '
        'teléfono +54 9 261 642-3730, en adelante "EL DESARROLLADOR".')
    pdf.body_text(
        'EL COMITENTE: ____________________________________________, '
        'DNI/CUIT N.° ____________, con domicilio comercial en '
        '____________________________________________, correo electrónico '
        '________________________, teléfono ________________________, en adelante "EL CLIENTE".')
    pdf.body_text(
        'En la ciudad de Mendoza, a los ______ días del mes de ______________ de 20____, '
        'las partes acuerdan celebrar el presente contrato de locación de servicios conforme '
        'a los artículos 1251 a 1261 del Código Civil y Comercial de la Nación.')

    # Clause 1
    pdf.section_title('Cláusula Primera — Objeto')
    pdf.body_text(
        'El Desarrollador se compromete a diseñar, desarrollar y entregar al Cliente un sitio '
        'web profesional según las especificaciones del Anexo A — Alcance del proyecto.')
    pdf.body_text('Plan contratado:')
    pdf.checkbox('Starter ($99.000)')
    pdf.checkbox('Profesional ($280.000)')
    pdf.checkbox('Premium ($480.000)')

    # Clause 2
    pdf.section_title('Cláusula Segunda — Alcance y exclusiones')
    pdf.bold_text('2.1. Incluye:')
    pdf.bold_text('Plan Starter ($99.000):')
    for item in [
        'Sitio web profesional a medida (hasta 5 secciones)',
        'Diseño responsive (celular, PC, tablet)',
        'Formulario de contacto funcional + botón de WhatsApp',
        'Google My Business optimizado + SEO básico',
        'Google Analytics 4 configurado',
        'Dominio .com.ar primer año + hosting sin costo mensual',
    ]:
        pdf.bullet(item)

    pdf.bold_text('Plan Profesional ($280.000) — todo lo anterior más:')
    for item in [
        'Sitio de 5+ secciones',
        'Sistema de reservas o turnos online integrado',
        'SEO avanzado + Google Analytics completo',
        'Capacitación para gestionar contenido',
    ]:
        pdf.bullet(item)

    pdf.bold_text('Plan Premium ($480.000) — todo lo anterior más:')
    for item in [
        'Catálogo con integración de Mercado Pago',
        'Versión bilingüe (español e inglés)',
        'Google Analytics avanzado con eventos personalizados',
        'Formularios inteligentes con notificaciones automáticas',
    ]:
        pdf.bullet(item)

    pdf.bold_text('2.2. No incluye:')
    for item in [
        'Creación de contenido (textos, fotos, logo) — el Cliente los provee',
        'Gestión de redes sociales ni campañas de publicidad',
        'Funcionalidades no especificadas en el Anexo A',
        'Aplicaciones móviles nativas',
        'Servicios de ingeniería de datos — se presupuestan a medida',
    ]:
        pdf.bullet(item)

    # Clause 3
    pdf.section_title('Cláusula Tercera — Precio y forma de pago')
    pdf.field_line('Precio total')
    pdf.body_text('Forma de pago:')
    pdf.checkbox('50% al aprobar prototipo, 50% al entregar')
    pdf.checkbox('3 cuotas de $__________ (primera al aprobar prototipo)')
    pdf.checkbox('Otra: ________________________________________')
    pdf.body_text('Medios: transferencia bancaria, efectivo, Mercado Pago.')
    pdf.body_text(
        'El Desarrollador no emite factura fiscal al momento de la firma. '
        'La falta de pago habilita a suspender el trabajo y retener archivos.')

    # Clause 4
    pdf.section_title('Cláusula Cuarta — Plazos')
    pdf.body_text('Prototipo visual: 48 horas hábiles desde recepción del contenido completo.')
    pdf.body_text('Sitio terminado (desde aprobación del prototipo):')
    pdf.bullet('Starter: 7 días hábiles')
    pdf.bullet('Profesional: 14 días hábiles')
    pdf.bullet('Premium: 21 días hábiles')
    pdf.body_text(
        'Los plazos se suspenden por demoras del Cliente. Se incluyen 2 rondas de revisión; '
        'cambios de estructura o alcance son trabajo adicional.')

    # Clause 5
    pdf.section_title('Cláusula Quinta — Obligaciones del Cliente')
    pdf.bullet('Proveer contenido completo dentro de 5 días hábiles de la firma.')
    pdf.bullet('Designar persona de contacto con capacidad de decisión.')
    pdf.bullet('Responder consultas en máximo 3 días hábiles.')
    pdf.bullet('Facilitar acceso a cuentas necesarias.')
    pdf.bullet('Abonar el precio en los plazos convenidos.')

    # Clause 6
    pdf.section_title('Cláusula Sexta — Propiedad intelectual')
    pdf.body_text(
        'Una vez cancelado el 100% del precio, todo el código, diseño y archivos pasan a ser '
        'propiedad exclusiva del Cliente, sin restricciones. El Desarrollador puede usar capturas '
        'en su portfolio, salvo prohibición escrita. Las imágenes stock se rigen por sus licencias. '
        'Hasta el pago total, el código es propiedad del Desarrollador.')

    # Clause 7
    pdf.section_title('Cláusula Séptima — Soporte post-entrega')
    pdf.bullet('Starter: sin soporte post-entrega.')
    pdf.bullet('Profesional: 3 meses (bugs + cambios menores de contenido).')
    pdf.bullet('Premium: 6 meses (bugs + cambios menores de contenido).')
    pdf.body_text(
        'No incluye: funcionalidades nuevas, rediseño, cambios estructurales, marketing. '
        'Mantenimiento posterior: desde $15.000/mes.')

    # Clause 8
    pdf.section_title('Cláusula Octava — Hosting y dominio')
    pdf.body_text(
        'Hosting sin costo para sitios estáticos. Si se requiere servidor, el costo se informa '
        'antes de comenzar y es a cargo del Cliente. El dominio (primer año incluido) se registra '
        'a nombre del Cliente. Renovación anual posterior a cargo del Cliente.')

    # Clause 9
    pdf.section_title('Cláusula Novena — Prototipo gratuito')
    pdf.body_text(
        'Prototipo visual sin costo ni compromiso. Si el Cliente no continúa, no hay pago. '
        'Es un diseño navegable, no el producto terminado. Es propiedad del Desarrollador '
        'hasta la contratación formal.')

    # Clause 10
    pdf.section_title('Cláusula Décima — Rescisión')
    pdf.body_text('Rescisión con 7 días corridos de preaviso por escrito (email con acuse).')
    pdf.bullet('Por el Cliente antes del prototipo: sin costo.')
    pdf.bullet('Por el Cliente después del prototipo: mínimo 50% del precio total.')
    pdf.bullet('Por el Desarrollador: reintegro de montos por trabajo no realizado en 15 días hábiles.')
    pdf.body_text('Rescisión automática si no hay contenido en 30 días corridos.')

    # Clause 11-14
    pdf.section_title('Cláusula Undécima — Confidencialidad')
    pdf.body_text('Ambas partes mantienen confidencial toda información no pública del otro.')

    pdf.section_title('Cláusula Duodécima — Responsabilidad')
    pdf.body_text(
        'El Desarrollador garantiza funcionamiento según especificaciones. No responde por: '
        'contenido del Cliente, interrupciones de hosting, resultados comerciales, ni cambios '
        'post-entrega. Responsabilidad limitada al monto percibido.')

    pdf.section_title('Cláusula Decimotercera — Jurisdicción')
    pdf.body_text('Tribunales Ordinarios de Mendoza, Argentina.')

    pdf.section_title('Cláusula Decimocuarta — Disposiciones generales')
    pdf.body_text(
        'Acuerdo completo. Modificaciones por escrito. Nulidad parcial no afecta el resto. '
        'Se rige por leyes de la República Argentina.')

    # Signatures
    pdf.ln(10)
    pdf.body_text('En prueba de conformidad, se firman dos ejemplares de un mismo tenor.')
    pdf.ln(15)

    y_sig = pdf.get_y()
    pdf.set_font('Cal', 'B', 10)
    pdf.set_text_color(40, 40, 40)

    pdf.set_xy(25, y_sig)
    pdf.cell(70, 6, 'EL DESARROLLADOR', align='C')
    pdf.set_xy(115, y_sig)
    pdf.cell(70, 6, 'EL CLIENTE', align='C')

    pdf.set_xy(25, y_sig + 20)
    pdf.cell(70, 6, '_________________________', align='C')
    pdf.set_xy(115, y_sig + 20)
    pdf.cell(70, 6, '_________________________', align='C')

    pdf.set_font('Cal', '', 9)
    pdf.set_xy(25, y_sig + 27)
    pdf.cell(70, 5, 'Juan Ignacio Barranco', align='C')
    pdf.set_xy(115, y_sig + 27)
    pdf.cell(70, 5, 'Nombre: _______________', align='C')

    pdf.set_xy(25, y_sig + 32)
    pdf.cell(70, 5, 'DNI: _________________', align='C')
    pdf.set_xy(115, y_sig + 32)
    pdf.cell(70, 5, 'DNI/CUIT: _____________', align='C')

    # ── Anexo A ──
    pdf.add_page()
    pdf.set_font('Cal', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'ANEXO A — Alcance del proyecto', align='C')
    pdf.ln(12)

    pdf.field_line('Nombre del negocio')
    pdf.field_line('Rubro')
    pdf.ln(2)
    pdf.body_text('Plan contratado:')
    pdf.checkbox('Starter')
    pdf.checkbox('Profesional')
    pdf.checkbox('Premium')
    pdf.ln(2)
    pdf.body_text('Descripción del sitio:')
    for _ in range(3):
        pdf.set_draw_color(180, 180, 180)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(7)
    pdf.ln(2)
    pdf.bold_text('Secciones incluidas:')
    for s in [
        'Página principal', 'Sobre nosotros / Historia',
        'Servicios / Productos / Menú', 'Galería de fotos',
        'Reservas / Turnos online', 'Catálogo con Mercado Pago',
        'Formulario de contacto', 'Testimonios', 'Ubicación y horarios',
        'Versión en inglés', 'Otra: ____________________',
    ]:
        pdf.checkbox(s)

    pdf.ln(2)
    pdf.field_line('Dominio deseado')
    pdf.ln(2)
    pdf.bold_text('Contenido a cargo del Cliente:')
    for item in ['Textos y descripciones', 'Fotografías', 'Logotipo',
                 'Contacto y horarios', 'Lista de productos/precios']:
        pdf.checkbox(item)
    pdf.ln(2)
    pdf.field_line('Fecha límite contenido')
    pdf.ln(2)
    pdf.body_text('Notas adicionales:')
    for _ in range(3):
        pdf.set_draw_color(180, 180, 180)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(7)

    path = os.path.join(OUT_DIR, 'contrato-servicios.pdf')
    pdf.output(path)
    print(f'PDF saved: {path}')
    return path


if __name__ == '__main__':
    build_docx()
    build_pdf()
    print('Done!')
