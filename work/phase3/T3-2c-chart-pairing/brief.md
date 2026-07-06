# TASK T3-2c-chart-pairing (P7 plan subtask c)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 82d0180f94035ba3b43e44b2a68607b87cb14ade
## 목표
plan 단계 3/4 — 차트-출처 페어링 검증: deck-plan의 차트 슬롯 바인딩에 대해
(1) chart-manifest의 sourceRef가 claims/source-pack 실존 id인지 (T2-10 claims-validate 재사용),
(2) 수치 차트 슬라이드에 source 슬롯 바인딩이 함께 존재하는지, (3) 위반 시 plan 단계 실패
(PLAN P3/P8 계약 — 익스포트까지 가기 전에 차단). 결과는 plan-report에 pairing 섹션 추가.
## 입력
incubator/packages/deck-assembler/src/plan/, incubator/packages/deck-storyline/src/claims-validate.mjs,
incubator/contracts/{chart-manifest.schema.json,deck-plan.schema.json}
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/plan/chart-pairing.mjs,
incubator/packages/deck-assembler/tests/run-plan-c.mjs, incubator/packages/deck-assembler/tests/fixtures-pairing/
## 합격기준
WORKERS T3-2c 게이트: 페어링 음성 케이스(댕글링 sourceRef / source 슬롯 부재) 검출 + 정상 케이스 green.
run-plan-a/b 회귀 green.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-plan-c.mjs && node packages/deck-assembler/tests/run-plan-b.mjs
## 금지사항
claims-validate 수정 금지(재사용만). contracts/ 수정 금지.
