import sys
from pathlib import Path

_here = Path(__file__).parent

# paik/ → "apps.titanic.*" 임포트 활성화
_paik_dir = str(_here.parent.parent.parent)
if _paik_dir not in sys.path:
    sys.path.insert(0, _paik_dir)

