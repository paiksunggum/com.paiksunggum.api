"""
[하네스 엔지니어링] Python Import 스타 토폴로지 검증기
========================================================
안드레이 카파시의 하네스 엔지니어링 철학 적용:
  - 구조적 제약 조건을 코드로 강제한다.
  - 규칙 위반이 빌드/CI 단계에서 즉시 감지되어야 한다.
  - "테스트가 없으면 기능이 없는 것이다" → "검증이 없으면 아키텍처가 없는 것이다"

스타 토폴로지 규칙:
  ✅ spoke → hub       허용 (스포크가 허브를 참조)
  ✅ spoke → core      허용 (공통 인프라 참조)
  ✅ hub   → core      허용
  ❌ spoke → spoke     금지 (직접 크로스-도메인 import)
  ❌ hub   → spoke     금지 (허브의 도메인 결합 방지)

사용법:
  python scripts/validate_topology.py
  python scripts/validate_topology.py --strict   # 경고도 오류로 처리
"""

import ast
import argparse
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List

PAIK_ROOT = Path(__file__).parent.parent
APPS_DIR = PAIK_ROOT / "apps"
HUB_MODULE = "star_craft"


def _collect_spoke_modules() -> List[str]:
    return [
        d.name
        for d in APPS_DIR.iterdir()
        if d.is_dir()
        and d.name != HUB_MODULE
        and not d.name.startswith("_")
        and d.name != "__pycache__"
        and (d / "__init__.py").exists()
    ]


SPOKE_MODULES = _collect_spoke_modules()


@dataclass
class Violation:
    file: str
    line: int
    kind: str      # "SPOKE_TO_SPOKE" | "HUB_TO_SPOKE"
    source: str
    target: str

    def __str__(self) -> str:
        label = {
            "SPOKE_TO_SPOKE": "스포크→스포크 직접 참조",
            "HUB_TO_SPOKE":   "허브→스포크 역방향 결합",
        }.get(self.kind, self.kind)
        return (
            f"  [{self.kind}] {self.file}:{self.line}\n"
            f"    {label}: apps.{self.source} → apps.{self.target}"
        )


def _extract_imports(file_path: Path) -> List[tuple[int, str]]:
    """Python 파일에서 (라인번호, import된 모듈명) 목록을 AST로 추출."""
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    results: List[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                results.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom) and node.module:
            results.append((node.lineno, node.module))
    return results


def _source_domain(file_path: Path) -> str | None:
    """파일이 속한 apps.XXX 도메인명을 반환. apps/ 외부면 None."""
    try:
        rel = file_path.relative_to(APPS_DIR)
    except ValueError:
        return None
    parts = rel.parts
    return parts[0] if parts else None


def check_topology() -> List[Violation]:
    violations: List[Violation] = []

    for py_file in APPS_DIR.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue

        source_domain = _source_domain(py_file)
        if not source_domain:
            continue

        rel_path = str(py_file.relative_to(PAIK_ROOT))

        for lineno, imported in _extract_imports(py_file):
            if not imported.startswith("apps."):
                continue

            parts = imported.split(".")
            if len(parts) < 2:
                continue
            target_domain = parts[1]

            # 규칙 1: 허브 → 스포크 금지
            if source_domain == HUB_MODULE and target_domain in SPOKE_MODULES:
                violations.append(Violation(
                    file=rel_path, line=lineno,
                    kind="HUB_TO_SPOKE",
                    source=source_domain, target=target_domain,
                ))

            # 규칙 2: 스포크 → 스포크 금지
            if (
                source_domain in SPOKE_MODULES
                and target_domain in SPOKE_MODULES
                and source_domain != target_domain
            ):
                violations.append(Violation(
                    file=rel_path, line=lineno,
                    kind="SPOKE_TO_SPOKE",
                    source=source_domain, target=target_domain,
                ))

    return violations


def main() -> None:
    parser = argparse.ArgumentParser(description="Star Topology Python Import 검증기")
    parser.add_argument("--strict", action="store_true", help="경고도 종료 코드 1로 처리")
    args = parser.parse_args()

    print("=" * 60)
    print("[Star Topology Validator] Python Import 검증")
    print(f"  Hub    : apps/{HUB_MODULE}")
    print(f"  Spokes : {', '.join(sorted(SPOKE_MODULES))}")
    print("=" * 60)

    violations = check_topology()

    if not violations:
        print("\n✅ 토폴로지 위반 없음. 모든 import 규칙 준수.\n")
        sys.exit(0)

    spoke_to_spoke = [v for v in violations if v.kind == "SPOKE_TO_SPOKE"]
    hub_to_spoke   = [v for v in violations if v.kind == "HUB_TO_SPOKE"]

    print(f"\n❌ 토폴로지 위반 {len(violations)}건 발견\n")

    if hub_to_spoke:
        print(f"  [허브→스포크 결합] {len(hub_to_spoke)}건 — 허브의 순수성 파괴")
        for v in hub_to_spoke:
            print(v)
        print()

    if spoke_to_spoke:
        print(f"  [스포크→스포크 직접 참조] {len(spoke_to_spoke)}건 — 허브 경유 필요")
        for v in spoke_to_spoke:
            print(v)
        print()

    print("수정 방법: 크로스-도메인 참조는 apps/star_craft 허브를 통해 인터페이스를 노출할 것.")
    sys.exit(1)


if __name__ == "__main__":
    main()
