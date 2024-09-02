import toml
import os

def load_pyproject_toml(path):
    """Load a pyproject.toml file."""
    return toml.load(path)

def save_pyproject_toml(path, data):
    """Save a pyproject.toml file."""
    with open(path, 'w') as f:
        toml.dump(data, f)

def merge_dependencies(main_toml, sub_tomls):
    """Merge dependencies from sub-tomls into the main_toml."""
    main_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
    main_dev_dependencies = main_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

    for sub_toml_path in sub_tomls:
        sub_toml = load_pyproject_toml(sub_toml_path)
        sub_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
        sub_dev_dependencies = sub_toml.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})

        # Merge dependencies
        main_dependencies.update(sub_dependencies)
        main_dev_dependencies.update(sub_dev_dependencies)

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