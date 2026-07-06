# TASK T0-6-license-evidence

## 메타
taskType: research
determinismClass: nondeterministic
mode: attended
baseCommit: 59b29e93bf3231af44fc299a57ac88acd21a6e5f
schemaVersion: n/a

## 목표
PLAN.md 8절 리스크 레지스터의 라이선스 잔여 확인 항목을 원문 근거로 닫고,
파이프라인이 소비할 기계 판독 라이선스 표와 증거 아카이브를 만든다.
완료는 "모든 대상 자산에 대해 (a) 라이선스 판정, (b) 원문 스냅샷, (c) 출처 URL과
캡처 날짜가 남아 있고, 미확정 항목은 미확정으로 정직하게 표기된 상태"다.

## 입력
- /home/seunghyeong/deck-factory/PLAN.md 8절 (리스크 레지스터의 라이선스 행들)
- /home/seunghyeong/deck-factory/research/toss-design.md, korean-design-systems.md,
  chart-libs.md, astryx.md, manim-video.md, slides-grab.md (1차 조사 결과 — 재검증 대상)

## 산출
allowedWritePaths:
- incubator/docs/license-table.json — 항목: asset, kind(font|code|emoji|tool|data),
  license, commercialUse(yes|no|conditional|unverified), conditions[], evidencePath,
  sourceUrl, retrievedAt, verdict(adopt|adopt-with-conditions|reject|defer)
- incubator/docs/license-evidence/<asset>/ — 라이선스 원문 스냅샷(md 또는 txt)
- incubator/docs/license-notes.md — 판정 근거 요약과 미확정 목록

대상 자산 (최소): Pretendard, TossFace, Astryx(@astryxdesign/*), Montage, KRDS,
decktape, MVP 차트 4엔진(Vega-Lite, ECharts, Mermaid, Graphviz)과 Kroki,
slides-grab, manim(CE), hyperframes, gpt-image 계열 생성물의 상업적 사용 약관.

## 합격기준
PLAN.md Phase 0 인용: "라이선스 확인 잔여 작업 처리 + license evidence archive" —
license-table.json이 위 스키마로 전 대상을 커버하고, 각 행의 evidencePath가 실존하며,
commercialUse=unverified 항목은 사유와 후속 확인 방법이 license-notes.md에 있을 것.
TossFace는 "원본 무수정 재배포, 저작권 안내 동봉" 조건 확인이 원문 스냅샷으로 뒷받침될 것.
expectedCommand: node -e "JSON.parse(require('fs').readFileSync('incubator/docs/license-table.json'))" (파싱 성공 + fable이 evidencePath 실존 확인)

## 금지사항
원문을 찾지 못한 자산에 대해 판정을 추정으로 채우지 말 것 — unverified로 두고 사유 기록.
날조 URL 금지. allowedWritePaths 밖 쓰기 금지. 이모지·볼드(**) 금지.

## 참조
웹 접근이 차단되면 r.jina.ai 프록시, GitHub raw, 웨이백 순으로 우회.
