# RETRY 1 — attempt-0 부분 실패 근거 (mermaid만)
공용 글리프 검사 이식 후 vegalite/echarts/graphviz는 2회 연속 green.
mermaid만 "browser.newPage: Target page, context or browser has been closed"로 일관 실패 —
한글 판정 단계에 도달조차 못 한다. mermaid는 렌더 자체가 chromium을 쓰는 유일한 엔진이라
브라우저를 2회(렌더+검사) 띄우는 경로가 의심된다.

수정 지시 (mermaid PoC만, 다른 3엔진 코드·공용 lib의 동작 변경 금지):
(1) 먼저 원인을 실측하라 — mermaid render-poc.mjs에 launch 에러 전문 로깅을 넣고 1회 실행해
    실제 실패 지점(launch인지 newPage인지, 어떤 executable인지)을 확인.
(2) 유력 수정 방향: 렌더와 글리프 검사를 브라우저 1회 기동으로 통합 (같은 browser 인스턴스에서
    mermaid.render 페이지와 검사 페이지를 순차 사용, 종료는 마지막 한 번).
(3) headless shell이 mermaid 렌더에 부족하면 chromium full(playwright chromium 채널)로
    launch하되 chromiumSandbox:false 유지. pw-libs 부트스트랩은 공용 lib 그대로.
수정 후 mermaid expectedCommand 2회 연속 green + 다른 3엔진 각 1회 회귀 green 확인,
out/attempt-1/result.md에 원인 실측 결과와 함께 기록.
# TASK T2-1f-glyphcheck-unify (T2-1 재분해 — 글리프 검사 하네스 통일)
## 메타
taskType: code / determinismClass: canonicalized / mode: attended / baseCommit: 1dad9d9b190fed7d45b8ed127c0b8c5e2be236ec / schemaVersion: v0.1.0-draft
## 배경 (실패 근거)
4엔진 PoC 중 vegalite만 글리프 검사 2회 연속 green. 나머지 3엔진은 SVG 한글 보존은 통과했으나
각자 다르게 짠 playwright 검사 코드가 환경 문제로 실패:
echarts=playwright MODULE_NOT_FOUND(잘못된 해석 기준), mermaid=chromium sandbox EPERM,
graphviz=browser 조기 종료. 검사 로직이 4벌 중복 구현된 것이 원인.
## 목표
(1) vegalite PoC(packages/deck-charts/poc/vegalite/ — 검증된 정본)의 playwright 로드·pw-libs 부트스트랩·
폰트 data-URL 임베드·글리프 검사를 공용 모듈 packages/deck-charts/poc/lib/glyph-check.mjs 로 추출.
playwright는 createRequire(incubator root 절대경로 기준)로 로드하고 chromiumSandbox:false로 launch.
(2) 4엔진 PoC 전부 이 공용 모듈을 쓰도록 교체 (vegalite 포함 — 자기 코드를 모듈 호출로 치환).
(3) mermaid는 렌더 자체도 chromium을 쓰므로 같은 launch 헬퍼를 재사용.
(4) 4엔진 재실행으로 poc-result.json 갱신.
## 입력
incubator/packages/deck-charts/poc/ 전체 (vegalite가 정본), incubator/assets/fonts/
## 산출
allowedWritePaths: incubator/packages/deck-charts/poc/** (lib/ 신설과 4엔진 스크립트 수정)
## 합격기준
4엔진 각각 expectedCommand(render-poc.mjs 실행 → poc-result.json status pass && koreanTextOk) 2회 연속 green.
진짜 렌더 실패(한글 tofu)가 나오는 엔진은 조작하지 말고 fail로 정직하게 남겨라 — 실패 엔진 존재는 유효한 결과다.
expectedCommand: cd incubator && for i in 1 2; do for E in vegalite echarts mermaid graphviz; do node packages/deck-charts/poc/$E/render-poc.mjs && node -e "const r=require('./packages/deck-charts/poc/$E/poc-result.json');process.exit(r.status==='pass'&&r.koreanTextOk?0:1)" || echo "FAIL:$E"; done; done
## 금지사항
판정 기준 완화 금지 (로드 방식만 통일). contracts/ 수정 금지. 새 npm 설치 금지. allowedWritePaths 밖 쓰기 금지.
