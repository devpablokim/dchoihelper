# TASK T1-1-validators
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 45c8f935c1a01849afd58bc301b6a11c4221f662 / schemaVersion: v0.1.0-draft
## 목표
deck-tokens 패키지에 토큰 검증기 2종을 구현한다: (1) tokens.json이 contracts/tokens.schema.json을 만족하는지 검증, (2) WCAG 2.1 상대휘도 기반 대비율 계산기 + 토큰 색상쌍(본문/배경, 강조/배경 등 스키마의 페어 정의) 전수 대비 검사.
## 입력
/home/seunghyeong/deck-factory/incubator/contracts/tokens.schema.json, /home/seunghyeong/deck-factory/PLAN.md P1절(395~437행), incubator/packages/deck-contracts/scripts/validate.mjs(스키마 검증 재사용 가능)
## 산출
allowedWritePaths: incubator/packages/deck-tokens/scripts/{validate-tokens.mjs,contrast.mjs}, incubator/packages/deck-tokens/tests/, incubator/packages/deck-tokens/package.json
## 합격기준
WORKERS.md T1-1 게이트: 골든 대비 계산 테스트 — 알려진 색상쌍 기대값(흑/백 21:1, 동일색 1:1 포함 6쌍 이상, 오차 0.01) + 스키마 검증 valid/invalid 케이스.
expectedCommand: cd incubator/packages/deck-tokens && node tests/run.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 패키지 의존 금지 (node 내장/python3 stdlib만). allowedWritePaths 밖 쓰기 금지.
루트 공유 파일(incubator/package.json 등) 수정 금지 — 필요하면 deps-request.json에 기록만.
임계값·상수 하드코딩 금지: incubator/contracts/deck-constants.json 로드.
## 공통 완료 규약
완료 시 expectedCommand를 직접 실행해 green을 확인하고, 그 출력과 작업 요약을 result.md(-o 회수 파일)에 담아라.
