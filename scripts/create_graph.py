
import os
import re
import json
import sys

def parse_vault(vault_path):
    entities = set()
    relationships = []

    # Regex to find [[wiki-links]]
    link_pattern = re.compile(r"\[\[(.*?)\]\]")

    for root, _, files in os.walk(vault_path):
        # Ignore hidden folders like .git, .obsidian, etc.
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                file_name_without_ext = os.path.splitext(file)[0]

                # Add the note itself as an entity
                entities.add(file_name_without_ext)

                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                    except Exception as e:
                        print(f"Could not read {file_path}: {e}")
                        continue

                    # Find all links in the content
                    found_links = link_pattern.findall(content)
                    for link in found_links:
                        # Simple relationship: file A -> links to -> file B
                        target_entity = link.split('|')[0] # Handle aliased links [[Real Name|Alias]]
                        entities.add(target_entity)
                        relationships.append({
                            "source": file_name_without_ext,
                            "target": target_entity,
                            "type": "links_to"
                        })

    return list(entities), relationships

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = "." # Default to current directory

    print(f"Scanning vault at: {vault_path}")
    entities, relationships = parse_vault(vault_path)

    output_dir = os.path.join(vault_path, ".gemini")
    os.makedirs(output_dir, exist_ok=True)

    entities_path = os.path.join(output_dir, "entities.json")
    with open(entities_path, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2)

    relationships_path = os.path.join(output_dir, "relationships.json")
    with open(relationships_path, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2)

    print(f"Graph created successfully!")
    print(f"Found {len(entities)} entities.")
    print(f"Found {len(relationships)} relationships.")
    print(f"Output files generated in '{output_dir}' directory.")
