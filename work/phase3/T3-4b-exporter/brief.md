# TASK T3-4b-exporter
## 메타
taskType: code / determinismClass: canonicalized / mode: attended / baseCommit: 7016949b46d45c30d4232683edc850454eda8d8a
## 목표
Playwright 익스포터: 덱을 (1) PNG (슬라이드별 1280x720, pw-libs 부트스트랩·Pretendard 정본 렌더 —
deck-layouts overflow-check의 방식 재사용), (2) PDF (PNG 병합 또는 chromium print), (3) PPTX —
새 npm 금지이므로 최소 OOXML: 슬라이드별 PNG를 풀블리드 이미지로 넣은 pptx를 node zlib로 zip 조립.
draft 격리 규약: deck-manifest exportStatus=final만 exports/final/, draft는 exports/draft/ + -draft 접미사,
releaseBlocked 덱은 final 거부 (계약 정본).
## 입력
incubator/packages/deck-assembler/, incubator/contracts/deck-manifest.schema.json, incubator/packages/deck-layouts/scripts/overflow-check.mjs (렌더 방식 참고)
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/export/, incubator/packages/deck-assembler/tests/run-export.mjs
## 합격기준
WORKERS T3-4 게이트: 3포맷 스모크(golden-compose 덱 → png n장+pdf 1+pptx 1 실존, pptx는 unzip 구조 검증)
+ final/draft 격리 케이스 + releaseBlocked final 거부 케이스.
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-export.mjs
## 금지사항
새 npm 금지. viewer 파일 접근 금지. 슬라이드 HTML 수정 금지.
