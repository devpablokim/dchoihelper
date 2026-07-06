# RETRY 1 — attempt-0 실패 근거
attempt-0은 codex 3기 동시 스폰 중 한도로 프로세스가 도중 사망 (exit 1, result.md 미산출).
잔존물 중 유효분: incubator/tools/orchestration/vendored/ 에 원본 러너 3파일 복사 완료 상태.
이 부분은 재사용하되 체크섬을 직접 검증해 VENDORED.json을 작성하라.
spawn_wrapper.py, tests/test_spawn_wrapper.py, VENDORED.json은 미산출 — 이번 시도에서 작성.
결과는 out/attempt-1/result.md 에 작성하라.
# TASK T0-9-spawn-wrapper

## 메타
taskType: code / determinismClass: deterministic / mode: attended
baseCommit: 65c0b2964e98fefaef1219f8e9f2e5ffcaf76080
schemaVersion: v0.1.0-draft

## 목표
codex-spawn 러너의 attempt-분리 wrapper를 구현하고 원본 러너를 vendoring한다.
완료는 "wrapper가 attempt별 출력 경로를 분리하고, skip 판정을 out 존재가 아니라
passed 마커로 하며, preflight 쓰기 검증과 pgid 스코프 kill이 테스트로 입증된 상태"다.

## 입력
- /home/seunghyeong/.claude/skills/codex-spawn/ 디렉토리 전체 (원본 러너와 규약 — 정독)
- /home/seunghyeong/behavior-skill-analysis/drafts/doc-readability-linter/forge/skill_forge_runner.py
- /home/seunghyeong/deck-factory/WORKERS.md 1.1절, 6절, T0-9 스펙 (373~380행)

## 산출
allowedWritePaths:
- incubator/tools/orchestration/vendored/ — 원본 러너 사본 (codex-spawn 러너 스크립트,
  skill_forge_runner.py)
- incubator/tools/orchestration/VENDORED.json — 원본 경로·버전·sha256 체크섬·복사 시각
- incubator/tools/orchestration/spawn_wrapper.py — python3 stdlib만. 기능:
  (a) 태스크 정의(tasks.jsonl 항목)를 받아 work/<phase>/<task-id>/out/attempt-N/ 경로 생성
      (N = 기존 attempt 최대값+1, 덮어쓰기 금지)
  (b) skip 판정: state/attempt-N.passed 존재 시에만 skip. out/ 파일 존재는 skip 근거 아님
  (c) 전 경로 절대화 (cwd, brief, out, schema)
  (d) preflight: out 디렉토리에 실제 파일 생성·삭제로 쓰기 검증, 실패 시 스폰 0건
  (e) setsid로 process group 생성, pgid를 logs/pgid에 기록
  (f) kill 서브커맨드: 기록된 pgid에만 신호 전달, 진행 중이던 out을 state/attempt-N.aborted로 마킹
- incubator/tools/orchestration/tests/test_spawn_wrapper.py — WORKERS.md T0-9 합격기준
  3케이스: 실패 attempt 뒤 재실행 시 skip되지 않음 / preflight 실패 시 스폰 0건 /
  kill이 기록된 pgid에만 전달 (mock 프로세스로)

## 합격기준
WORKERS.md T0-9 스펙 인용: "실패 attempt 뒤 재실행 시 skip되지 않음(sonnet 테스트) +
preflight 실패 시 스폰 0건 + kill이 기록된 pgid에만 전달되는 스코프 테스트".
expectedCommand: cd incubator && python3 tools/orchestration/tests/test_spawn_wrapper.py

## 금지사항
외부 패키지 금지 (python3 stdlib만). judge_harness.py 수정 금지.
원본 러너(홈 디렉토리) 수정 금지 — 읽기와 복사만. allowedWritePaths 밖 쓰기 금지.
codex 실호출 금지 — 스폰 대상은 테스트에서 mock 커맨드로.

## 참조
- /home/seunghyeong/deck-factory/WORKERS.md 7절 (실패 회수 절차 — aborted 마킹 규약)
