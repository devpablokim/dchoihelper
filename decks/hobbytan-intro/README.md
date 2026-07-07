# 하비탄AI 소개덱 (hobbytan.com)

deck-factory 디자인 시스템(`skills/deck-factory`)으로 지은 10장짜리 회사 소개덱.
콘텐츠 출처는 hobbytan.com — AI 파워워크샵(6주 AI 슈퍼유저 육성: 3주 공통 교육 + 3주 개별 프로덕트 개발) 중심. 시장 수치는 한국은행·McKinsey State of AI 2025 조사 기반.

## 구성

| # | 슬롯 | 내용 |
|---|---|---|
| 01 | cover | 조직의 체질을 완전히 바꾸는, 6주. |
| 02 | statement | 도입은 늘었는데 성과 조직은 드물다 (why now) |
| 03 | kpi-3 | 시장 격차 — 활용률 51%(한국은행) · 성과 못 본 기업 80% · 고성과 조직 6%(McKinsey 2025) |
| 04 | two-col | AI 파워워크샵 — 리터러시 · 툴 마스터 · 프로덕트 증명 |
| 05 | timeline | 6주 여정 — 3주 공통 교육 + 3주 개별 프로덕트 개발 |
| 06 | kpi-3 | 18개사 진행 · 80+ 슈퍼유저 · 중도 포기율 5% 미만 |
| 07 | stat | 평균 ROI 12배 · 재구매율 80% |
| 08 | stat | 투자 800만원 → 예상 연간 수익 9,600만원 |
| 09 | bento | 워크샵 너머 — 시스템 설정 · 웹사이트 · 컨설팅 · AI 클럽 |
| 10 | closing | 연락처 (pablo@hobbytan.com) |

## 렌더

Pretendard·JetBrains Mono 폰트를 시스템에 설치한 뒤:

```bash
pip install playwright pillow
python3 - <<'EOF'
from playwright.sync_api import sync_playwright
import glob, os
d = os.path.dirname(os.path.abspath('.')) if False else '.'
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1920,'height':1080})
    for f in sorted(glob.glob('slide-*.html')):
        pg.goto('file://'+os.path.abspath(f))
        pg.wait_for_timeout(400)
        pg.screenshot(path='out/'+os.path.basename(f).replace('.html','.png'))
    b.close()
EOF
```

주의: 헤드리스 크로미움 CLI의 `--screenshot`은 새 headless 모드에서 창 크기에 UI 영역이
포함돼 하단이 잘린다 — Playwright의 viewport 지정 방식을 쓸 것.

렌더 산출물은 `out/`(slide-NN.png 9장 + `hobbytan-intro-deck.pdf`).
