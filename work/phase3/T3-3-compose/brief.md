# TASK T3-3-compose (P7 compose 단계 — 순차)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 47fe5d64c7d8ac321a09cbff9f12d700e04fb124
## 목표
compose 단계: plan 통과한 deck-plan.json을 받아 (1) 레이아웃 템플릿(deck-layouts)에
콘텐츠(copy/chart-manifest/image-manifest)를 바인딩해 slides/*.html 생성 —
slide-html.contract.md 규약(data-slide-id/layout-id/slot-id, 자체 완결 1파일) 준수,
(2) 토큰 CSS 변수 바인딩(tokens.json), (3) 생성 후 overflow-check.mjs 실측 —
초과 슬라이드는 measured-overflow.json 반환(T3-2d 소비 계약), 통과 시 deck-manifest.json 생성
(exportStatus 규약 포함), (4) T3-1 이식 코어를 렌더 기반으로 재사용.
## 입력
incubator/packages/deck-assembler/src/, incubator/packages/deck-layouts/{templates,manifests,scripts}/,
incubator/contracts/, incubator/packages/deck-tokens/presets/vercel/, incubator/packages/deck-storyline/corpus/demo-topic-1/
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/compose/,
incubator/packages/deck-assembler/tests/run-compose.mjs, incubator/packages/deck-assembler/tests/golden-compose/
## 합격기준
WORKERS T3-3 게이트: 결정론 — 같은 deck-plan 2회 compose HTML diff 0 (해시 게이트) +
전 산출 슬라이드 validate-slide-html 통과 + overflow-check 실측 green + deck-manifest 스키마 통과.
plan a~d·골든 회귀 green.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-compose.mjs && node packages/deck-assembler/tests/run-plan-d.mjs
## 금지사항
템플릿·contracts/ 수정 금지. 폰트 축소 금지. 타임스탬프 등 volatile 값 HTML 삽입 금지 (결정론).
