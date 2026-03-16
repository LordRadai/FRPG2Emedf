import json
import re
import sys
import os

def clean_name(name):
    """Removes spaces and non-alphanumeric characters for keys."""
    if not name: return ""
    return re.sub(r'[^a-zA-Z0-9]', '', name)

def generate_aliased_json(old_path, new_path, output_path):
    with open(old_path, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    with open(new_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    # --- INITIALIZE DARKSCRIPT BLOCK ---
    if "darkscript" not in new_data:
        new_data["darkscript"] = {"aliases": {}, "enum_aliases": {}}
    
    if "aliases" not in new_data["darkscript"]:
        new_data["darkscript"]["aliases"] = {}
    if "enum_aliases" not in new_data["darkscript"]:
        new_data["darkscript"]["enum_aliases"] = {}

    target_aliases = new_data["darkscript"]["aliases"]
    target_enum_aliases = new_data["darkscript"]["enum_aliases"]

    # --- 1. PRE-MAP NEW DATA ---
    new_enum_names = {clean_name(enm["name"]) for enm in new_data.get("enums", [])}
    
    # Map Old Instructions: {group_idx: {event_idx: name}}
    old_instr_map = {
        cls["index"]: {i["index"]: i["name"] for i in cls.get("instrs", [])}
        for cls in old_data.get("main_classes", [])
    }

    # --- 2. PROCESS COMMAND ALIASES ---
    for cls in new_data.get("main_classes", []):
        group_id = cls["index"]
        for instr in cls.get("instrs", []):
            event_id = instr["index"]
            new_name = instr["name"]
            
            # Check if this command existed in the old file
            old_name = old_instr_map.get(group_id, {}).get(event_id)
            
            # If the name changed, create alias: "OldName": "groupID[eventID]"
            if old_name and old_name != new_name:
                key = clean_name(old_name)
                # Ensure we don't overwrite existing user-defined aliases
                if key not in target_aliases:
                    # Format changed to groupID[eventID]
                    # eventID is padded to 2 digits to match standard darkscript formatting
                    target_aliases[key] = f"{group_id}[{event_id:02}]"

    # --- 3. PROCESS MISSING ENUMS ---
    for old_enm in old_data.get("enums", []):
        old_clean_category = clean_name(old_enm["name"])

        if old_clean_category not in new_enum_names:
            old_values = old_enm.get("values", {})
            for val_id, val_name in old_values.items():
                alias_key = f"{old_clean_category}.{clean_name(val_name)}"
                if alias_key not in target_enum_aliases:
                    target_enum_aliases[alias_key] = int(val_id)

    # --- 4. SAVE OUTPUT ---
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"Generated {len(target_aliases)} command aliases.")
    print(f"Generated {len(target_enum_aliases)} enum aliases.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <old_json> <new_json> [output_json]")
        sys.exit(1)

    out_file = sys.argv[3] if len(sys.argv) > 3 else "output_aliased.json"
    generate_aliased_json(sys.argv[1], sys.argv[2], out_file)