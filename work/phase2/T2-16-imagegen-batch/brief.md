# TASK T2-16-imagegen-batch (P5 생성 실행 스모크)
## 메타
taskType: render / determinismClass: nondeterministic / mode: attended / baseCommit: d67fa8b745a5da21e4b00df63a2ad7ae3e2b9283
## 목표
P5 파이프라인 실사격 스모크: (1) incubator/packages/deck-imagery/tests/briefs/ 의 브리프 중
슬라이드 배경용 2건을 골라 prompt-compile.mjs로 프롬프트 컴파일, (2) 각 프롬프트를 너의
$imagegen 도구로 실제 생성 (2건 x 2변형 = 4장, 16:9), (3) PNG를
incubator/packages/deck-imagery/smoke/out/ 에 저장하고 manifest(생성 프롬프트·파일 경로) 기록.
## 산출
allowedWritePaths: incubator/packages/deck-imagery/smoke/ (프롬프트 jsonl, out/*.png, manifest.json)
## 합격기준
PNG 4장 실존 + manifest 완비. 구도 필터·수율 판정은 fable 후속.
expectedCommand: ls incubator/packages/deck-imagery/smoke/out/*.png | wc -l  (4 이상)
## 금지사항
이미지 위 글자 합성 금지 (배경용 — 프롬프트에 텍스트 금지 지시 유지). 다른 디렉토리 쓰기 금지.
