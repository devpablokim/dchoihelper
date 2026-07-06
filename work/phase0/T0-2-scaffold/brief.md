# TASK T0-2-scaffold
## 메타
taskType: code / determinismClass: deterministic / mode: attended
baseCommit: 7cb5e9d9b64810cd0f515cc99470e4fd0145401f
schemaVersion: v0.1.0-draft
## 목표
인큐베이션 리포의 packages/ 레이어 경계와 tools/orchestration/ 구조를 확정한다.
완료는 "PLAN.md 3절 리포 분할 맵의 각 리포가 packages/<이름>/ 스텁(package.json + README.md + src/ 또는 scripts/ 빈 디렉토리)으로 존재하고, 구조 린트 스크립트가 green인 상태"다.
## 입력
- /home/seunghyeong/deck-factory/PLAN.md 3절 (리포 분할 맵 — packages 이름 정본)
- /home/seunghyeong/deck-factory/incubator/contracts/ (T0-1 산출 — 이동·수정 금지)
## 산출
allowedWritePaths:
- incubator/packages/<각 패키지>/{package.json,README.md} — PLAN.md 3절의 리포 전부 (deck-contracts는 기존 유지, package.json 정합만)
- incubator/package.json — npm workspaces 루트 (private)
- incubator/tools/orchestration/README.md — T0-8/9/10 산출물이 들어올 위치와 규약 설명
- incubator/tools/lint-structure.mjs — packages/ 구조 린트 (필수 파일 존재, 패키지명 규칙)
## 합격기준
WORKERS.md T0-2 게이트 인용: "구조 린트" green.
expectedCommand: cd incubator && node tools/lint-structure.mjs
## 금지사항
contracts/ 파일 수정 금지. deck-contracts 패키지의 scripts/tests 수정 금지.
외부 npm 의존성 추가 금지 (workspaces 선언만). allowedWritePaths 밖 쓰기 금지.
## 참조
- /home/seunghyeong/deck-factory/PLAN.md 3절
