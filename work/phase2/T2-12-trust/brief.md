# TASK T2-12-trust
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
deck-grader 규칙군 2차 중 신뢰성 규칙군: 수치 슬라이드 출처 라인 존재, 댕글링 sourceRef(grade 대상 deck-plan 대조), 출처 표기 형식, 데이터 시점 표기 구현. T1-9와 동일 구조 (src/rules/trust.mjs + rules-trust.yaml 조각).
규칙 선정 근거는 research/consulting-quality.md와 PLAN 5.3에서 도출해 파일 상단 주석에.
## 입력
incubator/packages/deck-grader/src/ (뼈대·기존 규칙군 — 수정 금지, 패턴 참고), incubator/contracts/{deck-constants.json,grade-report.schema.json}
## 산출
allowedWritePaths: incubator/packages/deck-grader/src/rules/trust.mjs, incubator/packages/deck-grader/rules-trust.yaml, incubator/packages/deck-grader/tests/fixtures/trust/, incubator/packages/deck-grader/tests/run-trust.mjs
## 합격기준
규칙별 양성/음성 픽스처 + 골든 리포트 스냅샷, 오검출 0. 기존 테스트(run.mjs, run-typo/color/align) 회귀 green.
expectedCommand: cd incubator && node packages/deck-grader/tests/run-trust.mjs && node packages/deck-grader/tests/run.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
## 추가 금지
grader.yaml·다른 규칙군 파일 수정 금지.
