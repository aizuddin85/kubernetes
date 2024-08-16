import subprocess
import yaml
import sys
import re

def check_command_exists(command):
    """Check if a command exists on the system."""
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def parse_version(version):
    """Parse a version string into a tuple for comparison."""
    return tuple(int(part) if part.isdigit() else part for part in re.split(r'(\d+)', version))

def fetch_tags(registry, image, max_tags):
    """Fetch tags from a registry using Skopeo."""
    print(f"Fetching tags for {image} from {registry}...")

    try:
        # Fetch all tags using Skopeo
        result = subprocess.run(
            ['skopeo', 'list-tags', '--no-creds', f'docker://{registry}/{image}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        tags = yaml.safe_load(result.stdout)['Tags']
    except subprocess.CalledProcessError as e:
        print(f"Error fetching tags for {image} from {registry}: {e.stderr}")
        return

    if not tags:
        print(f"No tags found for {image} in {registry}.")
        return

    # Sort the tags using the custom version parsing function
    sorted_tags = sorted(tags, key=parse_version, reverse=True)

    # Limit the output to the max number of tags
    print(f"Latest {max_tags} tags for {image}:")
    for tag in sorted_tags[:max_tags]:
        print(tag)
    print()

def main():
    # Check if Skopeo is installed
    if not check_command_exists('skopeo'):
        print("Skopeo is not installed. Please install Skopeo to use this script.")
        sys.exit(1)

    # Load the configuration from the YAML file
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("config.yaml file not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

    max_tags = config.get('max', 3)

    # Loop through the registries and images in the YAML file
    for registry_config in config['registries']:
        registry = registry_config['registry']
        for image in registry_config['images']:
            fetch_tags(registry, image, max_tags)

if __name__ == "__main__":
    main()

