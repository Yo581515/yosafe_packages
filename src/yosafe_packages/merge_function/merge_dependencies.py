import toml
from packaging.version import Version, InvalidVersion

def load_pyproject_toml(path):
    """Load a pyproject.toml file."""
    return toml.load(path)

def save_pyproject_toml(path, data):
    """Save a pyproject.toml file."""
    with open(path, 'w') as f:
        toml.dump(data, f)

def update_version_range(existing_range, new_version):
    """Update the version range with the new version."""
    try:
        # Parse existing version range if present, or set initial range to new version
        if existing_range:
            min_version, max_version = existing_range
        else:
            min_version, max_version = new_version, new_version

        # Update min and max versions
        min_version = min(min_version, new_version)
        max_version = max(max_version, new_version)
        return min_version, max_version
    except InvalidVersion:
        # If parsing fails, fallback to just the current versions (could handle this better)
        return new_version, new_version

def merge_dependencies(main_toml, sub_tomls):
    """Merge dependencies from sub-tomls into the main_toml."""
    main_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
    main_dev_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

    # Using dicts to store the min and max versions of dependencies
    dependency_versions = {}
    dev_dependency_versions = {}

    for sub_toml_path in sub_tomls:
        sub_toml = load_pyproject_toml(sub_toml_path)
        sub_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
        sub_dev_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

        # Merge dependencies and determine min/max version ranges
        for dep, version in sub_dependencies.items():
            try:
                parsed_version = Version(version.lstrip('^'))
                if dep in dependency_versions:
                    dependency_versions[dep] = update_version_range(dependency_versions[dep], parsed_version)
                else:
                    dependency_versions[dep] = (parsed_version, parsed_version)
            except InvalidVersion:
                # Handle any dependencies that cannot be parsed as valid versions
                pass

        # Merge dev dependencies in the same way
        for dep, version in sub_dev_dependencies.items():
            try:
                parsed_version = Version(version.lstrip('^'))
                if dep in dev_dependency_versions:
                    dev_dependency_versions[dep] = update_version_range(dev_dependency_versions[dep], parsed_version)
                else:
                    dev_dependency_versions[dep] = (parsed_version, parsed_version)
            except InvalidVersion:
                # Handle any dependencies that cannot be parsed as valid versions
                pass

    # Convert the min/max version ranges into the required format and add to main dependencies
    for dep, (min_version, max_version) in dependency_versions.items():
        main_dependencies[dep] = f">={min_version},<{max_version.next_major()}"

    for dep, (min_version, max_version) in dev_dependency_versions.items():
        main_dev_dependencies[dep] = f">={min_version},<{max_version.next_major()}"

    # Update the main TOML with merged dependencies
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
