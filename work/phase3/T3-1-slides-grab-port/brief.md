# TASK T3-1-slides-grab-port (P7 트랙 선두 — 리팩터형: 골든 동결 → 구조)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: d69d2a4465baa283c267c0875429685f356588c1
## 목표
vendor/slides-grab (커밋 핀 클론)의 슬라이드 생성 코어를 incubator/packages/deck-assembler로
이식하는 1단계: (1) 골든 동결 — slides-grab의 대표 입력 1벌로 현재 출력 HTML을 골든으로 고정하는
테스트를 vendor 쪽 실행으로 먼저 작성, (2) 구조 이식 — 코어 모듈(slide-mode.cjs 계열)을
deck-assembler/src/로 복사·ESM화하되 동작 불변 (골든 diff 0), (3) 하드코딩 상수 제거 —
치수·폰트 상수를 incubator/contracts/deck-constants.json 로드로 교체 (기본값이 기존 상수와 동일해
골든이 유지되어야 함).
## 입력
/home/seunghyeong/deck-factory/vendor/slides-grab/ (수정 금지 — 읽기·복사만),
incubator/contracts/{deck-constants.json,slide-html.contract.md},
/home/seunghyeong/deck-factory/research/slides-grab.md (구조 분석 선행 리서치)
## 산출
allowedWritePaths: incubator/packages/deck-assembler/ (src/, tests/, golden/, package.json)
## 합격기준
WORKERS T3-1 게이트: 골든 동결 green 유지 — 이식본 출력과 골든 diff 0 + 상수가 deck-constants
로드 경유임을 확인하는 테스트 + 2회 실행 결정론 해시 일치.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-golden.mjs
## 금지사항
동작 변경 금지 (이 단계는 구조만 — 기능 추가는 T3-2/T3-3 몫). vendor/ 수정 금지. contracts/ 수정 금지.
