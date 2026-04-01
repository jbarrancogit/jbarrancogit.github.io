"""
quick_deploy.py — Deploy rápido de cambios.

Uso:
  python scripts/quick_deploy.py "mensaje del commit"
  python scripts/quick_deploy.py                          # auto-genera mensaje

Hace git add + commit + push en un solo comando.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd, **kwargs):
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, **kwargs)


def main():
    # Ver qué cambió
    status = run(['git', 'status', '--porcelain'])
    if not status.stdout.strip():
        print('  ✅ No hay cambios para pushear.')
        return

    print('  📋 Cambios detectados:')
    for line in status.stdout.strip().split('\n'):
        print(f'     {line}')

    # Mensaje de commit
    if len(sys.argv) > 1:
        msg = ' '.join(sys.argv[1:])
    else:
        msg = f'Actualización — {datetime.now().strftime("%d/%m %H:%M")}'

    # Stage, commit, push
    print(f'\n  📤 Commit: {msg}')
    run(['git', 'add', '-A'])
    result = run(['git', 'commit', '-m', msg])
    if result.returncode != 0:
        print(f'  ⚠ Error en commit: {result.stderr}')
        return

    result = run(['git', 'push'])
    if result.returncode != 0:
        print(f'  ⚠ Error en push: {result.stderr}')
        return

    print('  ✅ Pusheado exitosamente.')

    # Mostrar URL
    print('  🔗 https://jbarrancogit.github.io/')


if __name__ == '__main__':
    main()
