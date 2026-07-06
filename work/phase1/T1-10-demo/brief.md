# TASK T1-10-demo (Phase 1 완료 정의: 토큰 → 레이아웃 → grader 관통 데모)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: b71f10b4a9f693948d8599bbc50240cd46542056 / schemaVersion: v0.1.0-draft
## 목표
Phase 1 관통 데모 1건: (1) vercel 프리셋 tokens.json의 토큰을 CSS 변수로 바인딩해
레이아웃 템플릿 3종(커버 1, 본문 1, 데이터 1)에 실제 한국어 대표 콘텐츠를 채운 데모 덱
(slides/*.html 3장, slide-html 계약 준수)을 생성하고, (2) overflow-check green을 확인한 뒤,
(3) deck-grader를 돌려 grade-report에서 hard fail 0을 산출한다.
## 입력
incubator/packages/deck-tokens/presets/vercel/tokens.json, incubator/packages/deck-layouts/templates/,
incubator/packages/deck-grader/src/, incubator/contracts/slide-html.contract.md
## 산출
allowedWritePaths: incubator/examples/demo-phase1/ (slides/*.html, tokens 바인딩 css, README.md,
build-demo.mjs — 재생성 가능 스크립트), incubator/examples/demo-phase1/report/
## 합격기준
PLAN.md Phase 1 완료 정의 인용: "토큰 → 레이아웃 → grader 관통 데모 1건" —
demo 3장 전부 overflow-check green + grader hard fail 0 + 리포트가 grade-report.schema.json 검증 통과.
expectedCommand: cd incubator && node examples/demo-phase1/build-demo.mjs && node packages/deck-layouts/scripts/overflow-check.mjs examples/demo-phase1/slides && node packages/deck-grader/src/cli.mjs examples/demo-phase1/slides --out examples/demo-phase1/report 2>/dev/null || node examples/demo-phase1/run-demo-gate.mjs
게이트 실행 방식이 위와 다르면 run-demo-gate.mjs 하나로 전체를 묶어 exit code로 판정되게 하라.
## 금지사항
packages/·contracts/ 수정 금지 (소비만). 템플릿 원본 수정 금지 (사본 바인딩). allowedWritePaths 밖 쓰기 금지.
