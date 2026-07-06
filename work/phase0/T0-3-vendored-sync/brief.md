# TASK T0-3-vendored-sync

## 메타
taskType: code / determinismClass: deterministic / mode: attended
baseCommit: 65c0b2964e98fefaef1219f8e9f2e5ffcaf76080
schemaVersion: v0.1.0-draft

## 목표
독립 리포 승격 후 각 리포가 deck-contracts 스키마 사본을 버전 태그 핀으로 가져오는
vendored sync 방식을 구현한다. 완료는 "sync 스크립트가 지정 태그의 contracts/를
대상 디렉토리로 복사하고, diff 검사가 사본-원본 불일치를 exit 1로 잡는 왕복이
데모로 동작하는 상태"다 (PLAN.md Phase 0: 이 방식이 동작하는 것까지가 완료 조건).

## 입력
- /home/seunghyeong/deck-factory/incubator/contracts/ (원본)
- /home/seunghyeong/deck-factory/PLAN.md 3절 (vendored 스키마 diff CI 요구)

## 산출
allowedWritePaths:
- incubator/tools/sync-contracts.mjs — 인자: --tag <git태그|커밋> --dest <디렉토리>.
  git archive 또는 git show로 해당 시점 contracts/를 dest로 복사, 복사 기록
  (태그·해시·시각)을 dest/SYNC-PIN.json에 기록.
- incubator/tools/diff-contracts.mjs — SYNC-PIN.json의 핀과 현재 사본을 대조,
  불일치 파일 목록 출력 + exit 1.
- incubator/.github/workflows/contracts-diff.yml — 위 diff를 도는 CI 워크플로 골격.
- incubator/tools/tests/test-sync.sh — 왕복 데모: sync → diff green → 사본 1바이트 변조
  → diff가 exit 1 → 원복. bash, set -e.

## 합격기준
WORKERS.md T0-3 게이트 인용: "sync 왕복 동작 + diff 검사 green".
expectedCommand: cd incubator && bash tools/tests/test-sync.sh

## 금지사항
contracts/ 원본 수정 금지. 외부 npm 의존 금지 (node 내장 + git CLI만).
allowedWritePaths 밖 쓰기 금지.

## 참조
- /home/seunghyeong/deck-factory/WORKERS.md 0절 (vendoring 원칙)
