---
name: prospect
description: Busca negocios sin página web en Mendoza usando el scraper de OpenStreetMap. Acepta rubro y radio como argumentos. Usá cuando quieras encontrar nuevos prospectos para contactar.
user-invocable: true
argument-hint: "[rubro] [radio_metros]"
---

Descubrir negocios locales sin presencia web para contactar como prospectos.

## Contexto

- **Script:** `KIT_OPERATIVO/scraper_prospectos.py` — consulta Overpass API (OpenStreetMap)
- **Directorio de output:** `KIT_OPERATIVO/prospectos_*.csv`
- **Rubros válidos (amenity de OSM):** restaurant, cafe, bar, fast_food, clinic, dentist, doctors, pharmacy, veterinary, hairdresser, beauty, hotel, hostel, guest_house
- **Coordenadas default:** Mendoza Centro (-32.889458, -68.845839)
- **Radio default:** 2000 metros

## Paso 1: Interpretar argumentos

El usuario puede decir cosas como:
- `/prospect restaurant` → rubro=restaurant, radio=2000 (default)
- `/prospect cafe 5000` → rubro=cafe, radio=5000
- `/prospect dentist,clinic` → múltiples rubros
- `/prospect` (sin args) → preguntar qué rubro buscar

Si el usuario pide múltiples rubros separados por coma, ejecutar el scraper una vez por cada rubro.

## Paso 2: Ejecutar el scraper

Ejecutá el script con los argumentos correspondientes:

```bash
python KIT_OPERATIVO/scraper_prospectos.py --rubro {rubro} --radio {radio}
```

Si el script no acepta argumentos CLI (versión vieja sin argparse), modificá temporalmente las constantes `RUBRO` y `RADIO` en el script antes de ejecutar, y restaurá los valores originales después.

**IMPORTANTE:** Ejecutá el script desde la raíz del proyecto `oportunidades_mendoza/`, no desde `landing-page/`.

## Paso 3: Leer y presentar resultados

1. Buscá el CSV más reciente generado en `KIT_OPERATIVO/` que coincida con `prospectos_{rubro}_mendoza_*.csv`
2. Leé el CSV y presentá los resultados como tabla:

| # | Nombre | Teléfono | Web actual | Ubicación |
|---|--------|----------|------------|-----------|

3. Resaltá:
   - Cuántos prospectos se encontraron
   - Cuántos tienen teléfono disponible (contactables)
   - Cuántos son nuevos (no aparecen en CSVs anteriores)

## Paso 4: Siguiente paso

Sugerí al usuario:
- **Para contactar un prospecto:** `/outreach [nombre del negocio]`
- **Para buscar otro rubro:** `/prospect [otro_rubro]`
- **Para ampliar el radio:** `/prospect {rubro} 5000`

Todo el output en **español argentino**.
