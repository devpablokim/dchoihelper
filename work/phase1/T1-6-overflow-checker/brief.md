# TASK T1-6-overflow-checker
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 4ec14e2a83e94cff48c4d422c9377e70204950eb / schemaVersion: v0.1.0-draft
## 목표
레이아웃 검증 공용 도구 2종을 구현한다.
(a) 오버플로 검사기: 슬라이드 HTML 파일을 Playwright chromium으로 1280x720 뷰포트 렌더해
data-slot-id 요소별 콘텐츠 오버플로(scrollHeight>clientHeight 또는 scrollWidth 초과)와
슬롯 bbox 이탈, 본문 계열 슬롯의 계산된 font-size가 deck-constants.json fontFloors 미만인지 검출해
JSON 리포트를 낸다. 단일 파일 검사 CLI + 여러 파일 배치를 render_queue.py 잡 jsonl로 생성하는 모드.
(b) capacityFloors 산출기: 극단 콘텐츠 매트릭스(짧은/중간/최장 텍스트)를 더미 템플릿 슬롯에 주입 렌더해
실측 수용 한계를 구하고 capacity.mjs(T1-4) 추정과 대조표를 산출한다.
## 입력
incubator/contracts/{slide-html.contract.md,deck-constants.json,layout-manifest.schema.json},
incubator/packages/deck-layouts/scripts/capacity.mjs, incubator/tools/orchestration/render_queue.py
Playwright는 incubator/node_modules에 설치돼 있다 (chromium 포함, v1.61) — require('playwright') 가능.
## 산출
allowedWritePaths: incubator/packages/deck-layouts/scripts/{overflow-check.mjs,capacity-floors.mjs},
incubator/packages/deck-layouts/tests/run-overflow.mjs, incubator/packages/deck-layouts/tests/fixtures-overflow/
## 합격기준
WORKERS.md T1-6 게이트: 극단 콘텐츠 매트릭스 렌더 스냅샷 —
오버플로 있는 픽스처에서 검출 1+, 정상 픽스처 오검출 0, 폰트 하한 위반 픽스처 검출, 리포트 JSON 구조 안정(스냅샷 일치).
expectedCommand: cd incubator && node packages/deck-layouts/tests/run-overflow.mjs
## 금지사항
contracts/ 수정 금지. playwright 외 신규 npm 의존 금지. capacity.mjs 수정 금지.
폰트 자동 축소 로직 금지 (검출만, 해소는 다른 레이어 몫). allowedWritePaths 밖 쓰기 금지.
