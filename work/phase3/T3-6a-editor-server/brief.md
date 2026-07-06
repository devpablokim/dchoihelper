# TASK T3-6a-editor-server (P9 독립 트랙 subtask a)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: d69d2a4465baa283c267c0875429685f356588c1
## 목표
deck-editor 1단계: vendor/slides-grab에 편집 서버/API가 있으면 그 코어를, 없으면 신규 최소 구현으로 —
node 내장 http 서버 + POST /api/apply (slides/*.html의 특정 data-slot-id 텍스트/스타일 패치 적용,
edit-manifest.json 기록: contracts/edit-manifest.schema.json 준수) + GET /api/slide/:id.
편집 적용 시 deck-plan/deck-manifest invalidation 마킹(PLAN P9 final artifact editor 모드).
## 입력
vendor/slides-grab/ (읽기만), incubator/contracts/{edit-manifest.schema.json,slide-html.contract.md,deck-manifest.schema.json}, incubator/examples/demo-phase1/slides/ (테스트 소재)
## 산출
allowedWritePaths: incubator/packages/deck-editor/ (src/, tests/, package.json)
## 합격기준
WORKERS T3-6a 게이트: API 통합 green — demo 슬라이드 사본에 패치 적용 → edit-manifest 스키마 통과
→ invalidation 마킹 확인 → 원본 무변경 확인. 서버 기동/종료가 테스트 안에서 완결.
expectedCommand: cd incubator && node packages/deck-editor/tests/run-api.mjs
## 금지사항
demo-phase1 원본 수정 금지 (사본으로). contracts/ 수정 금지. 외부 npm 금지.
undo/미리보기는 T3-6b 몫 — 이번 범위 밖.
