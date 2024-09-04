import toml
from packaging.version import Version, InvalidVersion

def load_pyproject_toml(path):
    """Load a pyproject.toml file."""
    return toml.load(path)

def save_pyproject_toml(path, data):
    """Save a pyproject.toml file."""
    with open(path, 'w') as f:
        toml.dump(data, f)

def get_min_version(version1, version2):
    """Returns the minimum version between two version strings in caret format."""
    try:
        v1 = Version(version1)
        v2 = Version(version2)
        min_version = min(v1, v2)  # Select the least version
        return f"^{min_version.major}.{min_version.minor}.0"  # Format with caret for the major.minor range
    except InvalidVersion:
        # If versions can't be parsed correctly, return one as is (simple fallback)
        return version1

def merge_dependencies(main_toml, sub_tomls):
    """Merge dependencies from sub-tomls into the main_toml."""
    main_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
    main_dev_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

    for sub_toml_path in sub_tomls:
        sub_toml = load_pyproject_toml(sub_toml_path)
        sub_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
        sub_dev_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

        # Merge dependencies with the least version and caret format
        for dep, version in sub_dependencies.items():
            if dep in main_dependencies:
                main_dependencies[dep] = get_min_version(main_dependencies[dep], version)
            else:
                main_dependencies[dep] = f"^{version}" if not version.startswith('^') else version

        # Merge dev dependencies in the same way
        for dep, version in sub_dev_dependencies.items():
            if dep in main_dev_dependencies:
                main_dev_dependencies[dep] = get_min_version(main_dev_dependencies[dep], version)
            else:
                main_dev_dependencies[dep] = f"^{version}" if not version.startswith('^') else version

    main_toml['tool']['poetry']['dependencies'] = main_dependencies
    main_toml['tool']['poetry']['dev-dependencies'] = main_dev_dependencies

def main():
    main_toml_path = 'pyproject.toml'
    sub_tomls = [
        'src/yosafe_packages/yosafe_subpackage_1/pyproject.toml',
        'src/yosafe_packages/yosafe_subpackage_2/pyproject.toml',
        'src/yosafe_packages/yosafe_subpackage_3/pyproject.toml'
    ]

    main_toml = load_pyproject_toml(main_toml_path)
    merge_dependencies(main_toml, sub_tomls)
    save_pyproject_toml(main_toml_path, main_toml)


if __name__ == '__main__':
    main()
