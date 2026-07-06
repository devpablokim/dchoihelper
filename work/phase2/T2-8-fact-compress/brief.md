# TASK T2-8-fact-compress
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
deck-copy 압축 검증 도구: (1) 6x6 계산기 — 슬라이드당 불릿 수·불릿당 어절 수 상한 검사,
(2) 발화시간 계산기 — 한국어 음절 기반 발표 소요 추정(분당 음절 상수는 deck-constants에 추가 요청 말고 인자 기본값+meta 기록),
(3) 압축 팩트 보존 검사 — copy.json의 각 주장 텍스트가 claims(sourceRef) 참조를 유지하는지, 수치가 claims 원문 수치와 일치하는지 기계 대조.
## 입력
incubator/contracts/{copy.schema.json,claims.schema.json,deck-constants.json}
## 산출
allowedWritePaths: incubator/packages/deck-copy/src/{six-by-six.mjs,speech-time.mjs,fact-guard.mjs}, incubator/packages/deck-copy/tests/run-fact-compress.mjs, incubator/packages/deck-copy/tests/fixtures-fact/
## 합격기준
위반/정상 픽스처 전수 정분류 + 수치 불일치 케이스 검출 + 댕글링 sourceRef 검출.
expectedCommand: cd incubator && node packages/deck-copy/tests/run-fact-compress.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
