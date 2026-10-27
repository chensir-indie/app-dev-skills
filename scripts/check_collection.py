#!/usr/bin/env python3
"""Check skill discovery, portable local links and invocation metadata.

This is a packaging check, not a secrets scanner or visual-quality review.
"""
import html
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    import shlex
    root = Path(__file__).resolve().parents[1]
    sys.exit('Missing PyYAML. Activate your virtual environment and run: python -m pip install -r {}\nThen rerun: sh {} --scope collection.'.format(shlex.quote(str(root / 'skills/image-to-layered-html-prototype/requirements.txt')), shlex.quote(str(root / 'scripts/doctor.sh'))))

IGNORED = {'node_modules', '.git', '.venv', '__pycache__', 'exports', '.test-output'}
ROOT_READMES = ('README.md', 'README.zh-CN.md')
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently replacing discovery metadata."""

    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in mapping:
                raise yaml.constructor.ConstructorError(
                    None, None, f'duplicate or non-string YAML key: {key!r}', key_node.start_mark)
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def load_yaml(source):
    return yaml.load(source, Loader=UniqueKeyLoader)


def documents(root):
    for path in sorted(root.rglob('*.md')):
        if not IGNORED.intersection(path.relative_to(root).parts):
            yield path


def without_fences(source):
    """Keep rendered Markdown, excluding fenced examples and HTML comments."""
    source = re.sub(r'\A---[ \t]*\r?\n.*?\r?\n---(?:[ \t]*\r?\n|[ \t]*$)', '', source, count=1, flags=re.S)
    lines = []
    fence = None
    for line in source.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.match(r'^ {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', line):
                fence = None
            lines.append('')
        elif marker:
            fence = marker.group(1)
            lines.append('')
        else:
            lines.append(line)
    return re.sub(r'<!--.*?-->', '', '\n'.join(lines), flags=re.S)


def closing_delimiter(source, start, opening, closing):
    depth = 1
    cursor = start + 1
    while cursor < len(source):
        char = source[cursor]
        if char == '\\':
            cursor += 2
            continue
        if opening == '(' and char == '<':
            angle_end = source.find('>', cursor + 1)
            if angle_end != -1:
                cursor = angle_end + 1
                continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return cursor
        cursor += 1
    return None


def destination(source):
    """Read a Markdown destination, leaving an optional quoted title behind."""
    source = source.strip()
    if source.startswith('<'):
        end = source.find('>', 1)
        return source[1:end] if end != -1 else None
    cursor = 0
    depth = 0
    while cursor < len(source):
        char = source[cursor]
        if char == '\\':
            cursor += 2
            continue
        if char.isspace() and depth == 0:
            break
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        cursor += 1
    return source[:cursor]


def markdown_links(source):
    """Extract inline/image and defined reference links from rendered prose.

    This handles the link forms used by this collection, rather than trying to
    lint all Markdown syntax. Code examples are deliberately outside its scope.
    """
    source = without_fences(source)
    source = re.sub(r'(`+).*?\1', '', source, flags=re.S)
    definitions = {}

    def definition(match):
        label = ' '.join(match.group(1).split()).casefold()
        definitions.setdefault(label, destination(match.group(2)))
        return ''

    source = re.sub(r'^ {0,3}\[([^\]\n]+)\]:[ \t]*([^\n]*)$', definition, source, flags=re.M)
    reference_labels = set()
    for match in re.finditer(r'(?<!\\)\[', source):
        start = match.start()
        if start in reference_labels:
            continue
        end = closing_delimiter(source, start, '[', ']')
        if end is None:
            continue
        after = end + 1
        if source[after:after + 1] == '(':
            tail = closing_delimiter(source, after, '(', ')')
            if tail is not None:
                link = destination(source[after + 1:tail])
                if link:
                    yield link
            continue
        label = source[start + 1:end]
        if source[after:after + 1] == '[':
            tail = closing_delimiter(source, after, '[', ']')
            if tail is None:
                continue
            reference_labels.add(after)
            label = source[after + 1:tail] or label
        link = definitions.get(' '.join(label.split()).casefold())
        if link:
            yield link


def anchors(source, markdown=True):
    source = without_fences(source) if markdown else source
    explicit = set(re.findall(r'\b(?:id|name)\s*=\s*[\"\']([^\"\']+)[\"\']', source, re.I))
    if not markdown:
        return explicit
    headings = []
    lines = source.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r'^ {0,3}#{1,6}[ \t]+(.+?)\s*$', line)
        if heading:
            headings.append(re.sub(r'[ \t]+#+[ \t]*$', '', heading.group(1)))
        elif index and re.fullmatch(r' {0,3}(?:=+|-+)[ \t]*', line) and lines[index - 1].strip():
            headings.append(lines[index - 1].strip())
    generated = set()
    for heading in headings:
        heading = re.sub(r'<[^>]*>', '', heading)
        heading = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', heading)
        heading = html.unescape(heading).lower()
        slug = ''.join(char for char in heading
                       if char in '-_' or unicodedata.category(char)[0] not in 'PS')
        slug = re.sub(r'\s', '-', slug)
        unique = slug
        suffix = 0
        while unique in generated:
            suffix += 1
            unique = f'{slug}-{suffix}'
        generated.add(unique)
    return generated | explicit


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def valid_slug(value):
    return isinstance(value, str) and len(value) <= 64 and SLUG.fullmatch(value)


def local_link(doc, link):
    link = html.unescape(re.sub(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', r'\1', link))
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        return None
    target = (doc.parent / unquote(parsed.path)).resolve() if parsed.path else doc.resolve()
    return target, unquote(parsed.fragment)


def check(root):
    root = Path(root).resolve()
    errors = []
    skill_root = root / 'skills'
    skill_dirs = sorted(path for path in skill_root.iterdir()
                        if path.is_dir() and path.name not in IGNORED and not path.name.startswith('.')) if skill_root.is_dir() else []
    entries = []
    for skill in skill_dirs:
        if not valid_slug(skill.name):
            errors.append(f'{skill.name}: invalid skill directory slug')
        if (skill / 'SKILL.md').is_file():
            entries.append(skill / 'SKILL.md')
        else:
            errors.append(f'{skill.name}: missing discovery entry SKILL.md (flat skills/ layout required)')
    if not entries:
        errors.append('No skills discovered')
    names = {}
    for entry in entries:
        skill = entry.parent
        try:
            match = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---(?:[ \t]*\r?\n|[ \t]*$)', entry.read_text(encoding='utf-8'), re.S)
            header = load_yaml(match.group(1)) if match else {}
            if not isinstance(header, dict) or header.get('name') != skill.name:
                errors.append(f'{skill.name}: frontmatter name mismatch')
            if isinstance(header, dict):
                name = header.get('name')
                if not valid_slug(name):
                    errors.append(f'{skill.name}: invalid frontmatter name slug')
                elif name in names:
                    errors.append(f'{skill.name}: duplicate skill name {name!r} (also {names[name]})')
                else:
                    names[name] = skill.name
                description = header.get('description')
                if not nonempty_string(description) or len(description) > 1024:
                    errors.append(f'{skill.name}: missing or invalid description (nonempty string, at most 1024 characters)')
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f'{skill.name}: invalid frontmatter: {exc}')
        try:
            config = load_yaml((skill / 'agents/openai.yaml').read_text(encoding='utf-8'))
            metadata = config.get('interface') if isinstance(config, dict) else None
            valid = isinstance(metadata, dict)
            if valid:
                display = metadata.get('display_name')
                short = metadata.get('short_description')
                prompt = metadata.get('default_prompt')
                token = r'(?<![\w$-])\$' + re.escape(skill.name) + r'(?![\w-])'
                valid = (nonempty_string(display) and nonempty_string(short) and 25 <= len(short) <= 64
                         and isinstance(prompt, str) and re.search(token, prompt) is not None)
            if not valid:
                errors.append(f'{skill.name}: invalid invocation metadata (nonempty string fields, short_description 25-64 characters and exact ${skill.name} token required)')
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f'{skill.name}: invalid invocation metadata: {exc}')
        for name in ('LICENSE',):
            if not (skill / name).is_file():
                errors.append(f'{skill.name}: missing standalone {name}')
        if not (skill / 'scripts/doctor.sh').is_file():
            errors.append(f'{skill.name}: missing standalone runtime preflight scripts/doctor.sh')
    targets_by_doc = {}
    anchor_cache = {}
    for doc in documents(root):
        try:
            text = doc.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{doc.relative_to(root)}: unreadable documentation: {exc}')
            continue
        if re.search(r'/(?:Users|home)/[\w.-]+/', text):
            errors.append(f'{doc.relative_to(root)}: private absolute path')
        owner = next((entry.parent for entry in entries if entry.parent in doc.parents), None)
        targets_by_doc[doc] = set()
        for link in markdown_links(text):
            try:
                local = local_link(doc, link)
            except ValueError as exc:
                errors.append(f'{doc.relative_to(root)}: invalid link {link}: {exc}')
                continue
            if local is None:
                continue
            target, fragment = local
            targets_by_doc[doc].add(target)
            if not target.exists():
                errors.append(f'{doc.relative_to(root)}: broken link {link}')
            elif fragment and target.suffix.lower() in {'.md', '.markdown', '.html', '.htm', '.svg'}:
                if target not in anchor_cache:
                    try:
                        anchor_cache[target] = anchors(target.read_text(encoding='utf-8'), target.suffix.lower() in {'.md', '.markdown'})
                    except (OSError, UnicodeError) as exc:
                        errors.append(f'{doc.relative_to(root)}: unreadable fragment target {link}: {exc}')
                        anchor_cache[target] = set()
                if fragment not in anchor_cache[target]:
                    errors.append(f'{doc.relative_to(root)}: broken fragment {link}')
            if owner and target != owner and owner not in target.parents:
                errors.append(f'{doc.relative_to(root)}: link outside skill {link}')
            elif target != root and root not in target.parents:
                errors.append(f'{doc.relative_to(root)}: link outside collection {link}')
    for name in ROOT_READMES:
        doc = root / name
        if not doc.is_file():
            errors.append(f'{name}: missing collection README')
            continue
        for entry in entries:
            if entry.resolve() not in targets_by_doc.get(doc, set()):
                errors.append(f'{name}: missing direct skill entry link {entry.relative_to(root)}')
    return errors


if __name__ == '__main__':
    findings = check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
    if findings:
        print('\n'.join(findings), file=sys.stderr)
        sys.exit(1)
    print('Skill discovery, metadata, standalone links and documentation paths: PASS')
