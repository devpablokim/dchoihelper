# TASK T2-11-titles-prelint
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
titles-test 사전 린트: outline(스토리라인 단계 산출)의 섹션 제목 시퀀스만 이어 읽었을 때
스토리가 성립하는지의 기계 검사 가능분 — (1) 제목 시퀀스 추출기, (2) 중복/순환 감지,
(3) 논리 연결어 부재 등 휴리스틱 경고, (4) opus 판정용 판정 패키지(제목 시퀀스 텍스트) 생성기.
## 입력
incubator/contracts/input-envelope.schema.json, incubator/packages/deck-storyline/ (T2-10과 같은 패키지 — src/titles-prelint.mjs로 파일 분리, T2-10 파일 수정 금지)
## 산출
allowedWritePaths: incubator/packages/deck-storyline/src/titles-prelint.mjs, incubator/packages/deck-storyline/tests/run-titles.mjs, incubator/packages/deck-storyline/tests/fixtures-titles/
## 합격기준
정상/결함 outline 픽스처 정분류 + 판정 패키지 생성 green.
expectedCommand: cd incubator && node packages/deck-storyline/tests/run-titles.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
