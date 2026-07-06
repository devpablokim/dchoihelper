# TASK T0-4-grader-skeleton

## 메타
taskType: code / determinismClass: deterministic / mode: attended
baseCommit: 65c0b2964e98fefaef1219f8e9f2e5ffcaf76080
schemaVersion: v0.1.0-draft

## 목표
deck-grader의 뼈대를 구현한다 — 슬라이드 HTML 파서 + 기계검사 hard fail 6종 +
grader.yaml 골격 + deck-constants sync. 완료는 "샘플 HTML 덱(합격 1벌·위반 1벌)에
대해 grade-report를 산출하고, 위반 덱에서 해당 hard fail이 정확히 검출되는 상태"다.
종합점수 산출은 이 태스크 범위가 아니다 (PLAN.md Phase 0 완료 정의).

## 입력
- /home/seunghyeong/deck-factory/PLAN.md 5.3절 — hard fail 목록 정본. 의미론 3항목
  (액션타이틀·MECE·원메시지)은 제외하고, 기계검사 가능한 hard fail 6종을 선별해
  구현하라 (본문 폰트 하한(configured body floor) 미달, 수치 슬라이드 출처 라인 부재,
  명도 대비 미달, 오버플로 등 — 5.3 원문에서 6종을 확정하고 선정 근거를 README에 기록).
- incubator/contracts/slide-html.contract.md (파싱 대상 DOM 규약)
- incubator/contracts/deck-constants.json (임계값 단일 소스 — 하드코딩 금지)
- incubator/contracts/grade-report.schema.json (출력 계약)

## 산출
allowedWritePaths:
- incubator/packages/deck-grader/src/ — 파서(정규식/최소 DOM 파싱, 외부 패키지 금지)
  + hard fail 검사 6종 + 리포트 생성기 (node, ESM)
- incubator/packages/deck-grader/grader.yaml — 골격: 치수·하한 섹션은 constants sync로
  생성됨을 주석 명시, 규칙군 자리(타이포/컬러/정렬/데이터/신뢰성/접근성)는 빈 골격
- incubator/packages/deck-grader/scripts/sync-constants.mjs — deck-constants.json →
  grader.yaml 치수 섹션 생성
- incubator/packages/deck-grader/tests/ — 샘플 합격 덱 HTML 1벌 + 위반 덱 HTML 1벌
  (hard fail 6종이 각각 1회 이상 발동하도록 구성) + 테스트 러너
- incubator/packages/deck-grader/README.md — hard fail 6종 선정 근거
- incubator/packages/deck-grader/package.json 갱신

## 합격기준
WORKERS.md T0-4 게이트 인용: "샘플 HTML 덱에 리포트 산출".
추가: 위반 덱에서 6종 각각 검출 + 합격 덱에서 오검출 0 + 리포트가
grade-report.schema.json 검증 통과 (deck-contracts의 validate.mjs 사용).
expectedCommand: cd incubator/packages/deck-grader && node tests/run.mjs

## 금지사항
임계값 하드코딩 금지 (deck-constants.json 로드). 폰트 축소 로직 도입 금지.
contracts/ 수정 금지. 외부 npm 의존 금지. 종합점수/가중치 구현 금지 (Phase 2 몫).
allowedWritePaths 밖 쓰기 금지.

## 참조
- /home/seunghyeong/deck-factory/PLAN.md P8절 (grader 전체 그림 — 이번엔 뼈대만)
