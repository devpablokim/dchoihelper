# TASK T3-2a-binding-capacity (P7 plan 단계 subtask a)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 1d6f208bc7764a694600b794c52c12127838653b
## 목표
plan 단계 1/4 — 바인딩·수용량 검사: deck-plan.json(계약)과 copy.json·chart-manifest·image-manifest를
받아 (1) 각 슬라이드 slots의 contentRef가 실존 콘텐츠를 가리키는지 바인딩 검증,
(2) 텍스트 슬롯별 capacity.mjs(deck-layouts) 추정으로 수용량 검사 — 초과 슬롯은
copy-reject.json 초안(계약 스키마, attempt 카운터 포함) 생성,
(3) 결과 plan-report.json (검증 통과 슬라이드 / 반려 대상 / 근거 수치).
## 입력
incubator/contracts/ (deck-plan, copy, copy-reject, chart-manifest, image-manifest, layout-manifest 스키마),
incubator/packages/deck-layouts/scripts/capacity.mjs, incubator/packages/deck-layouts/manifests/,
incubator/packages/deck-storyline/corpus/demo-topic-1/ (골든 소재)
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/plan/binding.mjs,
incubator/packages/deck-assembler/src/plan/capacity-check.mjs,
incubator/packages/deck-assembler/tests/run-plan-a.mjs, incubator/packages/deck-assembler/tests/golden-plan/
## 합격기준
WORKERS T3-2a 게이트: 바인딩 골든 케이스 — 정상 deck-plan green + 댕글링 contentRef 검출 +
수용량 초과 시 copy-reject 초안이 스키마 통과. T3-1 골든 회귀 green.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-plan-a.mjs && node packages/deck-assembler/tests/run-golden.mjs
## 금지사항
capacity.mjs·contracts/ 수정 금지. 해소 루프(반려 처리)는 T3-2b 몫 — 초안 생성까지만.
