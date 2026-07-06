# TASK T1-4-capacity
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 45c8f935c1a01849afd58bc301b6a11c4221f662 / schemaVersion: v0.1.0-draft
## 목표
capacity 역산 스크립트를 구현한다: deck-constants.json(canvas·fontFloors·capacityMargin·폰트 메트릭 상수)을 로드해, 슬롯 bbox{w,h}와 폰트 크기를 입력으로 수용 가능한 문자 수·줄 수 추정 테이블을 산출한다. plan 단계 결정론 추정의 정본이다 (PLAN.md P7 책임 분리 — 실측은 compose 몫이므로 여기서 렌더 금지).
## 입력
/home/seunghyeong/deck-factory/incubator/contracts/deck-constants.json, /home/seunghyeong/deck-factory/PLAN.md P2절(438~484행)과 P7의 추정/실측 책임 분리 서술
## 산출
allowedWritePaths: incubator/packages/deck-layouts/scripts/capacity.mjs, incubator/packages/deck-layouts/tests/, incubator/packages/deck-layouts/package.json
필요한 폰트 메트릭 상수가 deck-constants.json에 없으면 하드코딩하지 말고 NOTES.md에 "constants 추가 요청"으로 기록 후 임시 파라미터 인자로 받아라.
## 합격기준
WORKERS.md T1-4 게이트: 실측 역산 출력 재현 해시 (deterministic) — 같은 입력 2회 실행 sha256 일치 + 알려진 케이스 검증.
expectedCommand: cd incubator/packages/deck-layouts && node tests/run.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 패키지 의존 금지 (node 내장/python3 stdlib만). allowedWritePaths 밖 쓰기 금지.
루트 공유 파일(incubator/package.json 등) 수정 금지 — 필요하면 deps-request.json에 기록만.
임계값·상수 하드코딩 금지: incubator/contracts/deck-constants.json 로드.
## 공통 완료 규약
완료 시 expectedCommand를 직접 실행해 green을 확인하고, 그 출력과 작업 요약을 result.md(-o 회수 파일)에 담아라.
