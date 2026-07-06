# TASK T2-9-copy-reject
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
copy-reject 반려 처리기: copy-reject.json(contracts/copy-reject.schema.json)을 받아
(1) attempt 상한(2회) 검증 — 초과는 스키마 위반으로 거부, (2) 반려 사유를 재작성 지시문으로 변환
(kind별 터미널 규칙 반영: title은 재작성만, body는 분할 허용 등 — contracts의 overflowPolicy 정본),
(3) copy.json에 rejectAttempt 에코 검증. 처리 결과는 reject-directive.json으로 산출.
## 입력
incubator/contracts/{copy-reject.schema.json,copy.schema.json,layout-manifest.schema.json}
## 산출
allowedWritePaths: incubator/packages/deck-copy/src/reject-handler.mjs, incubator/packages/deck-copy/tests/run-reject.mjs, incubator/packages/deck-copy/tests/fixtures-reject/
## 합격기준
attempt 0/1/2/3(위반) 4분기 + kind별 지시문 분기 케이스 전수 green.
expectedCommand: cd incubator && node packages/deck-copy/tests/run-reject.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
