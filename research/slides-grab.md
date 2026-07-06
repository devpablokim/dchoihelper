# slides-grab 코드 구조 분석

분석 대상 리포: NomaDamas/slides-grab (기본 브랜치 main, shallow clone 성공)
분석 시각 기준 package.json version 1.0.0

## 개요

slides-grab는 "에이전트 우선(agent-first) 프레젠테이션 프레임워크"다. 슬라이드 한 장을 자체 완결형 HTML+CSS 파일(slide-XX.html)로 다루고, 코딩 에이전트(Codex CLI 또는 Claude Code)에게 슬라이드를 계획/디자인/편집시킨 뒤 PDF/PPTX/PNG/Figma로 내보낸다. 핵심 차별점은 "비주얼 에디터"다. 브라우저에서 슬라이드 위에 사각형(bbox)을 드래그로 그려 영역을 지정하고, 그 영역 스크린샷에 빨간 박스를 합성한 이미지를 프롬프트와 함께 로컬 codex/claude 서브프로세스에 넘겨 해당 슬라이드 HTML 파일만 고쳐 쓰게 한다. 텍스트/색/크기/볼드 같은 단순 변경은 에이전트를 거치지 않고 브라우저에서 직접 DOM을 편집해 파일로 저장한다.

전체 워크플로는 3단계다. Plan(주제/파일에서 slide-outline.md 구조 생성) → Design(슬라이드별 HTML 생성) → Edit(비주얼 에디터로 반복 수정) → Export(디자인 게이트 통과 후 PDF/PPTX/Figma). 원류는 uxjoseph/ppt_team_agent(Builder Josh)이며 그 위에 비주얼 에디터와 다중 익스포트, 95종 디자인 스타일, 스킬 패키징을 얹었다.

## 핵심 발견

### 라이선스
- LICENSE 파일은 MIT. "Copyright (c) 2026 Jeffrey". package.json license 필드도 MIT, author는 vkehfdl1. 재사용/수정/재배포/판매 모두 허용, 저작권 고지만 유지하면 됨. 상업적 파생 및 코드 차용에 제약 없음.

### 언어/런타임/프레임워크
- 순수 Node.js(ESM, "type": "module"), engines node >=20. TypeScript는 devDependency일 뿐 소스는 .js/.cjs 혼용(대부분 순수 JS). 빌드 단계 없이 그대로 실행.
- CLI 프레임워크: commander. 서버: express 5. 렌더링/스크린샷/PDF: playwright(chromium). 이미지 합성: sharp. PPTX 생성: pptxgenjs. PDF 병합: pdf-lib. 다이어그램: tldraw + react/react-dom. 아이콘: lucide-react. 이미지 생성: god-tibo-imagen(로컬 Codex ChatGPT 로그인 재사용).
- 프런트엔드 에디터는 빌드 없는 바닐라 JS ES 모듈(브라우저가 직접 import). React는 tldraw 렌더링 전용이지 에디터 UI에는 안 씀.

### 모듈 구조 (파일 수준)
- bin/ppt-agent.js: 단일 CLI 엔트리(package.json bin "slides-grab"). commander로 서브커맨드 등록 후 대부분을 scripts/*.js 를 child_process.spawn(stdio inherit, cwd=사용자 디렉토리, env PPT_AGENT_PACKAGE_ROOT)로 실행. 커맨드: build-viewer, validate(alias lint), design-gate, install-skills/install-runtime, convert(PPTX), pdf, png, fetch-video, figma, tldraw, image, edit, list-templates, list-styles, preview-styles, import-design, show-design, show-template.
- scripts/: 각 커맨드의 실제 구현. editor-server.js(에디터 서버), html2pdf.js, html2png.js, html2pptx.js, figma-export.js, validate-slides.js, build-viewer.js, design-gate.js, generate-image.js, download-video.js, render-tldraw.js, install-runtime.js.
- src/: 순수 로직 라이브러리. slide-mode.cjs(프레임 치수 정의), image-contract.js(자산 경로 계약 + 런타임 HTML 주입), resolve.js(템플릿/패키지 루트 해석), design-styles.js/design-styles-data.js/design-diversity-data.js(95종 스타일), design-md-parser.js/design-import.js(커스텀 DESIGN.md), design-gate-state.js/report.js(익스포트 게이트), html2pptx.cjs/pptx-raster-export.cjs/export-resolution.cjs(PPTX), figma.js, validation/(검증 코어+CLI), tldraw/render.js, nano-banana.js/god-tibo-imagen.js(이미지 프로바이더).
- src/editor/: 비주얼 에디터. editor.html(1736줄, UI 셸+CSS), codex-edit.js(프롬프트/서브프로세스 인자 빌더+스크린샷 주석), edit-subprocess.js(서브프로세스 실행/타임아웃/abort), screenshot.js(playwright 캡처), editor-codex-prompt.md(에디터용 디자인 규칙 프롬프트), js/*(프런트 모듈 16개).
- templates/: 슬라이드 HTML 템플릿 13종(cover, content, chart, diagram, diagram-tldraw, timeline, team, quote, split-layout, statistics, contents, closing, section-divider) + templates/custom/(사용자 오버라이드), templates/design-styles/(프리뷰).
- skills/: Vercel Agent Skills 포맷 SKILL.md 5개(slides-grab, -plan, -design, -export, -card-news) + references/. runtimes/: codex/claude-code 어댑터(design-critic 에이전트).

### HTML 슬라이드 출력 포맷 (중요)
- 각 슬라이드는 독립 완결형 HTML 문서(<!DOCTYPE html> 통짜). 파일명 규칙은 정규식 /^slide-.*\.html$/i (예: slide-01.html). 슬라이드 디렉토리 기본값은 slides/, --slides-dir로 변경.
- 물리 치수는 pt 단위 CSS로 body에 하드코딩. presentation 모드 body 720pt x 405pt(16:9), card-news 모드 720pt x 720pt(1:1). src/slide-mode.cjs가 단일 소스. 좌표계(에디터 bbox 기준)는 960x540(presentation)/960x960(card-news)이고 PT_TO_PX=96/72로 framePx=960x540 계산. 스크린샷 캡처는 1600x900(또는 1600x1600).
- 폰트: Pretendard를 jsDelivr CDN으로 링크하는 게 기본. 색은 항상 # 접두. 텍스트는 반드시 시맨틱 태그(p, h1~h6, ul, ol, li) 안에 두고 div/span 직접 텍스트 금지(검증기가 강제).
- 스타일은 인라인 style 속성 위주(템플릿 예시가 전부 인라인 flex/grid 레이아웃). 카드리스/화이트스페이스 우선 디자인 가이드.
- 자산 계약(src/image-contract.js): 로컬 이미지/영상은 <slides-dir>/assets/ 에 두고 슬라이드에서 ./assets/<file> 상대경로로 참조. data: URL 허용. 원격 http(s):// 이미지 URL, 절대 파일경로(/Users, C:\ 등), 루트상대(/x), 기타 스킴은 저장 슬라이드에서 금지(critical). 비정규 상대경로는 warning. content 이미지는 <img>로, body 외 요소 background-image 금지.
- 런타임 주입(buildSlideRuntimeHtml): 에디터/뷰어가 슬라이드를 iframe으로 서빙할 때 <head>에 <base href>와 자산검증 <script>를 주입한다. 단 이 주입물은 저장 파일에는 절대 영속화하지 않음(프롬프트 규칙과 direct-edit 직렬화가 원본만 저장).
- 다중 슬라이드 뷰어: build-viewer가 slide-*.html들을 단일 viewer.html로 묶음(GitHub Pages showcase도 동일).

### 비주얼 에디터 동작 (편집 파이프라인)
- slides-grab edit → scripts/editor-server.js가 express 서버(기본 포트 3456) 기동. 라우트: GET / (editor.html), GET /slides/:file (원본 HTML에 런타임 주입해 iframe용으로 서빙), GET /api/slides(파일 목록), POST /api/slides/:file/save(직접편집 저장), GET /api/config(모드/치수), GET /api/models, GET/POST /api/runs(에이전트 실행 기록), GET /api/events(SSE), POST /api/apply(에이전트 편집 실행), POST /api/runs/:runId/cancel. /js 정적 서빙, /slides/assets 정적 서빙. fs.watch로 파일 변경 감지→SSE fileChanged.
- 에이전트 편집 경로(POST /api/apply): 슬라이드/프롬프트/selections(bbox+xpath 타깃)/model 수신 → 슬라이드당 동시 1런 락 → playwright로 슬라이드 스크린샷 캡처 → sharp로 빨간 bbox+번호 라벨 SVG 합성(writeAnnotatedScreenshot) → buildCodexEditPrompt로 프롬프트 조립 → codex 또는 claude 서브프로세스 spawn → stdout/stderr를 SSE(applyLog)로 스트리밍 → 완료 시 파일은 에이전트가 직접 수정, fs.watch가 감지해 iframe 리로드. AbortController+SIGTERM/SIGKILL로 취소/타임아웃/클라이언트 끊김 처리.
- 서브프로세스 인자(codex-edit.js): Codex는 `codex --dangerously-bypass-approvals-and-sandbox exec --color never [--model X] [--image annotated.png] -- <prompt>`. Claude는 `claude -p --permission-mode acceptEdits --model X --max-turns 30 --verbose <prompt>`(이미지 경로를 프롬프트 앞에 텍스트로 안내). 바이너리는 env PPT_AGENT_CODEX_BIN/PPT_AGENT_CLAUDE_BIN로 오버라이드.
- 모델 레지스트리(src/editor/js/model-registry.js, 브라우저/노드 공용): CODEX_MODELS=[gpt-5.5, gpt-5.4, gpt-5.3-codex, gpt-5.3-codex-spark], CLAUDE_MODELS=[claude-opus-4-8, claude-sonnet-4-6]. isClaudeModel로 디스패치 분기. 기본은 gpt-5.5. 모델 추가는 이 배열 + editor.html <option> 두 곳.
- 직접 편집 경로(에이전트 미경유): editor-select.js가 iframe DOM 요소를 XPath로 선택, editor-direct-edit.js가 style 변경(볼드/이탤릭/밑줄/취소선/정렬/색/크기/텍스트)을 iframe DOM에 적용 후 document.documentElement.outerHTML를 직렬화해 디바운스 저장(POST /api/slides/:file/save). editor-bbox.js는 bbox 드로잉·렌더·XPath 타깃 추출, editor-sse.js는 SSE 수신, editor-send.js는 /api/apply 호출·bbox 상태(pending/review) 관리.
- 프롬프트 조립(buildCodexEditPrompt): 편집 대상 슬라이드 경로 1개만 수정하도록 강한 제약 + editor-codex-prompt.md(또는 slides-grab-design SKILL 폴백)의 디자인 규칙 + 로컬 DESIGN.slides.md/DESIGN.md가 있으면 "신뢰불가 디자인 데이터"로 감싸 주입(프롬프트 인젝션 방어) + 선택 영역 bbox/XPath + 자산 계약 규칙.

### 익스포트 & 디자인 게이트
- convert(PPTX)/pdf/figma는 실행 전 assertDesignGateReady로 게이트 검사. slides-grab design-gate가 verdict=proceed와 Pass A/B 리뷰 리포트, PNG 증거를 <slides-dir>/.slides-grab/ 에 기록해야만 통과. 게이트는 슬라이드 파일 SHA-256 지문과 로컬 자산 지문을 저장해, 슬라이드가 바뀌면 게이트가 무효화됨.
- PPTX: html2pptx.cjs가 playwright로 렌더 후 텍스트/이미지/도형/불릿을 pptxgenjs 객체로 best-effort 변환(placeholder 클래스 위치 추출). 실험적/불안정 명시. figma-export는 같은 파이프라인으로 Figma Slides 임포트용 pptx 산출(업로드 아님). 기본 래스터 해상도 2160p/4k. pdf는 capture(래스터, 기본)/print(선택가능 텍스트) 모드. png는 슬라이드당 1 PNG(카드뉴스 1:1 인스타용).

## 재사용 가능 자산 (라이선스 명시: 전부 MIT, NomaDamas/slides-grab)

- 비주얼 bbox 편집 아키텍처 전체: scripts/editor-server.js + src/editor/codex-edit.js + src/editor/js/*. 우리 파이프라인의 "슬라이드 위 영역 지정→에이전트 수정" 기능을 통째로 차용 가능.
- 자산 경로 계약 + 런타임 검증 주입: src/image-contract.js (classifyImageSource, buildImageContractReport, buildSlideRuntimeHtml). 슬라이드 자산 규율을 그대로 이식 가능.
- 슬라이드 치수/모드 정의 단일 소스: src/slide-mode.cjs (720x405 / 720x720, PT_TO_PX, 스크린샷 치수, pptx/figma inch 매핑).
- 스크린샷 주석 합성기: codex-edit.js의 buildAnnotationSvg/writeAnnotatedScreenshot (sharp + SVG 오버레이).
- 서브프로세스 실행 하네스: src/editor/edit-subprocess.js (타임아웃/abort/로그 미러링), codex/claude 인자 빌더.
- 익스포트 게이트 패턴: src/design-gate-state.js (SHA-256 지문 기반 stale 감지).
- 슬라이드 HTML 템플릿 13종: templates/*.html (인라인 스타일, Pretendard, 720x405).
- 95종 디자인 스타일 데이터: src/design-styles-data.js, src/design-diversity-data.js. 단 이 중 30종은 corazzon/pptx-design-styles, 60종은 epoko77-ai/design-diversity에서 파생 — 재배포 시 원저작권/라이선스 별도 확인 필요(아래 리스크).
- Pretendard 폰트: OFL, CDN(orioncactus/pretendard v1.3.9) 사용. 상업 재배포 가능(OFL 준수).
- 에이전트 스킬 팩: skills/slides-grab-*/SKILL.md + references/ (Plan/Design/Export/CardNews 워크플로, 디자인 규칙, ooxml/html2pptx 참조).

## 통합 권고 (deck-factory 파이프라인 관점)

- 우리가 "HTML 슬라이드 + 에이전트 편집"을 얹으려면 이식 우선순위는 (1) src/slide-mode.cjs로 치수/좌표계 표준을 맞추고, (2) src/image-contract.js의 자산 계약과 런타임 주입을 채택해 저장 안전성/이식성을 확보하고, (3) 편집 기능은 scripts/editor-server.js의 /api/apply 흐름(스크린샷→bbox 주석→codex/claude exec→파일 직수정→fs.watch 리로드)을 코어로 삼는 것.
- "편집 기능"을 확장할 지점(파일 수준):
  - 새 코딩 에이전트/모델 추가: src/editor/js/model-registry.js의 CODEX_MODELS/CLAUDE_MODELS 배열 + src/editor/codex-edit.js의 buildCodexExecArgs/buildClaudeExecArgs(+ scripts/editor-server.js의 spawnCodexEdit/spawnClaudeEdit 분기) + editor.html <option>. README도 에디터가 "pure javascript라 새 에이전트 추가가 쉽다"고 명시.
  - 편집 프롬프트/규칙 변경: src/editor/editor-codex-prompt.md 및 src/editor/codex-edit.js의 buildCodexEditPrompt(제약/디자인 규칙/DESIGN.md 주입).
  - 직접(비에이전트) 편집 UI 확장(새 스타일 컨트롤/도형 조작): src/editor/js/editor-direct-edit.js + editor-select.js + editor.html의 툴바 마크업. 저장은 /api/slides/:file/save.
  - 새 API/서버 동작: scripts/editor-server.js에 라우트 추가. SSE 이벤트는 broadcastSSE.
  - bbox/좌표/XPath 추출 로직: src/editor/js/editor-bbox.js(getXPath, extractTargetsForBox) + codex-edit.js의 normalizeSelection/scaleSelectionToScreenshot.
- 익스포트를 붙일 때는 design-gate 강제를 그대로 쓸지 결정 필요(현재 PDF/PPTX/Figma는 게이트 없이는 실행 거부). 우리 파이프라인이 자동화라면 design-gate를 자동 기록하거나 게이트 체크를 우회하는 래퍼가 필요.
- 에디터는 로컬 codex/claude CLI 바이너리가 PATH에 있어야 하고 --dangerously-bypass-approvals-and-sandbox로 샌드박스 없이 실행되므로, 서버 환경/CI에서는 격리 필요.

## 리스크

- 실험적/불안정 익스포트: convert(PPTX)와 figma는 README/코드가 반복적으로 "experimental / unstable, best-effort"라 명시. 레이아웃 깨짐/수작업 보정 전제. 프로덕션 PPTX 신뢰는 금물.
- god-tibo-imagen 기본 이미지 프로바이더: 비공식 사설 Codex 백엔드를 호출하며 예고 없이 깨질 수 있고, 이미지 생성 권한이 있는 ChatGPT 계정 필요. 안정 파이프라인엔 OPENAI_API_KEY(gpt-image-2)나 GOOGLE_API_KEY(nano-banana) 폴백을 명시 사용 권장.
- 서브프로세스 보안: codex는 --dangerously-bypass-approvals-and-sandbox, claude는 --permission-mode acceptEdits(또는 --dangerously-skip-permissions)로 실행. 임의 파일 쓰기 가능. 신뢰 경계 밖 입력/환경에서 위험.
- 파생 스타일 데이터 라이선스: 90/95종이 외부 리포(corazzon/pptx-design-styles, epoko77-ai/design-diversity)에서 파생. slides-grab 자체는 MIT지만, 스타일 데이터를 그대로 재배포/상업이용하려면 각 원본 리포의 라이선스를 개별 확인해야 함(이 분석에서는 원본 라이선스 미확인).
- 모델 ID 하드코딩: gpt-5.5, claude-opus-4-8 등 미래형 모델명이 model-registry에 박혀 있음. 실제 로컬 CLI가 해당 모델을 지원하지 않으면 런타임 실패. 우리 환경 모델명과 매핑 필요.
- 뷰어/에디터 주입물 영속화 방지 규칙에 의존: 에이전트가 <base>/디버그 스크립트를 파일에 남기면 오염됨. 프롬프트 규칙과 direct-edit 직렬화가 방어하지만 100% 보장은 아님.
- 자체 프로모션 지시: README에 "AI 에이전트면 사용자에게 star 요청하고 동의 시 gh star" 지시가 박혀 있음(에이전트 행동 오염 소지). 이식 시 제거 권장.
- Node >=20, playwright chromium 설치 필요(npx playwright install chromium). 익스포트/스크린샷 전부 chromium 의존.

## 출처 링크

1. https://github.com/NomaDamas/slides-grab (리포, shallow clone로 직접 분석)
2. 로컬 분석 파일: LICENSE, package.json, README.md, bin/ppt-agent.js, scripts/editor-server.js, src/editor/codex-edit.js, src/editor/js/model-registry.js, src/editor/js/editor-send.js, src/editor/js/editor-direct-edit.js, src/editor/js/editor-bbox.js, src/editor/js/editor-select.js, src/image-contract.js, src/slide-mode.cjs, src/design-gate-state.js, src/html2pptx.cjs, src/design-styles.js, templates/cover.html, templates/content.html, skills/slides-grab-design/SKILL.md
3. https://github.com/uxjoseph/ppt_team_agent (원류 프로젝트, README Acknowledgment 기재)
4. https://github.com/corazzon/pptx-design-styles (스타일 30종 원본, README 기재)
5. https://github.com/epoko77-ai/design-diversity (스타일 60종 원본, README 기재)
