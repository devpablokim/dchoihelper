# TASK T2-6-overlay-post
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 7f62805eb8a6ef89d1f4f449ead65ca9a3ec1f68
## 목표
오버레이 후처리기: 배경 이미지 위 텍스트 배치 시 (1) textSafeRegions와 슬롯 bbox 교차 검증,
(2) 오버레이(스크림/그라디언트) CSS 생성 — 이미지 위 텍스트 대비 4.5:1(본문)/3:1(대형) 보장 계산
(이미지 해당 영역 평균 휘도 기반), (3) 산출: overlay-spec.json {slotId, scrim, computedContrast}.
이미지 픽셀 위 글자 합성 금지 — HTML 레이어 텍스트 전제의 CSS 스펙만 산출.
## 입력
incubator/contracts/{image-manifest.schema.json,deck-constants.json}, incubator/packages/deck-tokens/scripts/contrast.mjs (재사용)
## 산출
allowedWritePaths: incubator/packages/deck-imagery/src/overlay-post.mjs, incubator/packages/deck-imagery/tests/run-overlay.mjs, incubator/packages/deck-imagery/tests/fixtures-overlay/
## 합격기준
어두운/밝은/중간 배경 3케이스에서 computedContrast가 기준 충족 + 교차 검증 음성 케이스.
expectedCommand: cd incubator && node packages/deck-imagery/tests/run-overlay.mjs
## 공통 금지사항
contracts/ 수정 금지. npm 신규 설치 금지. allowedWritePaths 밖 쓰기 금지. 상수 하드코딩 금지.
## 공통 완료 규약
expectedCommand 직접 실행 green 확인 후 result.md 기록.
