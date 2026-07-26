#!/usr/bin/env python3
"""Render meta/main.yml from templates/meta_main.yml.j2."""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]
UBUNTU_CODENAME_MAP = {'20.04': 'focal', '22.04': 'jammy', '24.04': 'noble', '26.04': 'resolute'}
DEBIAN_CODENAME_MAP = {'11': 'bullseye', '12': 'bookworm', '13': 'trixie', '14': 'forky'}
PLATFORM_NAME_MAP = {'fedora': 'Fedora', 'ubuntu': 'Ubuntu', 'debian': 'Debian'}
PLATFORM_ORDER = ('fedora', 'ubuntu', 'debian')
RENDER_FEDORA_AS_ALL = True


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'Expected top-level mapping in {path}')
    return data


def normalize_versions(platform_key: str, versions: list[Any]) -> list[str]:
    if platform_key == 'ubuntu':
        return [UBUNTU_CODENAME_MAP.get(str(item), str(item)) for item in versions]
    if platform_key == 'debian':
        return [DEBIAN_CODENAME_MAP.get(str(item), str(item)) for item in versions]
    if platform_key == 'fedora' and RENDER_FEDORA_AS_ALL:
        return ['all']
    return [str(item) for item in versions]


def matrix_to_platforms(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    platforms = []
    for key in PLATFORM_ORDER:
        if key in matrix:
            platforms.append({'name': PLATFORM_NAME_MAP[key], 'versions': normalize_versions(key, matrix[key])})
    return platforms


def render(template_path: Path, output_path: Path, vars_path: Path) -> None:
    vars_data = load_yaml(vars_path)
    matrix = vars_data.get('platform_matrix', vars_data)
    env = Environment(loader=FileSystemLoader(str(template_path.parent)), undefined=StrictUndefined, trim_blocks=True)
    template = env.get_template(template_path.name)
    output_path.write_text(template.render(platforms=matrix_to_platforms(matrix), template_name=template_path.name), encoding='utf-8')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Render meta/main.yml from molecule/shared/vars.yml')
    parser.add_argument('--vars-file', default='molecule/shared/vars.yml')
    parser.add_argument('--template', default='templates/meta_main.yml.j2')
    parser.add_argument('--output', default='meta/main.yml')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    render(ROOT / args.template, ROOT / args.output, ROOT / args.vars_file)


if __name__ == '__main__':
    main()
