# TASK T0-1-contracts-v1

## 메타
taskType: code
determinismClass: deterministic
mode: attended
baseCommit: 59b29e93bf3231af44fc299a57ac88acd21a6e5f
schemaVersion: v0.1.0-draft (이 태스크가 생성하는 버전)

## 목표
PLAN.md 2.3절(파일 핸드오프 계약)에 산문으로 확정된 계약 전부를
기계 검증 가능한 JSON Schema(draft 2020-12) 파일 + 검증 스크립트 + 테스트로 전사한다.
완료는 "2.3절의 모든 계약이 스키마 파일로 존재하고, validate.mjs가 골든 샘플을 전부 통과시키고
위반 샘플을 전부 거부하는 상태"다. v1은 초안 동결이다 — 필드 추가는 가능하되
이 태스크 산출 필드의 이름 변경·삭제는 이후 스키마 변경 절차를 따른다.

## 입력
- /home/seunghyeong/deck-factory/PLAN.md 의 2.3절 (156행~343행) — 계약 정본. 반드시 정독.
- /home/seunghyeong/deck-factory/PLAN.md 의 1.2절 (물리 스펙 상수의 출처)

## 산출
allowedWritePaths:
- incubator/contracts/*.schema.json — 최소: deck-plan, deck-manifest, copy, copy-reject,
  chart-request, chart-manifest, image-manifest, image-reject, layout-manifest,
  measured-overflow, edit-manifest, 공통 입력 envelope. 2.3절에 있는데 이 목록에 없는 계약도 빠짐없이.
- incubator/contracts/deck-constants.json — 2.3절의 상수 단일 소스 (canvas, 좌표 매핑, fontFloors, capacityMargin)
- incubator/contracts/slide-html.contract.md — 슬라이드 HTML DOM 규약 (스키마로 표현 불가한 부분은 산문+검증 스크립트)
- incubator/packages/deck-contracts/scripts/validate.mjs — 파일경로+계약명을 받아 검증, exit code로 판정
- incubator/packages/deck-contracts/scripts/validate-slide-html.mjs — slide-html 계약 검증
- incubator/packages/deck-contracts/tests/ — 계약별 골든 샘플(valid) 1개 + 위반 샘플(invalid) 2개 이상과 테스트 러너
- incubator/packages/deck-contracts/package.json

## 합격기준
PLAN.md Phase 0 완료 정의 인용: "스키마 CI green(동기화 방식 포함)" 중 이 태스크 몫 —
모든 계약 스키마 존재 + 검증 스크립트가 골든/위반 샘플을 정확히 분류.
2.3절의 계약 필드(releaseBlocked, rejectCount/attempt, exportStatus/reviewRequired,
sourceRef, focalBox/textSafeRegions, splitGranularity/allowLossyTruncate, determinism 관련)가
스키마에 누락 없이 반영될 것.
expectedCommand: cd incubator/packages/deck-contracts && node tests/run.mjs (전부 pass, 의존성은 node 표준 모듈만 — ajv 등 외부 패키지 금지, 스키마 검증기는 직접 최소 구현 또는 node 내장만)

## 금지사항
공통: 계약 필드명을 PLAN.md 2.3과 다르게 변경 금지, 폰트 축소 로직 도입 금지,
allowedWritePaths 밖 쓰기 금지, 상수 하드코딩 금지(deck-constants.json에서만).
forbiddenSharedFiles: incubator/package.json 루트 파일은 이 태스크에서 만들지 않는다 (T0-2 몫).
2.3절에 없는 계약을 발명하지 말 것 — 부족하면 NOTES.md에 기록만.

## 참조
- /home/seunghyeong/deck-factory/PLAN.md 2.3절 (정본)
- /home/seunghyeong/deck-factory/research/skill-architecture.md (스키마 vendoring 관행)
