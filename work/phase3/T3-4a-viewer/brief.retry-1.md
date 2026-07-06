# RETRY 1 — attempt-0 게이트 실패 근거
fable 재실행에서 실패: "folder bundle font size must not be rewritten by viewport resize, expected 64px".
뷰포트 리사이즈 시 폰트 크기가 변한다 — transform scale 불변식 위반 (폰트 축소 금지, PLAN 1.2).
원인 추정: 뷰어가 scale을 transform이 아니라 font-size/zoom 재계산으로 구현했거나,
computed font-size를 검사하는 테스트와 실제 구현이 어긋남.
수정 지시: 스케일링은 컨테이너의 CSS transform: scale()로만 — 슬라이드 내부 요소의
computed font-size는 어떤 창 크기에서도 원본 값(px) 유지. 테스트 기준을 완화하지 말 것.
수정 후 run-viewer.mjs 2회 연속 green, out/attempt-1/result.md 기록.
# TASK T3-4a-viewer
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 7016949b46d45c30d4232683edc850454eda8d8a
## 목표
덱 뷰어: slides/*.html 덱을 여는 viewer.html — (1) folder bundle 모드(slides/ 병치 로드)와
single-html inline bundle 모드(전 슬라이드 인라인 병합 산출 스크립트) 2종 (PLAN 1.2 분리 규약),
(2) 키보드 내비게이션·슬라이드 번호, (3) transform scale로 창 크기 무관 16:9 유지 (폰트 축소 아님),
(4) exportStatus=draft 덱은 draft 워터마크 오버레이 표시 (deck-manifest 소비).
## 입력
incubator/packages/deck-assembler/tests/golden-compose/ (소재), incubator/contracts/deck-manifest.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-assembler/src/viewer/, incubator/packages/deck-assembler/tests/run-viewer.mjs
## 합격기준
WORKERS T3-4 게이트 중 뷰어분: 두 모드 산출 green + draft 워터마크 케이스 + playwright 로드 스모크(콘솔 에러 0).
expectedCommand: cd incubator && node packages/deck-assembler/tests/run-viewer.mjs
## 금지사항
슬라이드 HTML 수정 금지 (소비만). 외부 리소스 참조 금지 (자체 완결). exporter 파일 접근 금지.
