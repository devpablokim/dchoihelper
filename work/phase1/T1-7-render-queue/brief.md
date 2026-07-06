# TASK T1-7-render-queue
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 45c8f935c1a01849afd58bc301b6a11c4221f662 / schemaVersion: v0.1.0-draft
## 목표
비LLM 렌더 잡 큐를 구현한다 (WORKERS.md 441~447행 스펙 정본). 입력: 렌더 잡 jsonl {id, cmd, cwd, artifacts[], semaphoreClass(gpu|cpu), retries}. python3 stdlib만, LLM 호출 0.
## 입력
/home/seunghyeong/deck-factory/WORKERS.md T1-7 스펙, incubator/tools/orchestration/spawn_wrapper.py(pgid·상태 마커 사상 참고)
## 산출
allowedWritePaths: incubator/tools/orchestration/render_queue.py, incubator/tools/orchestration/tests/test_render_queue.py
기능: 세마포어 상한(gpu 4~6, cpu 설정값), 실패 자동 재시도 1회, artifact 존재 검증 + sha256 기록, 동시 실행 수 로그.
## 합격기준
WORKERS.md T1-7 합격기준: 더미 잡 매트릭스(sleep 기반 mock)에서 동시 실행 수가 세마포어 상한을 넘지 않음(로그 검증) + 재시도 케이스 + artifact 부재 시 fail 보고 — 전부 테스트로.
expectedCommand: cd incubator && python3 tools/orchestration/tests/test_render_queue.py
## 공통 금지사항
contracts/ 수정 금지. 외부 패키지 의존 금지 (node 내장/python3 stdlib만). allowedWritePaths 밖 쓰기 금지.
루트 공유 파일(incubator/package.json 등) 수정 금지 — 필요하면 deps-request.json에 기록만.
임계값·상수 하드코딩 금지: incubator/contracts/deck-constants.json 로드.
## 공통 완료 규약
완료 시 expectedCommand를 직접 실행해 green을 확인하고, 그 출력과 작업 요약을 result.md(-o 회수 파일)에 담아라.
