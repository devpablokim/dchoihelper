# TASK T1-5g-font-canonical (T1-5 재분해 2 — 렌더 폰트 정본화로 환경 갈림 종결)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 81fe8ce9be973312e1b9c0e5ff3e027f33763f57 / schemaVersion: v0.1.0-draft
## 배경 (실패 근거)
레이아웃 게이트가 실행 환경의 폰트에 따라 갈린다 — 검증 환경(Pretendard 실폰트)에서
data-chart-card-grid title이 한 줄 더 감겨 overflowPx y:40, 워커 샌드박스(다른 폴백 폰트)에선 통과.
어느 쪽에서 튜닝해도 반대편에서 깨지는 구조적 문제. 해법: 리포에 vendoring된 폰트로 렌더를 정본화.
incubator/assets/fonts/ 에 Pretendard Regular/SemiBold/Bold otf + LICENSE가 준비돼 있다 (fable이 배치).
## 목표
(1) overflow-check.mjs 렌더에 정본 폰트 주입: 페이지 로드 시 @font-face로 vendored Pretendard를
등록하고 --font-sans가 'Pretendard'를 가리키게 하는 스타일 주입 옵션을 기본 활성으로 추가
(파일 URL 절대경로, 폰트 로드 완료 대기 후 측정 — document.fonts.ready).
(2) 정본 폰트 기준으로 5묶음 20템플릿 전수 재측정, 오버플로/여유 8px 미만 템플릿의
여백·콘텐츠를 수정 (fontFloors 준수, 폰트 축소보다 여백·콘텐츠 축소 우선).
(3) manifests capacity 재산출 (capacity.mjs).
## 산출
allowedWritePaths: incubator/packages/deck-layouts/scripts/overflow-check.mjs (폰트 주입 부분만),
incubator/packages/deck-layouts/templates/**, incubator/packages/deck-layouts/manifests/*.json,
incubator/packages/deck-layouts/tests/**
## 합격기준
5묶음 테스트(run-cover-section/text-content/data-chart/image-visual/closing-special) 전부,
연속 3회 라운드 전체 green. run-overflow.mjs(T1-6 자체 테스트) 회귀 green.
expectedCommand: cd incubator && for i in 1 2 3; do for b in cover-section text-content data-chart image-visual closing-special; do node packages/deck-layouts/tests/run-$b.mjs || exit 1; done; done && node packages/deck-layouts/tests/run-overflow.mjs
## 금지사항
오버플로 판정 로직·임계값 수정 금지 (폰트 주입만 추가). contracts/ 수정 금지.
assets/fonts/ 수정 금지 (소비만). allowedWritePaths 밖 쓰기 금지.
