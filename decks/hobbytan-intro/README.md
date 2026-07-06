# 하비탄AI 소개덱 (hobbytan.com)

deck-factory 디자인 시스템(`skills/deck-factory`)으로 지은 9장짜리 회사 소개덱.
콘텐츠 출처는 hobbytan.com — AI 파워워크샵(5주 AI 슈퍼유저 육성 프로그램) 중심.

## 구성

| # | 슬롯 | 내용 |
|---|---|---|
| 01 | cover | 조직의 체질을 완전히 바꾸는, 5주. |
| 02 | statement | AI를 사는 것 ≠ 조직이 바뀌는 것 (문제 제기) |
| 03 | two-col | AI 파워워크샵 — 팀 단위 · 실전 · 팔로업 |
| 04 | kpi-3 | 11개사 · 80+ 슈퍼유저 · 중도 포기 0건 |
| 05 | flow | 프로그램 5요소 (커리큘럼→코칭→합숙→특강→90일 팔로업) |
| 06 | stat | 평균 ROI 12배 · 재구매율 80% |
| 07 | stat | 투자 800만원 → 예상 연간 수익 9,600만원 |
| 08 | bento | 워크샵 너머 — 시스템 설정 · 웹사이트 · 컨설팅 · AI 클럽 |
| 09 | closing | 연락처 (pablo@hobbytan.com) |

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
