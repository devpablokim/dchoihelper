# TASK T1-5-data-chart
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 81fe8ce9be973312e1b9c0e5ff3e027f33763f57 / schemaVersion: v0.1.0-draft
## 목표
레이아웃 템플릿 묶음 "data-chart" 를 구현한다 — 데이터 계열 4종: 차트 단독(차트 슬롯+출처 슬롯 페어), 차트+해설 2분할, KPI 빅넘버 3분할, 표 대체 카드 그리드. 수치 슬라이드는 source 슬롯 필수 바인딩
각 템플릿: (1) incubator/contracts/slide-html.contract.md 규약을 따르는 템플릿 HTML
(data-layout-id, data-slot-id/kind, 1280x720 고정, 토큰은 CSS 변수 var(--token)로만 소비),
(2) incubator/contracts/layout-manifest.schema.json 을 만족하는 매니페스트 조각
packages/deck-layouts/manifests/data-chart.json (슬롯 bbox·kind·overflowPolicy·capacity는 capacity.mjs로 산출해 기입).
## 입력
incubator/contracts/{slide-html.contract.md,layout-manifest.schema.json,deck-constants.json},
incubator/packages/deck-layouts/scripts/{capacity.mjs,overflow-check.mjs},
incubator/packages/deck-tokens/presets/vercel/tokens.json (렌더 검증용 대표 프리셋)
## 산출
allowedWritePaths: incubator/packages/deck-layouts/templates/data-chart/*.html,
incubator/packages/deck-layouts/manifests/data-chart.json,
incubator/packages/deck-layouts/tests/run-data-chart.mjs, incubator/packages/deck-layouts/tests/content-data-chart/
## 합격기준
WORKERS.md T1-5 게이트: (1) 대표 콘텐츠 주입 후 overflow-check.mjs 렌더 검사 — 오버플로 0건 +
폰트 하한 DOM 검사 통과 (4종 전부), (2) 매니페스트가 layout-manifest.schema.json 검증 통과,
(3) capacity 기입값이 capacity.mjs 산출과 일치. opus 시각 판정은 fable 후속 게이트.
expectedCommand: cd incubator && node packages/deck-layouts/tests/run-data-chart.mjs
## 금지사항
contracts/·scripts/(capacity.mjs, overflow-check.mjs) 수정 금지. 다른 묶음 디렉토리 접근 금지.
색상·크기 하드코딩 금지 (토큰 변수와 deck-constants만). 폰트 축소(auto-fit) 금지.
manifests/data-chart.json 외 매니페스트 파일 생성 금지 (통합 매니페스트는 별도 태스크).
