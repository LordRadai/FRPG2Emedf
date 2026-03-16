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
    # If the new file already has aliases, we start with those
    if "darkscript" not in new_data:
        new_data["darkscript"] = {"aliases": {}, "enum_aliases": {}}
    
    # Ensure sub-keys exist
    if "aliases" not in new_data["darkscript"]:
        new_data["darkscript"]["aliases"] = {}
    if "enum_aliases" not in new_data["darkscript"]:
        new_data["darkscript"]["enum_aliases"] = {}

    target_aliases = new_data["darkscript"]["aliases"]
    target_enum_aliases = new_data["darkscript"]["enum_aliases"]

    # --- 1. PRE-MAP NEW DATA ---
    # Set of clean names present in the NEW file to identify what is "Missing"
    new_enum_names = {clean_name(enm["name"]) for enm in new_data.get("enums", [])}
    
    # Map Old Instructions for the command aliases comparison
    old_instr_map = {
        cls["index"]: {i["index"]: i["name"] for i in cls.get("instrs", [])}
        for cls in old_data.get("main_classes", [])
    }

    # --- 2. PROCESS COMMAND ALIASES ---
    for cls in new_data.get("main_classes", []):
        c_idx = cls["index"]
        for instr in cls.get("instrs", []):
            i_idx, new_name = instr["index"], instr["name"]
            old_name = old_instr_map.get(c_idx, {}).get(i_idx)
            
            # If name changed, and the old name isn't already an alias
            if old_name and old_name != new_name:
                key = clean_name(old_name)
                if key not in target_aliases:
                    target_aliases[key] = f"{c_idx}{i_idx:02}[{i_idx:02}]"

    # --- 3. PROCESS MISSING ENUMS ---
    for old_enm in old_data.get("enums", []):
        old_clean_category = clean_name(old_enm["name"])

        # If this enum category is completely missing in the new file
        if old_clean_category not in new_enum_names:
            old_values = old_enm.get("values", {})
            
            for val_id, val_name in old_values.items():
                alias_key = f"{old_clean_category}.{clean_name(val_name)}"
                # Only add if it doesn't already exist in the new file's aliases
                if alias_key not in target_enum_aliases:
                    target_enum_aliases[alias_key] = int(val_id)

    # --- 4. SAVE OUTPUT ---
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"Process Complete.")
    print(f"Total Command Aliases: {len(target_aliases)}")
    print(f"Total Enum Aliases: {len(target_enum_aliases)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <old_json> <new_json> [output_json]")
        sys.exit(1)

    out_file = sys.argv[3] if len(sys.argv) > 3 else "output_with_merged_aliases.json"
    generate_aliased_json(sys.argv[1], sys.argv[2], out_file)