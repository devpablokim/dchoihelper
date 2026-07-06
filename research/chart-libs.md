# 도표/다이어그램 오픈소스 라이브러리 서베이 (프레젠테이션 임베드용)

조사일: 2026-07-03
조사자: 리서치 서브에이전트
목적: HTML 슬라이드(deck-factory 파이프라인)에 정적으로 임베드 가능한 도표/다이어그램 오픈소스를 16종 서베이하고, "도표 생성 스킬"에 채택할 10종과 역할 분담을 확정한다.

## 개요

평가 대상은 지정 후보 12종(D3.js, Apache ECharts, Vega-Lite, Observable Plot, Chart.js, Plotly, Mermaid, Graphviz, Kroki, Cytoscape.js, Recharts, visx)에 마진 확보 및 비교 기준선 확보를 위해 AntV G2, Nivo, ApexCharts, GoJS 4종을 추가해 총 16종을 조사했다. matplotlib/pandas plotting과 Apache Superset은 지시에 따라 제외했다.

평가축은 다음 5가지다.
(a) HTML 슬라이드 임베드 가능성 — 정적 SVG/PNG를 헤드리스(브라우저 UI 없이, 서버/CLI)로 렌더할 수 있는가.
(b) 디자인 토큰(색/폰트) 주입 커스터마이즈 자유도.
(c) 라이선스.
(d) LLM이 코드/스펙을 생성하기 좋은 정도(문법 제약성, 문서·예제 풍부성, 학습데이터 노출도).
(e) 특기 차트/다이어그램 유형.

조사 방법은 웹서치(WebSearch) 기반이며, 라이선스 원문은 가능한 경우 GitHub의 LICENSE 파일을 직접 fetch해 확인했다(D3, ECharts, Vega-Lite, Chart.js, Plotly.js, Mermaid, Graphviz, Cytoscape.js, Recharts, visx, AntV G2, Nivo, ApexCharts, Kroki, GoJS). 별도 URL 접근 실패 사례는 없었다 — 전 항목 WebSearch 및 일부 WebFetch로 정보를 확보했다.

## 핵심 발견

1. 순수 SVG 텍스트 문자열을 헤드리스로 뽑아낼 수 있는 라이브러리(브라우저/Chromium 없이 동작)가 임베드 안정성이 가장 높다. Apache ECharts는 `renderToSVGString`으로 의존성 제로 SVG 생성이 가능하고, Vega-Lite는 `vl-convert`(Rust 바이너리, Chromium 불필요)로 매우 빠른 헤드리스 PNG/SVG 변환을 지원한다. Graphviz(dot)는 애초에 CLI 네이티브 도구라 브라우저 의존성 자체가 없다.
2. Chart.js, Plotly.js(Kaleido), Mermaid(mermaid-cli)는 모두 헤드리스 렌더를 지원하지만 내부적으로 각각 node-canvas 네이티브 바인딩, Chrome/Chromium, Puppeteer(Chromium)에 의존한다. 컨테이너 이미지 크기와 콜드스타트 비용이 커진다는 공통 리스크가 있다.
3. Kroki는 자체 렌더 엔진이 아니라 Mermaid, Graphviz, PlantUML, D2, Excalidraw, Vega/Vega-Lite, BlockDiag 계열 등 20종 이상의 다이어그램 포맷을 하나의 HTTP API(SVG/PNG 반환)로 통합하는 게이트웨이다. 개별 렌더러의 Puppeteer/Chromium 의존성을 게이트웨이 뒤로 숨길 수 있어 파이프라인 운영 복잡도를 크게 낮춘다. 단, 퍼블릭 kroki.io를 쓰면 외부 네트워크 의존과 데이터 유출 우려가 생기므로 자체 호스팅(Docker)이 원칙이다.
4. LLM 코드 생성 친화도는 "선언적 스펙 언어"일수록 높다. Vega-Lite(JSON 스키마), Mermaid(전용 텍스트 DSL), Graphviz(dot 텍스트 DSL)는 문법이 제한적이라 LLM이 문법 오류 없이 생성하기 쉽고 학습데이터 노출도도 높다. 반대로 D3.js는 로우레벨 명령형 API라 표현력은 최고지만 LLM이 축/스케일 계산을 틀리는 사고가 잦다.
5. React 종속 라이브러리(Recharts, visx, Nivo, AntV G2/ant-design-charts)는 React 런타임 없이 `ReactDOMServer.renderToStaticMarkup`으로 정적 SVG 문자열을 뽑아 순수 HTML에 붙이는 것 자체는 기술적으로 가능하지만, deck-factory가 순수 HTML/CSS 슬라이드 파이프라인이라면 React 빌드 체인을 추가로 얹는 비용 대비 이득이 낮다.
6. 라이선스 전부 상업 이용 가능한 OSI 계열이지만 예외가 둘 있다. ApexCharts는 순수 MIT가 아니라 듀얼 라이선스(연매출 200만 달러 미만 개인/조직 무료 커뮤니티 라이선스 + 그 이상은 유상 상업/OEM 라이선스)다. GoJS는 아예 오픈소스가 아닌 상용 라이선스 전용(무료 티어 없음, 도메인/애플리케이션 단위 과금)이라 이번 채택 대상에서 제외했다.
7. Graphviz는 Eclipse Public License(과거 Common Public License, 현재 EPL) 기반이다. MIT류보다 조건이 많은 약한 카피레프트 성격의 OSI 승인 라이선스이며, 단순 실행 파일 호출(서브프로세스로 dot 실행) 방식이면 배포 리스크가 낮지만 코드를 직접 링크/수정 배포하는 경우 라이선스 조항을 재확인해야 한다.

## 라이브러리별 프로필 (평가축 a~e)

| 라이브러리 | (a) 헤드리스 정적 렌더 | (b) 디자인 토큰 주입 | (c) 라이선스 | (d) LLM 생성 적합도 | (e) 특기 유형 |
|---|---|---|---|---|---|
| D3.js | 가능(SVG 네이티브). Node 헤드리스는 d3-node/jsdom 등 별도 조합 필요, 공식 원클릭 CLI는 없음 | 완전 자유(모든 속성 프로그래매틱 제어) | BSD-3-Clause | 낮음~중간(로우레벨, 문서는 방대하나 예제마다 패턴이 달라 LLM이 축/스케일 실수 잦음) | 완전 커스텀/실험적 시각화, 인포그래픽형 그래픽 |
| Apache ECharts | 매우 우수. `renderToSVGString`으로 의존성 제로 SVG, node-canvas로 PNG도 가능 | 우수. JSON 테마 객체로 색/폰트/그리드 전면 주입 | Apache-2.0 | 높음(공식 핸드북+수백 예제, 옵션 스키마가 명확) | 대시보드형(게이지, 산키, 트리맵, 레이더, 캘린더 히트맵, 3D) |
| Vega-Lite (+Vega, vl-convert) | 매우 우수. `vl-convert`(Rust, Chromium 불필요)로 초고속 PNG/SVG, `vega-cli`(vg2svg/vg2png)도 가능 | 우수. config 블록으로 색상/폰트/축 토큰 전면 주입, theme 프리셋 지원 | BSD-3-Clause | 매우 높음(선언적 JSON 스키마라 문법 오류 자체가 거의 불가능, LLM 환각 최소화에 유리) | 통계 차트 문법(그래머 오브 그래픽스), 반복 패싯/레이어 차트 |
| Observable Plot | 우수. D3 기반, headless 옵션(document 주입) 공식 지원 | 양호. 마크/스케일 옵션으로 색상 지정, 세밀한 축 커스터마이즈는 D3보다 제한적 | ISC(퍼미시브) | 높음(문법이 간결해 한 줄로 표준차트 생성, 공식 예제 풍부) | 빠른 탐색적 통계차트(막대/선/산점도/히스토그램) 1차 생성 |
| Chart.js | 우수하나 네이티브 의존. `chartjs-node-canvas`(node-canvas 필요)로 PNG, SVG 네이티브 출력은 없음(캔버스 기반) | 중간. 데이터셋/옵션 객체로 색상 지정 가능하나 세밀한 커스텀 렌더는 플러그인 필요 | MIT | 매우 높음(가장 오래되고 학습데이터 노출 최다, 스택오버플로 예제 압도적) | 심플 카드형 통계 차트(막대/선/도넛), 대시보드 미니차트 |
| Plotly.js (+Kaleido) | 우수하나 무겁다. Kaleido가 Chrome/Chromium 필요(v1은 시스템 Chrome 탐색), PNG/SVG/PDF 지원 | 양호. layout/template 객체로 색·폰트 주입, 다만 CSS 스타일링 자유도는 SVG 네이티브보다 낮음 | MIT | 높음(공식 문서·갤러리 방대, Python/R/JS 3중 생태계) | 통계/과학 차트, 3D 표면/산점도, 금융(캔들스틱), 인터랙티브 데모 |
| Mermaid (+mermaid-cli) | 우수하나 무겁다. `mmdc`가 Puppeteer(Chromium) 필요, SVG/PNG/PDF 출력 | 낮음~중간. `themeVariables`로 색상 토큰은 주입 가능하나 레이아웃 엔진(자동배치)은 손대기 어려움 | MIT | 매우 높음(텍스트 DSL, ChatGPT/Claude 학습데이터에 노출 극도로 많음, 오탈자 하나로도 파싱 실패해 검증 쉬움) | 플로우차트, 시퀀스, 간트, ER, 상태 다이어그램, 개념도 |
| Graphviz (dot) | 최우수. 순수 CLI, 브라우저/Chromium 불필요, `-Tsvg`/`-Tpng` 직접 출력 | 낮음~중간. node/edge 속성으로 색·폰트 지정 가능하나 레이아웃(자동배치) 알고리즘 자체는 커스터마이즈 불가 | Eclipse Public License(구 CPL, 약한 카피레프트, OSI 승인) | 높음(수십 년 된 dot 문법, 문서·예제 매우 풍부) | 계층 구조도, 의존성 그래프, 트리, 조직도의 자동 레이아웃 |
| Kroki | 최우수(운영 관점). 자체 렌더 없이 Mermaid/Graphviz/PlantUML/D2/Excalidraw/Vega 등 20여 종을 단일 HTTP API로 SVG/PNG 반환, Docker 자체 호스팅 시 완전 헤드리스 | 개별 백엔드 문법에 종속(예: Mermaid 소스면 Mermaid 토큰 규칙 그대로) | MIT(게이트웨이 자체), 백엔드별 원 라이선스 별도 적용 | 높음(사실상 위 DSL들을 그대로 사용, 차이는 렌더 호출 방식뿐) | 다중 다이어그램 포맷 통합 게이트웨이, 폴백/백업 렌더러 |
| Cytoscape.js | 매우 우수. Node.js에서 컨테이너 없이 자동 headless 모드로 그래프 연산 및 레이아웃 계산, 렌더 오버헤드 없음 | 양호. 스타일시트(CSS 유사 selector 문법)로 색/폰트/모양 세밀 주입 | MIT | 중간(그래프이론 API라 D3보다는 쉬우나 옵션 스키마가 큼) | 복잡한 관계망/네트워크(노드-엣지), 생물정보학형 그래프, 대규모 그래프 레이아웃(cola/fcose/dagre) |
| Recharts | 양호. React 컴포넌트라 `ReactDOMServer.renderToStaticMarkup`으로 정적 SVG 추출 가능, 별도 빌드체인 필요 | 우수(React 컴포넌트 조합 자체가 토큰 주입) | MIT | 높음(React 생태계 문서·예제 풍부) | React 대시보드 내장형 통계 차트 |
| visx (Airbnb) | 양호. Recharts와 동일하게 SSR 정적 마크업 추출 가능, 30여 개 저수준 패키지 조합 필요 | 완전 자유(D3+React 조합, 비의견형 설계) | MIT | 중간(로우레벨이라 조합 코드량이 많음, 예제는 공식 사이트에 준수) | React 환경에서 D3급 커스텀 시각화 |
| AntV G2 | 양호. Canvas/SVG/WebGL 다중 렌더러, Node SSR 문서 존재 | 우수. mark/scale/coordinate 문법으로 토큰 주입, 테마 시스템 내장 | MIT | 중간(그래머 오브 그래픽스 개념 이해 필요, 문서는 중국어 우선이라 영어 자료가 상대적으로 적음) | 그래머 오브 그래픽스 기반 커스텀 통계 차트, ant-design-charts와 연동 |
| Nivo | 양호. SSR을 처음부터 염두에 두고 설계, HTTP 렌더 API(nivo-api) 별도 제공 | 우수. theme 객체로 색·폰트 세밀 주입 | MIT | 중간(React+D3 조합형이라 Chart.js보다는 학습데이터 적음) | React 대시보드용 화려한 통계 차트(캘린더, 선버스트, 코드플로우) |
| ApexCharts | 양호. 서버에서 실 SVG 렌더 후 클라이언트 hydration 구조, 헤드리스 전용 CLI는 약함 | 양호. options 객체로 색상 주입, 애니메이션 기본 강함 | 듀얼 라이선스(커뮤니티: 연매출 200만 달러 미만 무료 / 그 이상 유상 상업·OEM) | 중간(문서 준수, 그러나 학습데이터는 Chart.js/ECharts보다 적음) | 실시간 갱신형 라인/캔들스틱, 반응형 대시보드 위젯 |
| GoJS | 우수(export 기능 자체는 SVG/Canvas/PDF/PNG 지원) 하나 오픈소스 아님 | 우수(다이어그램 에디터급 세밀 제어) | 상용 전용(무료 티어 없음, 도메인/앱 단위 과금) — 오픈소스 아님, 이번 채택 대상에서 제외 | 중간(문서 풍부하나 상용 라이선스라 공개 학습데이터 상대적으로 적음) | 조직도, BPMN, 플로우차트, 간트, 스윔레인 등 인터랙티브 다이어그램 에디터 |

## 재사용 가능 자산(라이선스 명시)

- Apache ECharts 본체 + `renderToSVGString` 헤드리스 API — Apache-2.0, npm `echarts`. 참조: 공식 핸드북 SSR 가이드.
- Vega-Lite 스펙 + `vl-convert` CLI/Rust 라이브러리 — Vega-Lite BSD-3-Clause, vl-convert 별도 확인 필요(Vega 프로젝트 하위, 통상 BSD/Apache 계열). npm `vega`, `vega-lite`, `vl-convert-python`/`vl-convert` 바이너리.
- Observable Plot — ISC 라이선스, npm `@observablehq/plot`, headless `document` 옵션으로 서버 렌더 지원.
- Mermaid + `@mermaid-js/mermaid-cli`(mmdc) — 둘 다 MIT, Docker 이미지 다수 존재(예: `minlag/mermaid-cli` 계열, 공식 CLI 리포에서 Dockerfile 제공).
- Graphviz `dot` 바이너리 — Eclipse Public License, apt/brew로 시스템 설치(`apt install graphviz`), Node 래퍼 `graphviz-cli`(prantlf, WASM 빌드, MIT)도 존재해 시스템 설치 없이 사용 가능.
- Kroki 서버 — 게이트웨이 자체 MIT, Docker Hub `yuzutech/kroki` 이미지로 즉시 자체 호스팅 가능(`docker run -d -p 8000:8000 yuzutech/kroki`), Mermaid/BPMN/Excalidraw 등은 별도 컴패니언 컨테이너로 확장.
- Cytoscape.js — MIT, npm `cytoscape`, Node.js에서 컨테이너 DOM 없이 자동 headless 인스턴스 생성 가능(레이아웃 좌표 계산 후 별도 SVG 직렬화 필요, 자체 렌더러가 SVG 문자열을 직접 뽑아주진 않음 — 좌표만 계산하고 그리기는 별도 구현 필요한 점 주의).
- Plotly.js + Kaleido — Plotly.js MIT, Kaleido MIT. Kaleido v1은 시스템에 설치된 Chrome/Chromium을 찾아 사용(자체 번들 안 함), PyPI `kaleido`, npm은 Plotly.js 자체.
- Chart.js + `chartjs-node-canvas` — 둘 다 MIT, npm 패키지로 즉시 설치, `node-canvas`(카이로 기반 네이티브 바인딩) 시스템 의존성 필요(빌드 시 libcairo 등).
- D3.js — BSD-3-Clause, npm `d3`. 서버 헤드리스는 `d3-node`(라이선스 별도 확인 필요, MIT로 통상 표기됨) 또는 `jsdom` 조합.

## 통합 권고: 채택 10종 + 역할 분담 매트릭스

deck-factory의 "도표 생성 스킬"은 순수 HTML 슬라이드에 정적 SVG를 임베드하는 것을 기본값으로 하고, 필요 시 PNG로 래스터화(썸네일/PPTX 변환용)하는 이중 출력 전략을 권고한다. 이 기준으로 아래 10종을 채택한다. React 종속 라이브러리(Recharts, visx, Nivo, AntV G2)는 SSR 정적 마크업 추출이 기술적으로 가능하지만 순수 HTML 파이프라인에 React 빌드체인을 추가하는 비용이 이득보다 커서 이번 1차 채택에서 제외한다(추후 대시보드형 산출물이 필요해지면 재검토). ApexCharts는 라이선스 조건(연매출 200만 달러 기준)이 있어 회사 규모가 커질 경우 재확인이 필요하므로 1차에서 제외한다. GoJS는 오픈소스가 아니므로 제외한다.

| 순위 | 라이브러리 | 역할(우리 파이프라인) | 렌더 방식 | 채택 이유 |
|---|---|---|---|---|
| 1 | Vega-Lite (+vl-convert) | 기본 통계 차트 1차 생성 엔진(막대/선/영역/산점도/패싯) | vl-convert 헤드리스 SVG/PNG, Chromium 불필요 | 선언적 JSON이라 LLM 환각이 가장 적고, 렌더가 가장 가볍고 빠름 |
| 2 | Apache ECharts | 화려한 대시보드형 차트(게이지/산키/트리맵/레이더/히트맵) | `renderToSVGString` 의존성 제로 SVG | 차트 타입 커버리지 최다, 테마 토큰 주입 최우수 |
| 3 | Observable Plot | 빠른 보조 차트/1회성 탐색 차트 | headless document 주입 SVG | 문법이 가장 짧아 슬라이드 한 장짜리 간단 차트에 최적 |
| 4 | Mermaid (+mermaid-cli) | 플로우차트/시퀀스/간트/ER/상태 다이어그램 | mmdc(Puppeteer) SVG/PNG, 또는 Kroki 경유 | LLM의 다이어그램 DSL 숙련도가 가장 높음(학습데이터 최다) |
| 5 | Graphviz (dot) | 계층 구조도/조직도/의존성 그래프의 자동 레이아웃 | dot CLI 네이티브 SVG/PNG, 브라우저 불요 | 가장 가볍고 안정적인 헤드리스 렌더, 레이아웃 자동배치 품질 우수 |
| 6 | Kroki | Mermaid/Graphviz/PlantUML/D2/Excalidraw 등 통합 렌더 게이트웨이 겸 폴백 | 자체 호스팅 Docker HTTP API | 개별 렌더러(Puppeteer 등) 의존성을 게이트웨이 뒤로 격리, 운영 리스크 감소 |
| 7 | Plotly.js (+Kaleido) | 통계/과학/3D 차트, 인터랙티브 데모 슬라이드 | Kaleido(Chrome) SVG/PNG/PDF | 3D·과학 차트·인터랙티브 겸용은 유일하게 커버 |
| 8 | Cytoscape.js | 복잡한 관계망/네트워크 다이어그램(노드-엣지) | headless 좌표 계산 후 자체 SVG 직렬화 | 레이아웃 알고리즘(cola/fcose/dagre) 다양성에서 Graphviz보다 유연 |
| 9 | Chart.js (+chartjs-node-canvas) | KPI 카드용 미니차트/스파크라인 | node-canvas PNG | 가장 가볍고 학습데이터 최다라 단순 반복 생성에 안정적 |
| 10 | D3.js | 완전 커스텀/브랜드 특화 인포그래픽(최후 수단) | 수동 SVG 조합(d3-node/jsdom) | 위 9종으로 표현 불가능한 비정형 시각화의 탈출구 |

역할 분담 원칙: 1~3번(Vega-Lite/ECharts/Plot)이 "통계 차트" 삼각편대, 4~6번(Mermaid/Graphviz/Kroki)이 "다이어그램/플로우" 삼각편대, 7~9번(Plotly/Cytoscape/Chart.js)이 각각 3D·과학, 네트워크, 미니차트의 틈새 보강, 10번(D3)이 표현력 한계 돌파용 최종 폴백이다. 라우팅 로직은 사용자 요청의 차트/다이어그램 유형을 분류한 뒤 위 표의 역할로 매핑하는 방식을 권고한다.

## 리스크

1. Chromium 의존 렌더러(Kaleido, mermaid-cli의 Puppeteer)는 컨테이너 이미지 크기(수백 MB)와 콜드스타트 지연을 유발한다. CI/서버리스 환경에서는 Kroki 자체 호스팅으로 우회하거나, 순수 CLI 대안(Graphviz, vl-convert)을 우선순위로 배치해야 한다.
2. 한글 폰트 임베딩 문제를 이번 조사에서 직접 검증하지 못했다. Graphviz의 오래된 폰트 렌더링 파이프라인, Mermaid의 Puppeteer 시스템 폰트 의존, Vega-Lite/ECharts의 SVG 텍스트 임베딩 방식 모두 한글 웹폰트가 슬라이드 디자인 토큰과 일치하는지 실제 렌더 테스트가 필요하다. 이는 사실 확인이 아니라 리스크로만 기재한다.
3. ApexCharts 듀얼 라이선스(연매출 200만 달러 기준)는 이번 1차 채택에서 제외했으나, 추후 채택 시 사업 규모에 따라 유상 라이선스 전환 여부를 법무 확인해야 한다.
4. Kroki 퍼블릭 인스턴스(kroki.io)를 그대로 쓰면 슬라이드에 담기는 사내 데이터가 외부 네트워크로 전송된다. 반드시 자체 호스팅 Docker로 운용해야 한다.
5. Cytoscape.js는 headless 모드에서 좌표/레이아웃만 계산해줄 뿐 SVG 렌더러가 내장돼 있지 않다는 점을 재차 확인하지 못했다(공식 문서에서 headless는 "렌더링 오버헤드 없음"이라고만 언급). 실제 SVG export 경로(cytoscape.js-svg 등 서드파티 확장 필요 여부)는 통합 전 별도 검증이 필요하다.
6. Graphviz의 라이선스(Eclipse Public License)는 MIT류보다 조항이 많다. 서브프로세스로 dot 바이너리를 호출하는 방식(코드 링크 없음)이면 통상 문제가 없다고 보는 것이 업계 관행이지만, 이번 조사에서 법률 자문을 받은 것은 아니므로 상업 배포 전 재확인을 권고한다.
7. D3.js의 서버 헤드리스 렌더(d3-node, jsdom 조합)는 커뮤니티 도구 의존도가 높고 공식 지원 경로가 아니다. 유지보수 중단 리스크가 있어 D3는 "최후의 수단" 역할로만 한정하는 것이 안전하다.

## 출처

1. https://github.com/d3/d3/blob/main/LICENSE
2. https://github.com/d3-node/d3-node
3. https://apache.github.io/echarts-handbook/en/how-to/cross-platform/server/
4. https://echarts.apache.org/en/feature.html
5. https://vega.github.io/vega/usage/
6. https://github.com/vega/vl-convert
7. https://github.com/vega/vega-lite/blob/main/LICENSE
8. https://github.com/observablehq/plot
9. https://www.chartjs.org/docs/latest/getting-started/using-from-node-js.html
10. https://www.npmjs.com/package/chartjs-node-canvas
11. https://github.com/plotly/Kaleido
12. https://github.com/plotly/plotly.js/
13. https://plotly.com/javascript/is-plotly-free/
14. https://github.com/mermaid-js/mermaid-cli
15. https://raw.githubusercontent.com/mermaid-js/mermaid/develop/LICENSE
16. https://graphviz.org/license/
17. https://graphviz.org/doc/info/command.html
18. https://kroki.io/
19. https://docs.kroki.io/kroki/diagram-types/
20. https://docs.kroki.io/kroki/setup/install/
21. https://docs.kroki.io/kroki/setup/use-docker-or-podman/
22. https://github.com/cytoscape/cytoscape.js/
23. https://js.cytoscape.org/
24. https://github.com/recharts/recharts
25. https://github.com/airbnb/visx
26. https://visx.airbnb.tech/
27. https://github.com/antvis/g2
28. https://g2.antv.antgroup.com/en/
29. https://github.com/plouc/nivo
30. https://github.com/plouc/nivo-api
31. https://github.com/apexcharts/apexcharts.js/
32. https://raw.githubusercontent.com/apexcharts/apexcharts.js/main/LICENSE
33. https://apexcharts.com/
34. https://github.com/NorthwoodsSoftware/GoJS
35. https://www.jointjs.com/blog/javascript-diagramming-libraries
