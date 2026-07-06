# TASK T1-8-budget-watch
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 45c8f935c1a01849afd58bc301b6a11c4221f662 / schemaVersion: v0.1.0-draft
## 목표
한도/예산 감시기를 구현한다 (WORKERS.md 449~455행 스펙 정본). python3 stdlib만.
기능: (1) wrapper·러너 로그에서 한도 신호(429, "hit your.*limit", 즉사 패턴: 종료 rc!=0 && 소요<10s) 감지, (2) CPU 행 감지(tools/orchestration/watchdog.sh 사상 흡수 — /proc 지피 N분 정지), (3) 감지 시 신규 스폰 중지 신호 파일 + checkpoint.json(진행 중 태스크·attempt 상태) 저장, (4) 재개 명령 문자열 출력.
## 입력
/home/seunghyeong/deck-factory/WORKERS.md T1-8 스펙, incubator/tools/orchestration/{spawn_wrapper.py,watchdog.sh}
## 산출
allowedWritePaths: incubator/tools/orchestration/budget_watch.py, incubator/tools/orchestration/tests/test_budget_watch.py
## 합격기준
WORKERS.md T1-8 합격기준: 모의 429 연발 시나리오에서 신규 스폰 0 + checkpoint.json 산출 + 출력된 재개 명령으로 이어받기 스모크 완주 — 전부 mock 테스트로.
expectedCommand: cd incubator && python3 tools/orchestration/tests/test_budget_watch.py
## 공통 금지사항
contracts/ 수정 금지. 외부 패키지 의존 금지 (node 내장/python3 stdlib만). allowedWritePaths 밖 쓰기 금지.
루트 공유 파일(incubator/package.json 등) 수정 금지 — 필요하면 deps-request.json에 기록만.
임계값·상수 하드코딩 금지: incubator/contracts/deck-constants.json 로드.
## 공통 완료 규약
완료 시 expectedCommand를 직접 실행해 green을 확인하고, 그 출력과 작업 요약을 result.md(-o 회수 파일)에 담아라.
