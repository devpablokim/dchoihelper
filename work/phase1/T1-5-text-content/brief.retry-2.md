# RETRY 2 — attempt-1 게이트 실패 근거 (최종 시도, 상한 도달)
fable 재실행에서 실제 오버플로 검출: text-content 묶음의 경계선 템플릿이 서브픽셀 렌더 차이로 넘친다.
(text-two-column-compare / data-chart-card-grid overflow report != ok)
이는 허용오차 문제가 아니라 템플릿이 capacityMargin 없이 꽉 차게 설계된 문제다.

수정 지시: 해당 묶음 템플릿들의 슬롯 여유를 확보하라 — 대표 콘텐츠 기준 세로 여유가
deck-constants.json capacityMargin 이상 남도록 (패딩/행간/슬롯 높이 조정 또는 대표 콘텐츠 축소.
폰트 크기 하향은 fontFloors 위반 아닌 범위에서만, 축소 대신 여백 확보 우선).
매니페스트 capacity는 capacity.mjs로 재산출해 갱신. 오버플로 게이트 로직 수정 절대 금지.
완료 후 run-text-content.mjs 를 2회 연속 실행해 둘 다 green 확인, out/attempt-2/result.md에 기록.
# TASK T1-5-text-content
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 81fe8ce9be973312e1b9c0e5ff3e027f33763f57 / schemaVersion: v0.1.0-draft
## 목표
레이아웃 템플릿 묶음 "text-content" 를 구현한다 — 본문 텍스트 계열 4종: 1컬럼 액션타이틀+불릿, 2컬럼 비교, 텍스트+강조박스, 풀텍스트 서술형. 액션타이틀 위계(제목>부제>본문) 강제
각 템플릿: (1) incubator/contracts/slide-html.contract.md 규약을 따르는 템플릿 HTML
(data-layout-id, data-slot-id/kind, 1280x720 고정, 토큰은 CSS 변수 var(--token)로만 소비),
(2) incubator/contracts/layout-manifest.schema.json 을 만족하는 매니페스트 조각
packages/deck-layouts/manifests/text-content.json (슬롯 bbox·kind·overflowPolicy·capacity는 capacity.mjs로 산출해 기입).
## 입력
incubator/contracts/{slide-html.contract.md,layout-manifest.schema.json,deck-constants.json},
incubator/packages/deck-layouts/scripts/{capacity.mjs,overflow-check.mjs},
incubator/packages/deck-tokens/presets/vercel/tokens.json (렌더 검증용 대표 프리셋)
## 산출
allowedWritePaths: incubator/packages/deck-layouts/templates/text-content/*.html,
incubator/packages/deck-layouts/manifests/text-content.json,
incubator/packages/deck-layouts/tests/run-text-content.mjs, incubator/packages/deck-layouts/tests/content-text-content/
## 합격기준
WORKERS.md T1-5 게이트: (1) 대표 콘텐츠 주입 후 overflow-check.mjs 렌더 검사 — 오버플로 0건 +
폰트 하한 DOM 검사 통과 (4종 전부), (2) 매니페스트가 layout-manifest.schema.json 검증 통과,
(3) capacity 기입값이 capacity.mjs 산출과 일치. opus 시각 판정은 fable 후속 게이트.
expectedCommand: cd incubator && node packages/deck-layouts/tests/run-text-content.mjs
## 금지사항
contracts/·scripts/(capacity.mjs, overflow-check.mjs) 수정 금지. 다른 묶음 디렉토리 접근 금지.
색상·크기 하드코딩 금지 (토큰 변수와 deck-constants만). 폰트 축소(auto-fit) 금지.
manifests/text-content.json 외 매니페스트 파일 생성 금지 (통합 매니페스트는 별도 태스크).
