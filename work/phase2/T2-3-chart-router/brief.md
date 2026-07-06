# TASK T2-3-chart-router
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 7f62805eb8a6ef89d1f4f449ead65ca9a3ec1f68
## 목표
차트 유형 분류 라우터 + 테마 변환 공통층: chart-request.json의 chartType을
supported|required_fallback|not_applicable 매트릭스(POC-VERDICT.md의 채택/제외/폴백 반영 —
mermaid 계열 유형은 graphviz 폴백)로 어댑터에 라우팅하는 단일 진입 CLI
(render-chart.mjs request.json → 어댑터 위임 → manifest 반환). 유형×엔진 매트릭스는
src/matrix.json으로 선언하고 라우팅 로직과 분리.
## 입력
incubator/packages/deck-charts/src/adapters/ (3어댑터 — 수정 금지), incubator/packages/deck-charts/poc/POC-VERDICT.md, incubator/contracts/chart-request.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-charts/src/{render-chart.mjs,matrix.json}, incubator/packages/deck-charts/tests/run-router.mjs, incubator/packages/deck-charts/tests/requests-router/
## 합격기준
supported 셀 전수 라우팅 green + mermaid계 유형의 graphviz 폴백 케이스 + not_applicable 거부 케이스 + 3어댑터 기존 테스트 회귀 green.
expectedCommand: cd incubator && node packages/deck-charts/tests/run-router.mjs
## 공통 금지사항
contracts/ 수정 금지. npm 신규 설치 금지. allowedWritePaths 밖 쓰기 금지. 상수 하드코딩 금지.
## 공통 완료 규약
expectedCommand 직접 실행 green 확인 후 result.md 기록.
