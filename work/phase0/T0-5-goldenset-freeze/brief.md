# TASK T0-5-goldenset-freeze

## 메타
taskType: judgment
determinismClass: nondeterministic
mode: attended
baseCommit: 59b29e93bf3231af44fc299a57ac88acd21a6e5f
schemaVersion: n/a (계약 소비 없음)

## 목표
deck-grader 캘리브레이션과 Phase 5 판정자 검증이 매달릴 "레퍼런스 골든셋"의
출처·포함기준을 확정하고 동결 문서를 작성한다. 이 단계에서는 기준 확정만 하고
HTML 리빌드 등 무거운 조달은 하지 않는다 (PLAN.md Phase 0 — 조달은 Phase 5 준비로 이연).
완료는 "동결 문서가 존재하고, 이후 골든셋 구성원 추가·제외가 이 문서의 기준으로만
정당화되는 상태"다.

## 입력
- /home/seunghyeong/deck-factory/PLAN.md 의 P8(deck-grader) 절과 Phase 0/5 로드맵
- /home/seunghyeong/deck-factory/research/consulting-quality.md (채점 기준 후보 31종)
- /home/seunghyeong/deck-factory/research/deck-frameworks.md (상용 제품 벤치마크)

## 산출
allowedWritePaths:
- incubator/docs/goldenset-freeze.md — 필수 내용:
  (1) 골든셋의 목적 2종 구분 — grader 캘리브레이션용 vs 판정자(opus) 사전검증용
  (2) 출처 카테고리와 각각의 포함/제외 기준 (공개 IR/컨퍼런스 덱, 상용 AI 제품 산출물,
      synthetic HTML 골든셋, 자체 생성 덱 — 각각 라이선스·재배포 가능성 주의 명시)
  (3) 우수/열위 쌍 구성 기준 (판정자 변별력 검증용 — 무엇이 "명백히 우수/열위"인가의 조작적 정의)
  (4) 최소 수량과 커버리지 (슬라이드 role별: 커버/본문/차트/빅스탯/클로징)
  (5) 동결 규칙 — 추가·제외 절차와 기록 위치
  (6) Phase 2 1단계 캘리브레이션(synthetic+자체 덱)과 Phase 5 2단계(공개 덱 리빌드)의
      각 단계가 이 셋에서 무엇을 쓰는지 매핑

## 합격기준
PLAN.md Phase 0 완료 정의 인용: "골든셋 동결 문서 존재" —
단, 존재만으로는 부족하고 위 6개 항목이 전부 채워져 있어야 하며,
각 기준이 "제3자가 같은 기준으로 같은 판단을 내릴 수 있는" 수준으로 조작적이어야 한다.
expectedCommand: 없음 (judgment 태스크 — fable이 6항목 완비를 확인)

## 금지사항
HTML 리빌드·스크레이핑·대량 다운로드 금지 (Phase 5 이연).
"검증 완료" 류 공허한 단정 금지. 이모지·볼드(**) 금지.
allowedWritePaths 밖 쓰기 금지.

## 참조
- /home/seunghyeong/deck-factory/PLAN.md 5.4절 (판정자 사전 검증 임계값)
