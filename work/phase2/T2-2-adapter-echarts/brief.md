# TASK T2-2-adapter-echarts
## 메타
taskType: code / determinismClass: canonicalized / mode: attended / baseCommit: 1777bf1c4704e0321ef5d417c85ab99b2aad4e87 / schemaVersion: v0.1.0-draft
## 목표
차트 엔진 "echarts" 렌더 어댑터를 구현한다: contracts/chart-request.schema.json 을 만족하는
chart-request.json 을 입력받아 SVG(+PNG)를 렌더하고 contracts/chart-manifest.schema.json 을
만족하는 chart-manifest.json 조각을 산출하는 CLI.
담당 차트 유형: pie, donut, stacked-bar, heatmap, radar, gauge
## 핵심 규약
(1) 디자인 토큰 주입: request의 tokensRef가 가리키는 tokens.json에서 색 팔레트·폰트·폰트크기를
읽어 차트 스타일에 적용 (하드코딩 금지). 폰트는 Pretendard(assets/fonts 데이터 URL — poc/lib 재사용).
(2) 출처 계약: request의 sourceRef를 manifest에 그대로 전달하고 sourceLabel은 파생 표시값으로 기입.
sourceRef 없는 수치 차트 요청은 렌더 거부(exit 1 + 사유). — PLAN.md P3/P8 신뢰성 게이트 정합
(3) 렌더 재현성: 같은 request 2회 렌더 시 SVG가 canonical 비교(volatile 필드 제거)로 동일.
(4) 한글 골든: poc/lib/glyph-check.mjs 재사용으로 한글 깨짐 자동 검사 통과.
## 입력
incubator/contracts/{chart-request.schema.json,chart-manifest.schema.json,tokens.schema.json},
incubator/packages/deck-charts/poc/echarts/ (렌더 코드 승격 재료), incubator/packages/deck-charts/poc/lib/,
incubator/packages/deck-tokens/presets/vercel/tokens.json (테스트용)
## 산출
allowedWritePaths: incubator/packages/deck-charts/src/adapters/echarts.mjs,
incubator/packages/deck-charts/src/lib/ (어댑터 공통 유틸 — 다른 어댑터와 겹치면 이 태스크가 먼저 만든 것 우선, 있으면 재사용만),
incubator/packages/deck-charts/tests/run-echarts.mjs, incubator/packages/deck-charts/tests/requests-echarts/,
incubator/packages/deck-charts/package.json
## 합격기준
담당 유형 전수: 골든 request → 렌더 green + manifest 스키마 검증 통과 + 한글 검사 green +
canonical 재현 비교 일치 + sourceRef 누락 거부 케이스.
expectedCommand: cd incubator && node packages/deck-charts/tests/run-echarts.mjs
## 금지사항
contracts/ 수정 금지. poc/ 코드 수정 금지(복사·승격만). 새 npm 설치 금지.
다른 엔진 어댑터 파일 수정 금지. allowedWritePaths 밖 쓰기 금지.
