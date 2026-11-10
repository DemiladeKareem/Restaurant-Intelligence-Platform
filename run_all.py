from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
scripts=root/'02_Data_Generation'/'scripts'
# Dependencies: sales -> production -> procurement -> inventory.
order=[
'01_generate_reference_data.py',
'02_generate_recipes.py',
'04_generate_sales.py',
'05_generate_production.py',
'03_generate_procurement.py',
'06_generate_inventory.py',
'07_generate_expenses_and_validate.py',
]
for name in order:
    print(f'\nRunning {name}...',flush=True)
    subprocess.run([sys.executable,str(scripts/name)],cwd=root,check=True)
print('\nALL GENERATORS AND VALIDATIONS PASSED.')
