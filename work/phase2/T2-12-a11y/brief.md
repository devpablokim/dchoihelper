# TASK T2-12-a11y
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
deck-grader 규칙군 2차 중 접근성 규칙군: img alt/SVG title 존재, 명도 대비(이미 있는 color와 중복되지 않는 심화분 — 비텍스트 3:1), 읽기 순서(DOM 순서 vs 시각 순서), 장식 요소 aria 처리 구현. T1-9와 동일 구조 (src/rules/a11y.mjs + rules-a11y.yaml 조각).
규칙 선정 근거는 research/consulting-quality.md와 PLAN 5.3에서 도출해 파일 상단 주석에.
## 입력
incubator/packages/deck-grader/src/ (뼈대·기존 규칙군 — 수정 금지, 패턴 참고), incubator/contracts/{deck-constants.json,grade-report.schema.json}
## 산출
allowedWritePaths: incubator/packages/deck-grader/src/rules/a11y.mjs, incubator/packages/deck-grader/rules-a11y.yaml, incubator/packages/deck-grader/tests/fixtures/a11y/, incubator/packages/deck-grader/tests/run-a11y.mjs
## 합격기준
규칙별 양성/음성 픽스처 + 골든 리포트 스냅샷, 오검출 0. 기존 테스트(run.mjs, run-typo/color/align) 회귀 green.
expectedCommand: cd incubator && node packages/deck-grader/tests/run-a11y.mjs && node packages/deck-grader/tests/run.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
## 추가 금지
grader.yaml·다른 규칙군 파일 수정 금지.
