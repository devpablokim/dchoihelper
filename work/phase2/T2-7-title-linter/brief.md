# TASK T2-7-title-linter
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: ddb616c88d0f5d28730e1109e43251ae0309abef
## 목표
deck-copy 액션 타이틀 린터: copy.json(contracts/copy.schema.json)의 슬라이드 제목들에 대해
(1) 결론성 — 명사구 나열이 아닌 주장/결론 문장인지 (한국어 종결·서술 패턴 휴리스틱),
(2) 길이 상한(deck-constants), (3) 제목-본문 중복률, (4) 금지 패턴(개요/현황/소개 같은 무결론 제목)을
검사해 위반 리포트 JSON 산출. node ESM, stdlib만.
## 입력
incubator/contracts/{copy.schema.json,deck-constants.json}, research/consulting-quality.md (액션타이틀·타이틀테스트 절)
## 산출
allowedWritePaths: incubator/packages/deck-copy/src/title-lint.mjs, incubator/packages/deck-copy/tests/run-title-lint.mjs, incubator/packages/deck-copy/tests/corpus-titles/ (양성 10+/음성 10+ synthetic 한국어 코퍼스), incubator/packages/deck-copy/package.json
## 합격기준
WORKERS T2-7 게이트 기계분: 린터 정밀도 코퍼스 — 음성(무결론 제목) 검출률 90%+, 양성 오검출 10% 이하.
expectedCommand: cd incubator && node packages/deck-copy/tests/run-title-lint.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 npm 신규 설치 금지(설치분만). allowedWritePaths 밖 쓰기 금지. 임계값 하드코딩 금지(deck-constants.json 로드).
## 공통 완료 규약
expectedCommand를 직접 실행해 green 확인 후 출력·요약을 result.md에 기록.
