# RETRY 1 — attempt-0 실패 근거
attempt-0 codex 프로세스가 1시간 32분 경과에 CPU 사용 0초로 완전 정지(행) 상태여서
pgid 스코프 kill로 회수했다 (state/attempt-0.aborted). 산출물 0 (dag_runner.py,
dag.schema.json, 테스트 전부 미생성). 이 시도는 처음부터 다시 수행한다.
결과는 out/attempt-1/result.md 에 작성하라.
# TASK T0-10-dag-runner
## 메타
taskType: code / determinismClass: deterministic / mode: attended
baseCommit: 15e57034c78573f0b03b1d9dcea2451775c3964e
schemaVersion: v0.1.0-draft
## 목표
work/dag.json을 정본으로 소비하는 DAG 태스크 러너를 구현한다. 완료는 "needs 미충족
스폰 거부, consumes 부재 스폰 거부, sharedFiles 겹침 동시 스폰 차단, dynamicChildren
동적 팬아웃, passed/done 마커 재개가 전부 테스트로 입증된 상태"다.
forge stages.json은 직렬 전용이라 신규 구현이되, 게이트 루프·done 마커 사상은 forge에서 계승한다.
## 입력
- /home/seunghyeong/deck-factory/work/dag.json (현행 Phase 0 정본 — 스키마 도출 근거)
- /home/seunghyeong/deck-factory/WORKERS.md 2.3절(dag.json 필드 정본), 6절(상태 전이), T0-10 스펙(382~390행)
- incubator/tools/orchestration/spawn_wrapper.py (T0-9 산출 — 스폰 실행은 이것에 위임)
- incubator/tools/orchestration/vendored/skill_forge_runner.py (게이트 사상 참고)
## 산출
allowedWritePaths:
- incubator/tools/orchestration/dag_runner.py — python3 stdlib만. 기능:
  (a) dag.schema.json으로 dag.json 검증 후 로드, 순환 의존 감지 시 거부
  (b) needs 전 태스크가 integrated(done 마커) 아니면 스폰 거부
  (c) consumes 경로 미존재 시 스폰 거부
  (d) sharedFiles 선언 겹침 태스크 동시 스폰 차단 (실행 중 목록 관리)
  (e) dynamicChildren: 부모 done 후 expand 스크립트 실행 → 자식 tasks.jsonl + dag 항목 병합
  (f) 재개: done(integrated) 태스크 skip, passed.json만 있으면 "미통합" 목록으로 보고
  (g) 실행은 spawn_wrapper.py 호출로 위임 (dry-run 모드 필수 — 스폰 명령 출력만)
- incubator/tools/orchestration/dag.schema.json — WORKERS.md 2.3 필드 정본화
- incubator/tools/orchestration/tests/test_dag_runner.py — WORKERS.md T0-10 합격기준 3케이스:
  needs 미충족 스폰 거부 / 동적 팬아웃(모의 PoC 결과 → 자식 생성) / 중단 후 재실행 시
  integrated 태스크 skip. 추가: 순환 감지, sharedFiles 차단. 전부 mock 커맨드로.
## 합격기준
WORKERS.md T0-10 스펙 인용: "needs 미충족 스폰 거부 케이스 + 동적 팬아웃 케이스 +
중단 후 재실행 시 integrated 태스크 skip 케이스 전부 sonnet 테스트 green".
expectedCommand: cd incubator && python3 tools/orchestration/tests/test_dag_runner.py
## 금지사항
외부 패키지 금지. spawn_wrapper.py·judge_harness.py 수정 금지. work/dag.json 수정 금지.
codex 실호출 금지 (dry-run과 mock으로만 테스트). allowedWritePaths 밖 쓰기 금지.
## 참조
- 오늘 실사례: codex 3기 동시 스폰이 한도로 2기 사망 → 동시 스폰 수 제어와 상태 마커
  기반 회수가 이 러너의 존재 이유다. max-parallel 옵션을 두라.
