# RETRY 2 — attempt-1 실패 근거 (900초 타임아웃으로 도중 종료, 최종 시도)
attempt-1이 허용오차 완화 작업 중 타임아웃으로 죽었다. tests/run-image-visual.mjs 가
반쯤 수정된 상태일 수 있다. 현재 파일 상태를 먼저 확인하고, retry-1 지시(좌표 비교 허용오차
1.5px 완화, 게이트 본질 유지)를 완결하라. 오버플로가 실제로 검출되면 템플릿 여백을
capacityMargin 이상 확보하는 방향으로 고쳐라 (폰트 하한 준수, 게이트 로직 수정 금지).
완료 후 run-image-visual.mjs 2회 연속 green 확인, out/attempt-2/result.md에 기록.
# TASK T1-5-image-visual
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 81fe8ce9be973312e1b9c0e5ff3e027f33763f57 / schemaVersion: v0.1.0-draft
## 목표
레이아웃 템플릿 묶음 "image-visual" 를 구현한다 — 이미지 계열 4종: 풀블리드 이미지+텍스트 오버레이(textSafeRegions 존중), 이미지+텍스트 2분할, 이미지 3그리드, 인용+배경이미지. 오버레이 대비 확보 구조 필수
각 템플릿: (1) incubator/contracts/slide-html.contract.md 규약을 따르는 템플릿 HTML
(data-layout-id, data-slot-id/kind, 1280x720 고정, 토큰은 CSS 변수 var(--token)로만 소비),
(2) incubator/contracts/layout-manifest.schema.json 을 만족하는 매니페스트 조각
packages/deck-layouts/manifests/image-visual.json (슬롯 bbox·kind·overflowPolicy·capacity는 capacity.mjs로 산출해 기입).
## 입력
incubator/contracts/{slide-html.contract.md,layout-manifest.schema.json,deck-constants.json},
incubator/packages/deck-layouts/scripts/{capacity.mjs,overflow-check.mjs},
incubator/packages/deck-tokens/presets/vercel/tokens.json (렌더 검증용 대표 프리셋)
## 산출
allowedWritePaths: incubator/packages/deck-layouts/templates/image-visual/*.html,
incubator/packages/deck-layouts/manifests/image-visual.json,
incubator/packages/deck-layouts/tests/run-image-visual.mjs, incubator/packages/deck-layouts/tests/content-image-visual/
## 합격기준
WORKERS.md T1-5 게이트: (1) 대표 콘텐츠 주입 후 overflow-check.mjs 렌더 검사 — 오버플로 0건 +
폰트 하한 DOM 검사 통과 (4종 전부), (2) 매니페스트가 layout-manifest.schema.json 검증 통과,
(3) capacity 기입값이 capacity.mjs 산출과 일치. opus 시각 판정은 fable 후속 게이트.
expectedCommand: cd incubator && node packages/deck-layouts/tests/run-image-visual.mjs
## 금지사항
contracts/·scripts/(capacity.mjs, overflow-check.mjs) 수정 금지. 다른 묶음 디렉토리 접근 금지.
색상·크기 하드코딩 금지 (토큰 변수와 deck-constants만). 폰트 축소(auto-fit) 금지.
manifests/image-visual.json 외 매니페스트 파일 생성 금지 (통합 매니페스트는 별도 태스크).
