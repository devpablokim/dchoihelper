# HTML/CSS 프레젠테이션 기술 스택 서베이

## 개요

reveal.js, Slidev, Marp(Marp CLI/Marpit), impress.js, Spectacle, 순수 HTML+CSS 커스텀 덱 6가지 방식을 5개 평가축(16:9 고정 레이아웃 제어, 폰트 스케일 강제, PDF/PNG 익스포트, 편집기 얹기 용이성, 라이선스)으로 비교했다. 추가로 상용 AI 프레젠테이션 제품 5종(Gamma, Tome, Pitch, Beautiful.ai, Canva)의 생성 워크플로우를 분석해 벤치마크할 UX 패턴을 추렸다.

핵심 결론만 먼저 적으면: 5개 OSS 프레임워크 모두 MIT 라이선스로 라이선스 리스크는 없다. 폰트 크기를 "강제로 작아지지 않게" 만드는 메커니즘은 reveal.js/impress.js/Spectacle이 공통으로 쓰는 "고정 해상도로 저작 후 transform: scale로 뷰포트에 맞춰 비율 유지 축소"이며, Marp는 이 메커니즘이 없어 저자가 임의로 작은 폰트를 지정할 수 있다. 익스포트는 Marp CLI가 PDF/PPTX/PNG/JPEG를 모두 자체 CLI로 지원해 가장 완결적이고, Slidev는 Playwright 기반으로 PDF/PPTX/PNG/MD를 지원하지만 무거운 브라우저 의존성이 있다. reveal.js는 공식적으로는 브라우저 인쇄(Chrome 전용) 방식만 1급 지원하고 PNG는 서드파티(decktape) 의존이다. impress.js는 익스포트 기능이 사실상 없다. 상용 AI 툴들은 하나같이 "아웃라인 먼저 검토 → 테마/이미지 정책을 생성 전에 확정 → 정해진 레이아웃 템플릿 카탈로그에 콘텐츠를 채워 넣음(자유 CSS 생성 아님) → 슬라이드 단위 스코프 채팅 리파인 → 다중 포맷 익스포트"라는 동일한 UX 골격을 갖고 있다.

## 핵심 발견

### 1. reveal.js

- 16:9 고정 레이아웃 제어: `Reveal.initialize({ width, height, margin, minScale, maxScale })`로 "정상 크기"(저작 해상도, 흔히 1280x720 등 16:9)를 지정하면 어떤 뷰포트에서도 종횡비를 유지한 채 균일하게 scale되어 표시된다. 완전한 커스텀 레이아웃이 필요하면 `disableLayout: true`로 자동 스케일/센터링을 끄고 직접 반응형 CSS를 짤 수도 있다(Bring Your Own Layout).
- 폰트 스케일 강제: 슬라이드 전체가 하나의 transform으로 비율 유지 축소되므로, 저작 시점 폰트 크기가 뷰포트 크기와 무관하게 항상 슬라이드 대비 동일 비율을 유지한다. 즉 "화면이 작아서 글씨가 깨진다"는 실패모드가 구조적으로 방지된다. 단, `disableLayout: true`를 쓰면 이 보장이 사라지고 저자 책임이 된다.
- PDF/PNG 익스포트: 공식 1급 기능은 `?print-pdf` 쿼리스트링 + 브라우저 인쇄 다이얼로그(Chrome/Chromium 전용, "Background graphics" 옵션 필요)뿐이다. PNG나 CI 자동화가 필요하면 서드파티 CLI인 decktape(Node, headless Chrome 기반, reveal.js 외 다른 프레임워크도 지원)에 의존해야 한다. decktape 자체 라이선스는 이번 조사에서 확인하지 못했다(미검증).
- 편집기 얹기 용이성: 원저자 hakimel이 직접 만든 상용 SaaS 편집기 slides.com이 존재한다는 것 자체가 "DOM 섹션 + JSON config" 모델이 편집기 구축에 적합함을 방증한다. 다만 slides.com 자체는 비공개 상용 제품이라 참고용 레퍼런스는 될 수 있어도 재사용 가능한 오픈소스 편집기 코드는 아니다.
- 라이선스: MIT (Copyright 2011-2026 Hakim El Hattab).

### 2. Slidev

- 16:9 고정 레이아웃 제어: Markdown 프런트매터로 `canvasWidth`, `aspectRatio` 등을 지정하는 Vue/Vite 기반 프레임워크. 슬라이드는 Vue 컴포넌트로 렌더되며 UnoCSS로 스타일링한다.
- 폰트 스케일 강제: 프레임워크 차원의 자동 최소 폰트 강제는 없고, 테마/UnoCSS 유틸리티로 개발자가 직접 관리해야 한다.
- PDF/PNG 익스포트: 브라우저 내 익스포트 UI(v0.50 이후, Chromium 기반 브라우저 권장)와 CLI(`slidev export`) 둘 다 제공하며, PDF/PPTX/PNG/MD 네 가지 포맷을 지원하는 것이 특징이다. 단 내부적으로 Playwright(`playwright-chromium`)를 프로젝트에 별도 설치해야 하며, 이 패키지가 헤드리스 브라우저 바이너리를 통째로 받기 때문에 무겁다. PPTX 익스포트는 슬라이드를 통째로 이미지로 굽기 때문에 텍스트가 선택 불가능한 래스터가 된다.
- 편집기 얹기 용이성: Slidev 자체가 이미 Markdown + 프런트매터라는 구조화된 모델과 Vite 개발 서버의 실시간 편집(Monaco 기반)을 갖추고 있어, 그 위에 아웃라인 편집 UI를 얹기는 비교적 수월하다. 다만 Vue/Vite 생태계에 강하게 결합된다.
- 라이선스: MIT (Copyright 2020-2025 Anthony Fu).

### 3. Marp / Marp CLI / Marpit

- 16:9 고정 레이아웃 제어: Marpit(핵심 CSS 레이아웃 엔진)이 테마 CSS의 `@size` 디렉티브로 슬라이드 치수와 종횡비를 정의한다. 기본값에서 다른 비율(예: 4:3)로 바꾸는 것도 순수 CSS로 가능하다는 것이 공식 이슈 트래커에서 확인된다.
- 폰트 스케일 강제: 없음. `section { font-size: 30px; }`처럼 테마 CSS 또는 슬라이드별 `<style scoped>`로 폰트를 자유롭게 지정하며, 프레임워크가 하한선을 강제하지 않는다. 즉 "글씨가 너무 작아지는" 실패모드를 막으려면 우리 쪽에서 별도 린트/정책 레이어를 얹어야 한다.
- PDF/PNG 익스포트: 6개 방식 중 가장 완결적이다. `marp-cli` 단독으로 HTML/CSS, PDF, PowerPoint(PPTX), PNG/JPEG(단일 또는 슬라이드별 다중 이미지)를 모두 생성한다. 내부적으로 puppeteer-core를 번들해 헤드리스 Chrome을 직접 관리하므로 별도 브라우저 설치 스텝이 필요 없다(설치 시 자동 처리).
- 편집기 얹기 용이성: 콘텐츠가 순수 Markdown(+최소 프런트매터/디렉티브)이라는 점이 강점이다. 텍스트 기반이라 diff가 쉽고, LLM이 생성/수정하기에도 가장 단순한 포맷이다. 공식 VS Code 확장(marp-team.marp-vscode)이 참고 구현으로 존재한다.
- 라이선스: MIT (Copyright 2018 Marp team, `marp-cli` LICENSE 원문 직접 확인 완료).

### 4. impress.js

- 16:9 고정 레이아웃 제어: 루트 엘리먼트에 `data-width`/`data-height`(v1.2.0부터 기본값이 HD 1920x1080으로 변경되어 기본적으로 16:9), `data-max-scale`/`data-min-scale`로 목표 해상도와 스케일 한계를 지정하면, 뷰포트 크기와 무관하게 이 해상도 기준으로 자동 스케일된다. 다만 각 스텝(`.step`)은 무한 캔버스 위에 `data-x/data-y/data-z/data-rotate/data-scale`로 자유롭게 배치되는 3D 프레지(prezi.com) 스타일이라, 순차적 슬라이드 리스트가 아니라 공간적 좌표 모델이다.
- 폰트 스케일 강제: reveal.js와 동일한 "고정 해상도 저작 + 전체 transform 축소" 메커니즘이라 구조적으로는 안전하지만, 스텝 내부 요소는 반드시 픽셀 값으로 크기를 지정해야 하며(`%` 같은 상대 단위 금지) 저작 제약이 더 까다롭다.
- PDF/PNG 익스포트: 공식 문서(DOCUMENTATION.md)에 익스포트 관련 언급이 전혀 없다. 커뮤니티 차원에서 decktape 등을 시도하는 사례가 있으나 3D 좌표/카메라 애니메이션 특성상 안정적으로 지원되지 않는다. 6개 방식 중 익스포트가 가장 약하다.
- 편집기 얹기 용이성: 스텝이 순차 리스트가 아니라 x/y/z/rotate 좌표를 가진 자유 배치 공간이므로, "슬라이드 추가/순서 변경" 같은 표준 덱 편집 UI를 얹기가 구조적으로 어렵다. 논리적 슬라이드 리스트가 필요한 덱 팩토리 파이프라인에는 적합하지 않고, 줌/패닝 연출이 핵심 가치인 니치 프레젠테이션에만 적합하다.
- 라이선스: MIT (Copyright 2011-2016 Bartek Szopka).

### 5. Spectacle (Formidable Labs, React)

- 16:9 고정 레이아웃 제어: `<Deck>` 컴포넌트에 크기(width/height) prop을 지정하는 방식으로, JSX 컴포넌트 트리로 슬라이드를 구성한다. React 컴포넌트이므로 라이브 코드 데모 등 인터랙티브 콘텐츠 임베드에 강하다.
- 폰트 스케일 강제: 디자인 토큰(폰트 크기 스케일) 기반이며, 다른 스케일-투-핏 프레임워크들과 유사하게 전체 비율 유지 축소 메커니즘을 쓴다.
- PDF/PNG 익스포트: 브라우저 인쇄 스타일시트 기반의 PDF 내보내기가 커뮤니티 예제 수준에서 언급되나, 공식 저장소 자체에는 전용 헤드리스 PNG 익스포터가 번들되어 있지 않다. 공식 문서 사이트(commerce.nearform.com/open-source/spectacle)를 별도로 참조해야 하며, 이번 조사에서 export 전용 페이지까지는 확인하지 못했다.
- 편집기 얹기 용이성: 슬라이드가 곧 JSX/React 컴포넌트이므로, 이미 React 기반 파이프라인(예: LLM이 JSX를 직접 생성)이라면 가장 자연스럽게 맞물린다. 반대로 비개발자용 시각적 드래그앤드롭 에디터를 얹으려면 JSX AST를 다루거나 별도 스키마→React 컴파일러를 만들어야 해서 진입장벽이 있다.
- 라이선스: MIT (GitHub 저장소 License 배지로 확인).

### 6. 순수 HTML+CSS 커스텀 덱

- 16:9 고정 레이아웃 제어: `aspect-ratio: 16/9` 컨테이너 + CSS Container Queries(`container-type: inline-size`, `cqw` 단위) 조합으로 완전한 자체 제어가 가능하다. 사실 위 5개 프레임워크가 내부적으로 쓰는 "고정 해상도 저작 + transform 축소" 기법도 결국 순수 CSS 트릭이므로, 커스텀 덱에서 동일한 패턴을 직접 구현하면 동등한 안전성을 확보할 수 있다.
- 폰트 스케일 강제: `clamp()` + container query 단위로 하한선을 코드 레벨에서 강제할 수 있어, 오히려 프레임워크보다 더 엄격한 정책(예: "본문 최소 24px 미만 금지"를 빌드 타임에 린트)을 걸기 쉽다.
- PDF/PNG 익스포트: 프레임워크가 대신 해주는 게 없으므로 Playwright/Puppeteer로 `page.pdf()`/`page.screenshot()` 파이프라인을 직접 구축해야 한다. 다만 이는 Slidev나 Marp CLI가 내부적으로 하는 작업과 동일한 성격이라 "더 많은 일"이라기보다 "숨겨져 있던 일을 우리가 직접 소유"하는 것에 가깝다.
- 편집기 얹기 용이성: 프레임워크의 컴포넌트/디렉티브 관성이 전혀 없는 그린필드이므로, JSON 스펙 ↔ HTML 렌더러 ↔ 시각적 에디터를 처음부터 1:1로 설계할 수 있다. 초기 구축 비용은 가장 높지만 장기적으로 가장 이질감 없는 통합이 가능하다.
- 라이선스: 해당 없음(자체 코드), 업스트림 버전 추적/보안 패치 부담이 없다는 것도 장점이다.

### 7. 상용 AI 프레젠테이션 제품 워크플로우 비교

| 제품 | 생성 흐름 | 레이아웃 결정 방식 | 리파인 방식 | 익스포트 |
|---|---|---|---|---|
| Gamma | 토픽/컨텍스트 입력 → 카드 수 지정 → 아웃라인 생성 → 아웃라인 편집(가장 저렴한 수정 지점) → 테마/이미지 모델/텍스트 밀도 설정 → 전체 덱 생성 → 검토 | AI가 생성 시점에 레이아웃도 함께 결정(템플릿 카탈로그 방식인지는 비공개) | 스파클 아이콘으로 여는 에이전트 채팅, 슬라이드 단위 자연어 지시 → 미리보기 → 승인/되돌리기, 버전 히스토리 보관 | PDF, PPTX, Google Slides. 복잡한 멀티컬럼 레이아웃은 PPTX 변환 시 깨질 수 있음 |
| Tome | (과거) 프롬프트 → 서사 중심 생성, 타일 기반 드래그앤드롭의 유동적(scroll) 레이아웃, Figma/Miro 라이브 임베드 지원 | 고정 슬라이드 그리드가 아닌 자유 캔버스 | 텍스트 프롬프트 재생성 위주 | PPTX 호환 취약(장기간 미지원), PDF만 우선 지원 |
| Beautiful.ai | 다양한 입력(짧은 프롬프트/슬라이드별 상세 프롬프트/붙여넣은 아웃라인/문서 업로드) → 저해상도 아웃라인 초안(슬라이드별 제목+요점) → 아웃라인 전용 채팅 레이어로 순서변경/분할/톤 조정 → 생성 전에 테마·이미지 소스(AI/웹/스톡/없음)·언어 확정 → Smart Slides로 전체 슬라이드 생성 → 슬라이드별로 여러 레이아웃 후보 미리보기 후 원클릭 교체 | Smart Slides라는 결정론적 레이아웃 템플릿 시스템이 간격/정렬/위계/애니메이션을 자동 적용 — "자유 CSS 생성"이 아니라 "검증된 템플릿에 콘텐츠를 채우는" 방식 | 슬라이드 단위 AI 패널에서 프롬프트를 직접 보고 수정 가능(prompt transparency), 텍스트 보존 옵션, 이미지만 독립 재생성 가능 | PPTX(편집 가능), 웹 임베드 |
| Pitch | 블랭크/템플릿/AI(Pitch Agent) 중 택1로 시작 → Create(제작) → Collaborate(슬라이드 배정, 실시간 공동편집, 댓글) → Deliver(인터랙티브 임베드/애니메이션, 공유 링크, 커스텀 "피치룸", 방문자 열람 분석) | 150개 이상 전문가 제작 템플릿 + 브랜드 라이브러리(폰트/로고/미디어)로 팀 전체의 일관성 강제 | 팀 단위 협업(슬라이드 담당자 배정, 코멘트)이 핵심, AI 리파인은 Pitch Agent로 보조적 | PPTX 임포트/익스포트, 공유 링크 기반 열람 추적 |
| Canva (Magic Design / Canva AI) | 홈페이지에서 토픽 프롬프트 입력(템플릿 탭 경유 시 아웃라인 단계 생략됨) → AI가 섹션별 아웃라인 생성 → 드래그 핸들로 섹션 추가/삭제/순서변경, 섹션별 핵심 아이디어 편집 → "Generate presentation" → 완성된 템플릿형 덱. 별도로 "Edit with AI"는 기존 템플릿을 고른 뒤 그 템플릿의 시각적 스타일은 유지한 채 프롬프트로 콘텐츠만 재생성 | 템플릿의 "시각적 DNA"와 "콘텐츠"를 명확히 분리 — 템플릿이 제약(틀)을 제공하고 프롬프트가 내용만 채움 | Edit with AI 재실행, PDF/Word 문서 첨부로 컨텍스트 보강 가능 | Canva 자체 포맷/PDF/PPTX(Canva 생태계 표준 익스포트) |

벤치마크할 만한 공통 UX 패턴 5가지:

1. 2단계 생성(아웃라인 우선): 저비용 구조 초안(슬라이드별 제목+요점)을 먼저 만들어 사용자가 검토/수정하게 하고, 비용이 큰 전체 비주얼 생성은 그 다음에 실행한다. Gamma, Beautiful.ai, Canva 모두 이 패턴을 명시적으로 "가장 저렴한 수정 지점"이라 강조한다.
2. 생성 전 스타일 확정: 테마/브랜드 컬러·폰트, 이미지 소스 정책, 텍스트 밀도 같은 전역 설정을 아웃라인과 본 생성 사이에 한 번에 확정해, 슬라이드마다 스타일이 들쭉날쭉해지는 것을 막는다.
3. 결정론적 레이아웃 템플릿 카탈로그: Beautiful.ai의 Smart Slides와 Canva의 "템플릿 시각적 DNA 고정" 방식이 실제로 폰트 크기/오버플로 문제를 방지하는 메커니즘이다. LLM의 역할은 자유 CSS 생성이 아니라 "콘텐츠 작성 + 검증된 템플릿 중 선택"으로 제한된다.
4. 슬라이드 단위 스코프 채팅 리파인: 전체 덱을 재생성하지 않고 특정 슬라이드만 프롬프트로 수정하며, 미리보기 후 승인/되돌리기, 버전 히스토리를 제공한다.
5. 다중 포맷 병렬 익스포트: 하나의 소스 오브 트루스에서 PDF(보관/전달용), PPTX(편집 인계용), 웹 링크(인터랙티브 공유+열람 추적용)를 동시에 뽑아준다.

반면교사 사례: Tome은 슬라이드 그리드를 버리고 유동적 캔버스/타일 방식을 택했다가 기업 워크플로우 적합성(PPTX 호환 부재 등)에서 밀려 회사 차원에서 프레젠테이션 제품 우선순위를 낮추고 CRM(Lightfield)으로 피벗했다. "자유로운 캔버스"가 곧 "더 나은 결과물"은 아니라는 근거로 참고할 만하다.

## 재사용 가능 자산 (라이선스 명시)

- reveal.js 본체: https://github.com/hakimel/reveal.js/ — MIT
- Slidev 본체: https://github.com/slidevjs/slidev — MIT (Anthony Fu, 2020-2025)
- Marp CLI: https://github.com/marp-team/marp-cli — MIT (Marp team, 2018), LICENSE 원문 직접 확인
- Marpit(핵심 CSS 레이아웃 엔진): https://github.com/marp-team/marpit — MIT 계열(marp-cli와 동일 조직/라이선스 정책)
- impress.js: https://github.com/impress/impress.js/ — MIT (Bartek Szopka, 2011-2016)
- Spectacle: https://github.com/FormidableLabs/spectacle — MIT
- decktape(reveal.js 등 다용도 헤드리스 PDF 익스포터): https://github.com/astefanutti/decktape — 라이선스 미검증(이번 조사 범위 밖, 사용 전 별도 확인 필요)
- Marp VS Code 확장(편집기 참고 구현): https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode

## 통합 권고

deck-factory 파이프라인이 "LLM이 스펙을 생성하고 → 자동으로 16:9 고정 덱을 렌더링하고 → PDF/PNG로 뽑아내는" 구조라면, 다음 조합을 권고한다.

1차 후보(콘텐츠 생성 레이어): Marp/Marpit 방식을 참고해 Markdown+프런트매터 또는 그와 동급으로 단순한 텍스트 기반 슬라이드 스펙을 LLM 출력 포맷으로 채택한다. 텍스트 포맷은 diff가 쉽고 LLM이 다루기 가장 안전하다. 단, Marp 자체의 폰트 크기 무강제 문제를 그대로 가져오면 안 되므로, 상용 AI 툴들의 "결정론적 레이아웃 템플릿" 패턴을 그대로 이식해야 한다 — 즉 LLM에게 자유 CSS/폰트 크기를 맡기지 말고, 사전에 우리가 튜닝해 둔 레이아웃 템플릿 카탈로그(제목+불릿, 빅스탯, 2단 컬럼, 이미지-좌 등) 중 하나를 선택하고 그 템플릿에 콘텐츠만 채우게 한다.

2차 후보(렌더링/스케일 레이어): reveal.js 또는 impress.js가 쓰는 "고정 해상도 저작 + transform: scale로 뷰포트에 맞춰 비율 유지 축소" 기법을 순수 HTML+CSS 커스텀 덱에 직접 이식한다. 프레임워크 전체를 들여올 필요 없이 이 스케일링 패턴(수십 줄짜리 CSS/JS)만 재사용하면 "작은 글씨 방지" 요구사항을 프레임워크 의존성 없이 만족시킬 수 있다.

3차 후보(익스포트 레이어): Marp CLI가 puppeteer-core를 내부 번들해 PDF/PPTX/PNG를 한 번에 뽑는 방식을 그대로 벤치마크해, Playwright 기반 자체 익스포트 스크립트(`page.pdf()` + `page.screenshot()`)를 구축한다. Slidev의 CLI 옵션 설계(`--format pdf|pptx|png|md`, `--range`, `--dark`, `--wait`)도 CLI 인터페이스 설계 시 참고할 만하다.

편집기 레이어: 텍스트 기반 스펙(1차 후보)을 채택하면 편집기는 "스펙을 편집하는 구조화 폼/아웃라인 뷰"만 만들면 되고, 렌더러는 항상 스펙→HTML을 재생성하는 단방향 파이프라인으로 유지하는 것이 가장 유지보수하기 쉽다. Beautiful.ai/Gamma처럼 "아웃라인 단계"와 "테마 확정 단계"를 UI상 명확히 분리하는 2단계 흐름을 그대로 채택할 것을 권한다.

기존 5개 OSS 프레임워크를 통째로 프로덕션에 들여오는 것은 권장하지 않는다. reveal.js/Slidev/Marp/impress.js/Spectacle 각각이 특정 사용 사례(개발자 발표, 마크다운 저작, prezi식 줌 연출, React 라이브 데모)에 최적화되어 있어 범용 "AI 생성 덱 팩토리"에는 과결합된 관성이 딸려온다. 대신 위에서 정리한 세 가지 검증된 패턴(텍스트 기반 스펙, 고정해상도+transform 스케일링, headless 브라우저 익스포트)만 뽑아 순수 HTML+CSS 커스텀 스택 위에 재구현하는 것이 장기적으로 더 가볍고 통제 가능하다.

## 리스크

- Marp 계열을 차용할 경우, 폰트 크기 하한을 프레임워크가 강제하지 않으므로 우리 쪽 템플릿/린트 레이어를 반드시 별도로 만들어야 한다. 이를 빠뜨리면 "작은 글씨 방지"라는 핵심 요구사항이 깨진다.
- reveal.js의 PNG 익스포트와 CI 자동화는 서드파티 decktape에 의존하는데, 이 도구의 라이선스와 유지보수 활성도를 이번 조사에서 검증하지 못했다. 채택 전 별도 확인이 필요하다.
- Slidev의 PDF/PPTX/PNG 익스포트는 `playwright-chromium` 풀브라우저 바이너리 설치를 요구해 빌드/배포 이미지가 무거워진다. 서버리스/경량 컨테이너 환경에는 부적합할 수 있다.
- impress.js는 익스포트 기능이 사실상 없고, 콘텐츠 모델이 순차 슬라이드가 아닌 3D 좌표 배치라 표준 "슬라이드 추가/순서 변경" 편집기와 근본적으로 안 맞는다. 덱 팩토리 용도로는 채택 근거가 약하다.
- Spectacle은 React/JSX에 강결합되어 있어 편집기 레이어를 React 생태계에 종속시키게 되며, 공식 익스포트 문서가 이번 조사 범위에서 명확히 확인되지 않았다(추가 확인 필요).
- 순수 HTML+CSS 커스텀 방식은 초기 구축 비용(스케일링 로직, 익스포트 파이프라인, 편집기)을 전부 자체 부담해야 한다는 리스크가 있다. 다만 이 비용은 정확히 위 프레임워크들이 내부적으로 이미 해결해 둔 문제를 재발명하는 것이므로, 그들의 구현을 참고 삼아 재현하면 리스크를 크게 낮출 수 있다.
- Tome의 실패 사례(유동적 캔버스 UX가 기업 채택률에서 밀려 회사가 프레젠테이션 제품 우선순위를 낮춤)는 "자유도가 높은 레이아웃일수록 좋다"는 가정이 틀릴 수 있다는 근거다. deck-factory가 자유 캔버스형 UX를 검토 중이라면 이 리스크를 감안해야 한다.
- 이번 조사에서 Tome의 공식 웹사이트/제품 페이지는 직접 스크래핑하지 못했고 비교 리뷰(beautiful.ai 발행) 및 서드파티 자료에만 의존했다. Tome 자체 1차 출처 확인은 실패로 기록한다.

## 출처

1. https://github.com/hakimel/reveal.js/
2. https://github.com/hakimel/reveal.js/blob/master/LICENSE
3. https://revealjs.com/pdf-export/
4. https://revealjs.com/presentation-size/
5. https://github.com/astefanutti/decktape (decktape 언급 근거, 라이선스 미검증)
6. https://sli.dev/guide/exporting
7. https://github.com/slidevjs/slidev
8. https://github.com/slidevjs/slidev/blob/main/LICENSE
9. https://github.com/marp-team/marp-cli
10. https://raw.githubusercontent.com/marp-team/marp-cli/main/LICENSE
11. https://marpit.marp.app/
12. https://github.com/marp-team/marpit/issues/163
13. https://stackoverflow.com/questions/78349602/how-to-specify-fontsize-for-individual-slides-marp
14. https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode
15. https://github.com/impress/impress.js/
16. https://github.com/impress/impress.js/blob/master/DOCUMENTATION.md
17. https://github.com/impress/impress.js/blob/master/LICENSE
18. https://github.com/FormidableLabs/spectacle
19. https://gamma.app/
20. https://www.mindstudio.ai/blog/create-professional-ai-presentation-gamma-under-10-minutes
21. https://www.beautiful.ai/comparison/beautiful-ai-vs-tome
22. https://www.beautiful.ai/blog/introducing-the-create-with-ai-workflow
23. https://pitch.com/
24. https://www.canva.com/help/using-magic-presentations/
