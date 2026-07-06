# TASK T3-2d-measured-roundtrip (P7 plan subtask d — plan 트랙 종결)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 82d0180f94035ba3b43e44b2a68607b87cb14ade
## 목표
plan 단계 4/4 — 추정/실측 이음매: compose가 반환하는 measured-overflow.json(계약 스키마,
아직 compose 미구현이므로 mock 입력)을 받아 (1) 해당 슬라이드 강제 분할 재계획(T3-2b 해소 루프 재호출),
(2) 재왕복 상한 1회 — 재실측 후에도 초과면 needsHumanReview+releaseBlocked (PLAN P7 규약),
(3) 왕복 이력을 plan-report에 기록.
## 입력
incubator/packages/deck-assembler/src/plan/, incubator/contracts/measured-overflow.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/plan/measured-roundtrip.mjs,
incubator/packages/deck-assembler/tests/run-plan-d.mjs, incubator/packages/deck-assembler/tests/fixtures-measured/
## 합격기준
WORKERS T3-2d 게이트: 왕복 케이스(1회 재계획 후 해소) + 상한 케이스(재왕복 후에도 초과 → releaseBlocked)
green. run-plan-a/b/c 회귀 green.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-plan-d.mjs && node packages/deck-assembler/tests/run-plan-c.mjs
## 금지사항
resolve-loop 파괴적 수정 금지(호출·확장만). contracts/ 수정 금지.
