# TASK T1-5f-margin-hardening (T1-5 재분해 — data-chart·image-visual 플레이크 종결)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 81fe8ce9be973312e1b9c0e5ff3e027f33763f57 / schemaVersion: v0.1.0-draft
## 배경 (실패 근거)
data-chart와 image-visual 묶음이 런마다 pass/fail이 갈리는 플레이크 상태다. 원인: 일부 템플릿의
대표 콘텐츠가 슬롯 한계 1px 이내에 붙어 있어 서브픽셀 렌더 차이로 오버플로가 뒤집힌다.
직전 실측: image-text-split에 content-overflow 검출, data-chart-card-grid도 과거 검출 이력.
## 목표
두 묶음의 전 템플릿(8종)에 대해 "대표 콘텐츠 기준 세로·가로 여유가 항상 8px 이상"이 되도록
템플릿을 하드닝한다. 여백/행간/슬롯 치수 조정과 대표 콘텐츠 축소로만 — 폰트 크기는
fontFloors 미만 금지, 게이트·검사기 로직 수정 절대 금지.
## 방법
overflow-check.mjs 리포트의 overflowPx/잔여 여유를 직접 측정해 여유 8px 미만인 템플릿을 전부 찾고
(현재 fail 나는 것만이 아니라 경계 근접 전부), 수정 후 manifests의 capacity를 capacity.mjs로 재산출.
## 산출
allowedWritePaths: incubator/packages/deck-layouts/templates/{data-chart,image-visual}/*.html,
incubator/packages/deck-layouts/manifests/{data-chart,image-visual}.json,
incubator/packages/deck-layouts/tests/content-{data-chart,image-visual}/
## 합격기준
run-data-chart.mjs 와 run-image-visual.mjs 를 각 5회 연속 실행해 전부 green (플레이크 소멸 증명).
다른 3개 묶음 테스트 회귀 없음 (run-cover-section, run-text-content, run-closing-special 각 1회 green).
expectedCommand: cd incubator && for i in 1 2 3 4 5; do node packages/deck-layouts/tests/run-data-chart.mjs && node packages/deck-layouts/tests/run-image-visual.mjs || exit 1; done
## 금지사항
contracts/·scripts/·게이트 테스트 로직 수정 금지. 폰트 축소로 여유 확보 금지(여백 우선). allowedWritePaths 밖 쓰기 금지.
