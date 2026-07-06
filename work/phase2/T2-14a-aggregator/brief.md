# TASK T2-14a-aggregator
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 847e176b64f6125ec0014a9fe052d507921fb483
## 목표
grader 종합점수 집계기: (1) rules-{typo,color,align,dataviz,trust,a11y}.yaml 조각을 로드해
grader.yaml scoring 스펙(카테고리 6종 가중치·a11yAssignment — fable 확정, 수정 금지)대로
규칙 점수 → 카테고리 정규화(0~100) → 가중합을 계산, (2) 규칙별 만점·감점 함수 프레임
(위반 건수·정도 기반 — 규칙 yaml에 scoring 필드 없으면 균등 기본값), (3) grade-report.json에
categoryScores·totalScore 기입 (grade-report.schema.json 준수 — 스키마 수정 금지),
(4) semantic-gate.json의 failBranches를 hard fail 경로로 연결 (prefilter 호출, opus 판정은 스텁 인터페이스만).
## 입력
incubator/packages/deck-grader/{grader.yaml,rules-*.yaml,semantic-gate.json,src/}, incubator/contracts/grade-report.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-grader/src/aggregate.mjs, incubator/packages/deck-grader/src/cli.mjs(있으면 확장, 없으면 신설), incubator/packages/deck-grader/tests/run-aggregate.mjs, incubator/packages/deck-grader/tests/fixtures/aggregate/
## 합격기준
고품질 픽스처 덱 totalScore ≥ 90, 저품질 픽스처 ≤ 60, hard fail 덱은 점수 무관 반려,
가중치 합 100 검증, 기존 전 테스트 회귀 green.
expectedCommand: cd incubator && node packages/deck-grader/tests/run-aggregate.mjs && node packages/deck-grader/tests/run.mjs
## 금지사항
grader.yaml scoring 섹션·semantic-gate.json·contracts/ 수정 금지. 다른 규칙군 파일 수정 금지.
