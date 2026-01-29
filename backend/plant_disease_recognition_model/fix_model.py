import zipfile
import json
import os

INPUT_FILE = "plant_disease_model.keras"
OUTPUT_FILE = "plant_disease_model_fixed.keras"

print(f"Fixing {INPUT_FILE} -> {OUTPUT_FILE}...")

def fix_config(d):
    if isinstance(d, dict):
        # Fix 1: batch_shape (Keras 3 -> 2 compat or general compat)
        if 'batch_shape' in d:
            if 'batch_input_shape' not in d:
                d['batch_input_shape'] = d['batch_shape']
            del d['batch_shape']
            
        # Fix 2: DTypePolicy (Keras 3) -> string (Keras 2)
        # Config looks like: 'dtype': {'module': 'keras', 'class_name': 'DTypePolicy', 'config': {'name': 'float32'}, ...}
        # We want: 'dtype': 'float32'
        keys_to_modify = []
        for k, v in d.items():
            if k == 'dtype' and isinstance(v, dict) and v.get('class_name') == 'DTypePolicy':
                # Extract the type name
                try:
                    dtype_name = v['config']['name']
                    keys_to_modify.append((k, dtype_name))
                except KeyError:
                    pass
            else:
                fix_config(v)
        
        for k, v in keys_to_modify:
            print(f"Replacing DTypePolicy with '{v}' in key '{k}'")
            d[k] = v
            
    elif isinstance(d, list):
        for item in d:
            fix_config(item)

try:
    with zipfile.ZipFile(INPUT_FILE, "r") as zin:
        with zipfile.ZipFile(OUTPUT_FILE, "w") as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "config.json":
                    print("Processing config.json...")
                    config = json.loads(data)
                    fix_config(config)
                    data = json.dumps(config).encode('utf-8')
                zout.writestr(item, data)
    print("Success: Created fixed model file.")
except Exception as e:
    print(f"Failed: {e}")
