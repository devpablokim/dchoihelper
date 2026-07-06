# TASK T4-4b-unattended-contract (라우터 계약 위반 수정)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: edf408a1bca88576c00d650743fc49c09e25f596
## 실측 결함
실사격에서 compose 단계가 "compose overflow remained after measured roundtrip" RouterError로 중단됨
(s1 title/subtitle 오버플로가 재왕복 1회 후 잔존). 그러나 계약(PLAN P7 + 5.3 unattended 규약) 정본은:
재왕복 상한 도달 → 해당 슬라이드 releaseBlocked=true + needsHumanReview=true →
deck-manifest exportStatus=draft 집계 → unattended 모드에서는 중단이 아니라
draft 익스포트 완료 후 review-required 종료(exit 2). attended 모드에서만 사람 에스컬레이션 중단이 맞다.
## 목표
packages/deck-factory/src/router.mjs 의 compose 단계 오버플로 잔존 처리를 계약에 맞게 수정:
(1) unattended — releaseBlocked 마킹 경로로 계속 진행(문제 슬라이드 draft 격리), 나머지 정상 슬라이드 포함
draft 익스포트 산출, exit 2 + 결과 JSON에 reviewRequired 사유 목록,
(2) attended — 현행대로 명시적 실패 (단 에러 메시지에 어느 슬라이드·슬롯·측정값인지 포함),
(3) 기존 mock E2E 테스트에 unattended 오버플로 잔존 케이스 추가 (고의 초과 콘텐츠 픽스처).
## 입력
incubator/packages/deck-factory/, incubator/contracts/{deck-plan.schema.json,deck-manifest.schema.json,measured-overflow.schema.json}, /home/seunghyeong/deck-factory/PLAN.md P7절(추정/실측 이음매)과 5.3 unattended 서술
## 산출
allowedWritePaths: incubator/packages/deck-factory/src/router.mjs, incubator/packages/deck-factory/tests/
## 합격기준
신규 unattended 오버플로 잔존 케이스: exit 2 + exports/draft/ 산출 + deck-manifest
releaseBlocked/reviewRequired 필드 정합. 기존 run-router-e2e 전 케이스 회귀 green.
expectedCommand: cd incubator && node packages/deck-factory/tests/run-router-e2e.mjs
## 금지사항
contracts/·다른 패키지 수정 금지. 게이트 완화 금지 (오버플로 판정 자체는 그대로 — 처리 경로만 계약화).
