# TASK T2-5-composition-filter
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 7f62805eb8a6ef89d1f4f449ead65ca9a3ec1f68
## 목표
생성 이미지 구도 필터: PNG를 받아 (1) 밝기 분산도 기반 네거티브 스페이스(텍스트 안전 영역) 검출 →
image-manifest의 focalBox/textSafeRegions 필드 산출, (2) 렌더된 글자 혼입 검사(playwright 없이 —
간단한 고대비 텍스트 패턴 휴리스틱 또는 sharp 급 의존 금지이므로 png 픽셀 직접 파싱 stdlib 구현),
(3) 판정 결과 pass/reject + 사유. node ESM, 외부 의존 없이 PNG 디코드는 zlib(stdlib)로 구현.
## 입력
incubator/contracts/image-manifest.schema.json, incubator/packages/deck-charts/poc/vegalite/out/*.png (테스트 소재)
## 산출
allowedWritePaths: incubator/packages/deck-imagery/src/composition-filter.mjs, incubator/packages/deck-imagery/tests/run-filter.mjs, incubator/packages/deck-imagery/tests/fixtures-png/
## 합격기준
텍스트 많은 PNG(차트)와 여백 큰 synthetic PNG의 정분류 + textSafeRegions 산출이 manifest 스키마 통과.
expectedCommand: cd incubator && node packages/deck-imagery/tests/run-filter.mjs
## 공통 금지사항
contracts/ 수정 금지. npm 신규 설치 금지. allowedWritePaths 밖 쓰기 금지. 상수 하드코딩 금지.
## 공통 완료 규약
expectedCommand 직접 실행 green 확인 후 result.md 기록.
