# Astryx (astryx.atmeta.com) 조사

## 개요

astryx.atmeta.com은 Meta가 만든 오픈소스 디자인 시스템 "Astryx"의 공식 사이트다. atmeta.com은 Meta 소유 도메인이며, 페이지 하단 저작권은 "©2026 Meta Platforms, Inc.", 배포처는 opensource.fb.com(Meta Open Source), 소스 리포는 github.com/facebook/astryx다. 내부 코드명은 XDS(패키지 displayName "XDS Core", CLI 별칭 xds)로 보인다.

정체는 명확히 "디자인 시스템"이다. 단순 에셋 라이브러리나 SaaS 도구가 아니라, React 컴포넌트 라이브러리 + 디자인 토큰/테마 + CLI + 문서 + 템플릿을 묶은 풀 디자인 시스템이며, 핵심 차별점으로 "agent ready"(AI 에이전트가 소비하도록 설계)를 내세운다. 기술 스택은 React + StyleX(Meta의 atomic CSS-in-JS). 현재 상태는 Beta(core/cli 버전 0.1.2), 사이트 og 설명은 "An open source design system that is fully customizable and agent ready." 블로그 "Introducing Astryx by Meta" 발행일 2026-06-18 기준으로 최근 공개된 신규 프로젝트다.

## 핵심 발견

- 제공물 4축: (1) 150개 이상 컴포넌트(접근성·테마·다크모드 내장), (2) 프로덕션용 페이지 템플릿(대시보드/설정/폼/AI 챗/체크아웃 등), (3) 테마 시스템(디자인 토큰을 CSS custom properties로 제공), (4) CLI + MCP 서버(사람과 AI 에이전트가 동일 API로 문서/토큰/템플릿 접근).
- 라이선스: MIT. GitHub LICENSE 파일 원문 확인 "MIT License / Copyright (c) 2026 Meta Platforms, Inc." core package.json도 "license": "MIT". 즉 코드/컴포넌트/토큰은 자유롭게 사용·수정·재배포·상업적 이용 가능(고지 유지 조건).
- npm 패키지(스코프 @astryxdesign): @astryxdesign/core(컴포넌트+테마 시스템), @astryxdesign/cli, @astryxdesign/build(StyleX 소스 빌드 플러그인), 테마 7종 @astryxdesign/theme-{neutral, butter, chocolate, gothic(다크 전용), matcha, stone, y2k}.
- 설치: `npm install @astryxdesign/core @astryxdesign/theme-neutral @astryxdesign/cli` 후 `npx astryx init`. 전역 CSS에 `@astryxdesign/core/reset.css`, `@astryxdesign/core/astryx.css`, 테마 CSS를 import. 컴포넌트는 서브패스 임포트(`@astryxdesign/core/Button`).
- CLI(@astryxdesign/cli, v0.1.2)가 시스템의 1차 인터페이스. 명령: init, component, search, docs, template, hook, swizzle(컴포넌트 소스를 프로젝트로 복사), upgrade(버전 마이그레이션 codemod), theme build, discover, doctor. 모든 명령이 `--json` 타입드 envelope과 `--dense`(AI 토큰 절약 포맷) 지원. 프로그래매틱 API(@astryxdesign/cli/api)도 노출.
- AI/에이전트 통합이 핵심 셀링포인트: `npx astryx init --features agents`로 CLAUDE.md / AGENTS.md / .cursorrules 생성. 안정적 error code(ERR_* 접두)와 capability manifest(OpenAPI 유사 자기기술 매니페스트) 제공.
- 공식 MCP 서버 제공: URL 타입 `https://astryx.atmeta.com/mcp`. 도구 2개 노출 — search(query)로 컴포넌트/문서/템플릿 검색, get(name)으로 props·사용법·예제 포함 전체 문서 조회. Claude Desktop/Cursor/Windsurf/Cline 등 MCP 호환 툴에 바로 등록 가능.
- 다운로드/API 가능 여부: 가능. (a) npm 공개 패키지, (b) GitHub 공개 리포 git clone(예제 앱 apps/example-nextjs 등 5종 포함), (c) CLI JSON API, (d) MCP 서버, (e) 사이트 sitemap.xml/각 컴포넌트 문서 페이지 공개.
- "Astryx powers over 13,000 apps" "Meta 내부에서 8년간 성장" 주장(마케팅 카피). GitHub 스타 약 3.3k(WebFetch 시점 추정치).
- 마스코트: Astracat(우주비행사 헬멧 쓴 고양이). 마케팅/제품 이미지는 lookaside.facebook.com/assets/astryx/ 에서 서빙(Meta CDN).
- 커뮤니티/소셜: Discord(discord.com/invite/XnsUcFykEP), Facebook/Instagram/Threads/X 모두 @astryxdesign.

## 재사용 가능 자산 (라이선스 명시)

- 코드 전체(컴포넌트 소스, 토큰, 테마 CSS, CLI, 예제 앱): MIT 라이선스. 상업적 사용·수정·재배포 자유, 저작권/라이선스 고지만 유지. 리포 github.com/facebook/astryx, npm @astryxdesign/*.
- 디자인 토큰(spacing/color/radius/typography/shadow/motion/size)이 CSS custom properties로 제공됨 → 테마 CSS 파일만 떼어 순수 HTML/CSS 프로젝트에서도 변수로 활용 가능(MIT). `npx astryx docs tokens`로 전체 레퍼런스 출력.
- 테마 7종(neutral/butter/chocolate/gothic/matcha/stone/y2k) → 팔레트·타이포 프리셋으로 참고/차용 가능(MIT).
- 페이지 템플릿(대시보드/폼/AI챗/체크아웃/설정 등) 및 컴포넌트 예제 코드 → `npx astryx template`, swizzle로 추출(MIT).
- MCP 서버 엔드포인트 https://astryx.atmeta.com/mcp → 에이전트가 디자인 시스템 문서를 직접 조회(무료 공개, 등록만 하면 됨).
- 주의: 마케팅/제품 사진 및 마스코트 Astracat, "Meta"·"Astryx" 로고/브랜드는 lookaside.facebook.com 등에서 서빙되는 Meta 브랜드 자산으로, MIT 코드 라이선스와 별개다. 이미지·상표는 재사용 대상이 아니라고 봐야 안전하다(라이선스 미확인).

## 통합 권고 (deck-factory 파이프라인 관점)

- deck-factory가 HTML 슬라이드를 생성하는 파이프라인이라면, Astryx를 통째로 런타임 의존성으로 넣는 것보다 "디자인 토큰 추출" 방식이 현실적이다. Astryx 컴포넌트는 React + StyleX 빌드 체인을 요구하므로, 정적 HTML 덱에는 무겁다. 테마 CSS의 CSS 변수(색/타이포/스페이싱/라운드)만 뽑아 우리 슬라이드 토큰과 매핑하면 프레임워크 종속 없이 룩앤필을 차용할 수 있다(MIT).
- 우리 저장소에는 이미 design-* 스킬(apple/linear/notion/stripe/vercel)이 디자인 시스템별 토큰 접근을 하고 있다. Astryx 테마 7종을 같은 방식으로 "토큰 프리셋"으로 증류해 신규 design-astryx 후보로 검토할 수 있다. 단 Astryx는 제품 UI(대시보드/체크아웃/챗) 지향이라 프레젠테이션 덱보다는 앱 화면 톤에 가깝다는 점 감안.
- React 기반 산출물을 만드는 경로가 있다면, `npx astryx init --features agents`로 AGENTS.md/CLAUDE.md를 생성해 에이전트가 정확한 import 경로·props를 쓰게 하고, MCP 서버(https://astryx.atmeta.com/mcp)를 등록하면 컴포넌트 문서를 실시간 조회할 수 있다. 이건 "에이전트가 UI 코드를 정확히 뽑는" 우리 워크플로에 바로 이식 가능한 패턴이다.
- 벤치마크 가치: CLI의 --json 타입드 envelope + 안정 error code + capability manifest + --dense 포맷은 "에이전트가 소비하는 CLI" 설계의 좋은 레퍼런스. 우리 자체 툴/스킬의 에이전트 친화 출력 설계에 참고할 만하다.

## 리스크

- Beta 단계(core/cli 0.1.2). upgrade codemod과 append-only error code 체계가 존재한다는 것 자체가 API 파괴적 변경을 전제한다. 프로덕션 고정 의존 시 버전 락 필요.
- StyleX(atomic CSS-in-JS) 및 @astryxdesign/build 빌드 플러그인 종속. 순수 HTML/정적 덱 파이프라인엔 통합 비용이 크다. React 렌더 경로가 없으면 컴포넌트 직접 사용은 부적합.
- 코드는 MIT지만 마케팅 이미지·마스코트(Astracat)·Meta/Astryx 로고는 브랜드/상표 자산으로 라이선스가 확인되지 않음. 이미지 직접 차용 금지 권장.
- "13,000 apps" "8년" 등은 검증되지 않은 마케팅 카피(1차 출처는 자사 블로그뿐). 도입 근거로 인용 시 주의.
- MCP 서버는 Meta 호스팅 외부 엔드포인트라 가용성/레이트리밋/변경이 Meta 통제 하에 있음. 파이프라인이 여기에 하드 의존하면 외부 장애에 노출.
- 신규 공개(2026-06) 프로젝트로 생태계·서드파티 검증이 얕다. 장기 유지보수 보장 미확인.

## 출처 링크

1. https://astryx.atmeta.com/ — 홈(정체·기능 개요, og 메타)
2. https://astryx.atmeta.com/docs/getting-started — 설치·패키지·테마·예제 앱
3. https://astryx.atmeta.com/docs/cli — CLI 명령/JSON API/error code/manifest/doctor
4. https://astryx.atmeta.com/docs/working-with-ai — 에이전트 docs, MCP 서버 설정, --dense
5. https://github.com/facebook/astryx — 소스 리포(설명·스타·패키지)
6. https://raw.githubusercontent.com/facebook/astryx/main/LICENSE — MIT 라이선스 원문
7. https://raw.githubusercontent.com/facebook/astryx/main/packages/core/package.json — @astryxdesign/core v0.1.2, license MIT
8. https://astryx.atmeta.com/blog/introducing-astryx — 소개 블로그(2026-06-18)
9. https://astryx.atmeta.com/blog/how-astryx-works — 아키텍처 설명(2026-06-29)
10. https://astryx.atmeta.com/mcp — 공식 MCP 서버 엔드포인트
11. https://opensource.fb.com/ — Meta Open Source(배포 주체)
