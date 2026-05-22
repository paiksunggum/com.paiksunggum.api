"""GET / 브라우저용 메인 안내 HTML."""


def home_page_html() -> str:
    return """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TJ Watson API</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      background: #f8fafc;
      color: #0f172a;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    main {
      max-width: 32rem;
      width: 100%;
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 1.75rem;
      box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
    }
    h1 { margin: 0 0 0.5rem; font-size: 1.35rem; }
    p { margin: 0 0 1.25rem; color: #64748b; font-size: 0.9rem; line-height: 1.5; }
    ul { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }
    a {
      display: block;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      background: #f1f5f9;
      color: #0f172a;
      text-decoration: none;
      font-weight: 500;
    }
    a:hover { background: #e2e8f0; }
    a.primary { background: #0f172a; color: #fff; }
    a.primary:hover { background: #1e293b; }
    code { font-size: 0.85em; background: #f1f5f9; padding: 0.1em 0.35em; border-radius: 4px; }
  </style>
</head>
<body>
  <main>
    <h1>TJ Watson API</h1>
    <p>백엔드가 실행 중입니다. 아래 링크에서 API 문서와 DB 연결을 확인하세요.</p>
    <ul>
      <li><a class="primary" href="/docs">API 문서 (Swagger)</a></li>
      <li><a href="/redoc">API 문서 (ReDoc)</a></li>
      <li><a href="/db-check">DB 연결 확인</a></li>
      <li><a href="/chat">채팅 페이지</a></li>
    </ul>
    <p style="margin-top:1.25rem;margin-bottom:0;font-size:0.8rem;">
      서버 실행: <code>backend</code> 폴더에서
      <code>python run.py</code> 또는 <code>uvicorn apps.main:app --reload --host 0.0.0.0 --port 8000</code>
    </p>
  </main>
</body>
</html>"""
