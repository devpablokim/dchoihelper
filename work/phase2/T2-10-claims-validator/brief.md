# TASK T2-10-claims-validator
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
deck-storyline claims 검증기: source-pack.json과 claims.json(contracts 스키마)에 대해
(1) 스키마 검증, (2) 댕글링 참조 0건 — 모든 claims[].sourceRef가 source-pack에 실존,
(3) 커버리지 검사 — outline의 각 섹션이 참조하는 claims 존재 여부 매트릭스 산출.
synthetic 통합 코퍼스(실제 발표 주제 1건 분량의 source-pack+claims+outline 세트)도 이 태스크가 제작 — T2-17과 P6 테스트가 소비할 정본.
## 입력
incubator/contracts/{source-pack.schema.json,claims.schema.json,input-envelope.schema.json}
## 산출
allowedWritePaths: incubator/packages/deck-storyline/src/claims-validate.mjs, incubator/packages/deck-storyline/tests/, incubator/packages/deck-storyline/corpus/demo-topic-1/ (통합 코퍼스 정본), incubator/packages/deck-storyline/package.json
## 합격기준
댕글링 0건 양성 + 댕글링 주입 음성 케이스 검출 + 커버리지 매트릭스 산출.
expectedCommand: cd incubator && node packages/deck-storyline/tests/run-claims.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
