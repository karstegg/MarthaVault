
import os
import re
import json
import sys

def parse_vault(vault_path):
    entities = set()
    relationships = []

    # Regex to find [[wiki-links]]
    link_pattern = re.compile(r"[["(.*?)"]]")

    print("Starting scan...")
    for root, dirs, files in os.walk(vault_path):
        # Modify the dir list in-place to exclude hidden ones
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        print(f"Scanning directory: {root}")

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                file_name_without_ext = os.path.splitext(file)[0]

                # Add the note itself as an entity
                entities.add(file_name_without_ext)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"  - Could not read file: {file_path}, Error: {e}")
                    continue

                # Find all links in the content
                found_links = link_pattern.findall(content)
                for link in found_links:
                    target_entity = link.split('|')[0].strip() # Handle aliases and strip whitespace
                    entities.add(target_entity)
                    relationships.append({
                        "source": file_name_without_ext,
                        "target": target_entity,
                        "type": "links_to"
                    })
    print("Scan complete.")
    return list(entities), relationships

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide the absolute path to the vault directory.")
        sys.exit(1)
        
    vault_path = sys.argv[1]

    if not os.path.isdir(vault_path):
        print(f"Error: Provided path '{vault_path}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning vault at: {vault_path}")
    entities, relationships = parse_vault(vault_path)

    # Output dir will be in the vault's root
    output_dir = os.path.join(vault_path, ".gemini")
    os.makedirs(output_dir, exist_ok=True)

    entities_path = os.path.join(output_dir, "entities.json")
    with open(entities_path, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2)

    relationships_path = os.path.join(output_dir, "relationships.json")
    with open(relationships_path, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2)

    print("\nGraph created successfully!")
    print(f"Found {len(entities)} entities.")
    print(f"Found {len(relationships)} relationships.")
    print(f"Output files generated in '{output_dir}' directory.")
