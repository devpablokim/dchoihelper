# TASK T3-2b-resolve-loop (P7 plan 단계 subtask b)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: c2c7d0c3de6d3538e72b94f8c41b35f93aa477a1
## 목표
plan 단계 2/4 — 오버플로 해소 루프: T3-2a의 plan-report(반려 대상)를 받아 계약 정본
(contracts/layout-manifest overflowPolicy, copy-reject attempt 상한 2회)대로 처리한다.
분기: (1) 대체 레이아웃 재선택 시도(같은 archetype 내 여유 큰 템플릿),
(2) kind별 터미널 — body는 splitGranularity 경계 연속 슬라이드 분할, title/source는 copy-reject 반려,
caption은 allowLossyTruncate 슬롯만 truncate+감사 기록,
(3) 반려 상한 도달 시 releaseBlocked=true + needsHumanReview=true 마킹 (deck-plan 계약 필드).
deck-copy reject-handler(기존 도구)를 반려 지시문 생성에 재사용하라.
## 입력
incubator/packages/deck-assembler/src/plan/, incubator/packages/deck-copy/src/reject-handler.mjs,
incubator/contracts/, incubator/packages/deck-layouts/manifests/
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/plan/resolve-loop.mjs,
incubator/packages/deck-assembler/tests/run-plan-b.mjs, incubator/packages/deck-assembler/tests/fixtures-resolve/
## 합격기준
WORKERS T3-2b 게이트: 해소 3분기 케이스 각 1 + 반려 상한 케이스(attempt 2 초과 → releaseBlocked,
데드락·무한루프 없음 확인) green. 기존 run-plan-a·run-golden 회귀 green.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-plan-b.mjs && node packages/deck-assembler/tests/run-plan-a.mjs
## 금지사항
폰트 축소로 해소 금지 (불변식). contracts/·reject-handler 수정 금지. 차트-출처 페어링은 T3-2c 몫.
