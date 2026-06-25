"""
[하네스 엔지니어링] MD 온톨로지 구조 검증기 (Obsidian WikiLink 양식)
=====================================================================
MD 파일 기반 지식 그래프의 무결성을 검증한다.

검증 대상:
  1. YAML 프론트매터 존재 여부 및 필수 필드 확인
  2. 'type' 필드 값 (hub | spoke)
  3. 'links' 필드가 리스트 형식인지 확인
  4. Obsidian WikiLink [[Target]] 파싱 → 깨진 링크 탐지
  5. 스포크→스포크 직접 WikiLink 금지 (토폴로지 위반)

MD 파일 규칙 (Obsidian 양식):
  ---
  type: hub          # 또는 spoke
  title: 문서 제목
  links: []          # 명시적 연결 목록
  ---

  본문에서 [[다른파일명]] 또는 [[폴더/파일명]] 형식으로 링크.
  [[파일명|표시명]], [[파일명#헤더]] 형식도 지원 (타겟 파일명만 추출).

사용법:
  python scripts/validate_md_ontology.py                  # paik/ 루트에서 전체 검색
  python scripts/validate_md_ontology.py --path apps/     # 특정 경로만
  python scripts/validate_md_ontology.py --no-broken-link # 깨진 링크 검사 제외
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML이 필요합니다: pip install PyYAML")
    sys.exit(1)

# ── 정규식 ────────────────────────────────────────────────────────────────────
# YAML 프론트매터: 파일 맨 앞 --- ... --- 블록
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\s*\n", re.DOTALL)

# Obsidian WikiLink: [[Target]], [[Target|Alias]], [[Target#Heading]]
# 타겟 부분(|나 # 이전)만 캡처
WIKILINK_RE = re.compile(r"\[\[([^\[\]|#\n]+?)(?:[|#][^\[\]\n]*)?\]\]")

REQUIRED_FIELDS: Set[str] = {"type", "links"}
VALID_TYPES: Set[str] = {"hub", "spoke"}

# 검색에서 제외할 경로 패턴
EXCLUDE_PATTERNS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


# ── 데이터 모델 ───────────────────────────────────────────────────────────────

@dataclass
class MdNode:
    path: Path
    node_type: str = "unknown"           # "hub" | "spoke" | "unknown"
    declared_links: List[str] = field(default_factory=list)
    wikilinks: List[str] = field(default_factory=list)   # 본문의 [[Target]] 목록
    parse_errors: List[str] = field(default_factory=list)


@dataclass
class OntologyViolation:
    file: str
    kind: str
    message: str

    def __str__(self) -> str:
        return f"  [{self.kind}] {self.file}\n    {self.message}"


# ── 파싱 ─────────────────────────────────────────────────────────────────────

def _parse_md_node(file_path: Path) -> MdNode:
    node = MdNode(path=file_path)

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        node.parse_errors.append("파일 인코딩 오류 (UTF-8 아님)")
        return node

    # 1. 프론트매터 추출
    match = FRONTMATTER_RE.match(content)
    if not match:
        node.parse_errors.append("YAML 프론트매터 없음 (파일 맨 앞 --- 블록 필요)")
        # 프론트매터 없어도 WikiLink는 추출
        node.wikilinks = WIKILINK_RE.findall(content)
        return node

    # 2. YAML 파싱
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        node.parse_errors.append(f"YAML 파싱 오류: {e}")
        return node

    if not isinstance(frontmatter, dict):
        node.parse_errors.append("프론트매터가 키-값 매핑 형식이 아님")
        return node

    # 3. 필수 필드 검증
    for required in REQUIRED_FIELDS:
        if required not in frontmatter:
            node.parse_errors.append(f"필수 필드 누락: '{required}'")

    # 4. type 필드 검증
    node_type = frontmatter.get("type", "")
    if node_type not in VALID_TYPES:
        node.parse_errors.append(
            f"'type' 값 오류: '{node_type}' — 허용값: {sorted(VALID_TYPES)}"
        )
    else:
        node.node_type = node_type

    # 5. links 필드 검증
    links = frontmatter.get("links", [])
    if not isinstance(links, list):
        node.parse_errors.append(f"'links' 필드는 리스트여야 함 (현재: {type(links).__name__})")
    else:
        node.declared_links = [str(lnk) for lnk in links if lnk]

    # 6. 본문 WikiLink 추출 (프론트매터 이후 텍스트)
    body = content[match.end():]
    node.wikilinks = WIKILINK_RE.findall(body)

    return node


def _build_node_map(search_path: Path) -> Dict[str, MdNode]:
    """
    검색 경로의 모든 .md 파일을 파싱하여 {파일명 stem → MdNode} 매핑 반환.
    동일 stem이 여러 경로에 존재하면 마지막 것이 덮어씀 (경고 출력).
    """
    node_map: Dict[str, MdNode] = {}
    duplicates: Dict[str, List[Path]] = {}

    for md_file in sorted(search_path.rglob("*.md")):
        # 제외 경로 필터
        if any(p in EXCLUDE_PATTERNS for p in md_file.parts):
            continue

        stem = md_file.stem
        if stem in node_map:
            duplicates.setdefault(stem, [node_map[stem].path]).append(md_file)
        node_map[stem] = _parse_md_node(md_file)

    if duplicates:
        print("[경고] 동일 파일명(stem) 중복 — WikiLink 해석이 모호할 수 있음:")
        for stem, paths in duplicates.items():
            for p in paths:
                print(f"  [[{stem}]] → {p}")
        print()

    return node_map


# ── 검증 ─────────────────────────────────────────────────────────────────────

def validate_ontology(
    node_map: Dict[str, MdNode],
    check_broken_links: bool = True,
) -> List[OntologyViolation]:
    violations: List[OntologyViolation] = []

    spoke_stems: Set[str] = {s for s, n in node_map.items() if n.node_type == "spoke"}

    for stem, node in node_map.items():
        rel = str(node.path)

        # 프론트매터 구조 오류
        for err in node.parse_errors:
            violations.append(OntologyViolation(
                file=rel, kind="FRONTMATTER_ERROR", message=err
            ))

        # 이하 링크 검증은 type을 알 수 있는 노드만
        if node.node_type == "unknown":
            continue

        for raw_link in node.wikilinks:
            # 링크 타겟의 파일명 stem 추출 ("폴더/파일명" → "파일명")
            target_stem = Path(raw_link.strip()).stem

            # 깨진 WikiLink 검사
            if check_broken_links and target_stem not in node_map:
                violations.append(OntologyViolation(
                    file=rel,
                    kind="BROKEN_LINK",
                    message=f"참조 대상 없음: [[{raw_link}]] ('{target_stem}.md' 파일을 찾을 수 없음)",
                ))
                continue

            # 스포크 → 스포크 직접 WikiLink 금지
            if node.node_type == "spoke" and target_stem in spoke_stems and target_stem != stem:
                violations.append(OntologyViolation(
                    file=rel,
                    kind="SPOKE_TO_SPOKE_LINK",
                    message=(
                        f"스포크 간 직접 링크 금지: [[{raw_link}]]\n"
                        f"    → 허브(star_craft 관련 노드)를 경유하는 링크로 변경할 것"
                    ),
                ))

    return violations


# ── 진입점 ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="MD 온톨로지 토폴로지 검증기 (Obsidian WikiLink)")
    parser.add_argument(
        "--path", type=Path,
        default=Path(__file__).parent.parent,
        help="검색 루트 경로 (기본: paik/ 루트)",
    )
    parser.add_argument(
        "--no-broken-link", action="store_true",
        help="깨진 WikiLink 검사 생략",
    )
    args = parser.parse_args()

    search_path = args.path.resolve()

    print("=" * 60)
    print("[MD Ontology Validator] WikiLink 토폴로지 검증")
    print(f"  검색 경로: {search_path}")
    print("=" * 60)

    node_map = _build_node_map(search_path)

    hub_count   = sum(1 for n in node_map.values() if n.node_type == "hub")
    spoke_count = sum(1 for n in node_map.values() if n.node_type == "spoke")
    unknown_count = len(node_map) - hub_count - spoke_count

    print(f"\n  발견된 MD 파일: {len(node_map)}개")
    print(f"    hub    : {hub_count}개")
    print(f"    spoke  : {spoke_count}개")
    print(f"    unknown: {unknown_count}개 (프론트매터 없거나 type 오류)\n")

    violations = validate_ontology(
        node_map,
        check_broken_links=not args.no_broken_link,
    )

    if not violations:
        print("✅ 온톨로지 위반 없음. 모든 MD 파일 구조 준수.\n")
        sys.exit(0)

    # 종류별 분류
    by_kind: Dict[str, List[OntologyViolation]] = {}
    for v in violations:
        by_kind.setdefault(v.kind, []).append(v)

    print(f"❌ 온톨로지 위반 {len(violations)}건 발견\n")

    order = ["FRONTMATTER_ERROR", "SPOKE_TO_SPOKE_LINK", "BROKEN_LINK"]
    for kind in order + [k for k in by_kind if k not in order]:
        items = by_kind.get(kind, [])
        if not items:
            continue
        labels = {
            "FRONTMATTER_ERROR":   "프론트매터 구조 오류",
            "SPOKE_TO_SPOKE_LINK": "스포크→스포크 직접 링크 (토폴로지 위반)",
            "BROKEN_LINK":         "깨진 WikiLink",
        }
        print(f"  [{kind}] {labels.get(kind, kind)} — {len(items)}건")
        for v in items:
            print(v)
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
