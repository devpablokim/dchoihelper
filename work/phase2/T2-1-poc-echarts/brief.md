# TASK T2-1-poc-echarts
## 메타
taskType: code / determinismClass: canonicalized / mode: attended / baseCommit: 1dad9d9b190fed7d45b8ed127c0b8c5e2be236ec / schemaVersion: v0.1.0-draft
## 목표
차트 엔진 "echarts" 한글 골든 렌더 PoC. 방법: echarts npm (설치됨). SSR SVG 모드 (init에 {renderer:'svg', ssr:true}). 파이 1종, 스택 막대 1종.
각 차트에 한국어 제목·축라벨·범례·데이터라벨(예: "매출", "영업이익률", "1분기")을 넣어 SVG로 렌더하고,
(1) SVG 내 한글 원문 문자열 보존 검사, (2) playwright로 SVG를 1280x720 페이지에 로드해 스크린샷 PNG 저장
+ 텍스트가 tofu(□)로 깨지지 않았는지 렌더된 글리프 폭 기반 자동 검사(폭이 비정상 균일하면 실패),
(3) poc-result.json 산출: {engine, status: "pass"|"fail", charts: [{type, svg, png}], koreanTextOk, notes}.
## 입력
incubator/node_modules (의존성 설치 완료), incubator/packages/deck-layouts/scripts/overflow-check.mjs (pw-libs 부트스트랩·playwright 사용 예),
incubator/assets/fonts/ (Pretendard — SVG/페이지에 @font-face로 사용)
## 산출
allowedWritePaths: incubator/packages/deck-charts/poc/echarts/ (렌더 스크립트 render-poc.mjs, out/ SVG·PNG, poc-result.json, 자동검사 스크립트)
## 합격기준
WORKERS.md T2-1 게이트 중 기계분: 한글 렌더 깨짐 0건(자동 검사 green) + poc-result.json 산출 + render-poc.mjs 재실행 가능.
opus PNG 판정은 fable 후속.
expectedCommand: cd incubator && node packages/deck-charts/poc/echarts/render-poc.mjs && node -e "const r=require('./packages/deck-charts/poc/echarts/poc-result.json');process.exit(r.status==='pass'&&r.koreanTextOk?0:1)"
## 금지사항
새 npm 의존 설치 금지(설치된 것만 — 네트워크 없음). contracts/·다른 엔진 poc 디렉토리 수정 금지.
allowedWritePaths 밖 쓰기 금지. 실패 시 status:"fail"과 원인을 poc-result.json에 정직하게 기록 (실패도 유효한 PoC 결과).
