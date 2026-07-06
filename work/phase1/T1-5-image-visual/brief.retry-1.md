# RETRY 1 — attempt-0 게이트 실패 근거
테스트는 워커 렌더 시점 좌표를 과도한 정밀도로 스냅샷 고정했다. fable 재실행에서
서브픽셀 렌더 차이로 실패: 예) cover-title.kicker.y expected 154.66666, got 154.65625 (차이 0.01px).
이는 게이트 본질(오버플로 0, 폰트 하한, 매니페스트 스키마, capacity 대조)이 아닌 환경 노이즈다.

수정 지시 (이것만 수행, 템플릿·매니페스트 수정 금지):
incubator/packages/deck-layouts/tests/run-image-visual.mjs 의 좌표/치수 비교 허용오차를 1.5px로 완화하라
(assertClose 계열 tolerance). 판정 자체를 없애지 말 것 — bbox가 매니페스트 선언과 1.5px 내 일치는 유지.
오버플로·폰트 하한·스키마 검증 로직은 손대지 말 것.
수정 후 테스트를 2회 연속 실행해 둘 다 green임을 확인하고 결과를 out/attempt-1/result.md에 남겨라.
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
