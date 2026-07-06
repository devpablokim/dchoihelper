# manim_skill + hyperframes 결합 영상화 파이프라인 리서치

## 개요

3Blue1Brown 스타일 설명용 PNG 정지컷과 영상을 프레젠테이션에 넣는 파이프라인을 목표로 두 리포를 분석했다. 두 리포 모두 실존하며 로컬 clone 후 소스를 직접 읽었다.

- adithya-s-k/manim_skill: 수학 애니메이션 엔진 Manim(CE/GL)을 AI 에이전트에게 가르치는 Claude/에이전트 스킬 모음집. 엔진 자체가 아니라 베스트프랙티스 문서 + 예제 코드 + 테스트로 구성된 "스킬 팩". MIT 라이선스.
- heygen-com/hyperframes: HTML/CSS/미디어 + 시크 가능한 애니메이션을 결정론적 MP4로 렌더하는 오픈소스 영상 프레임워크. HeyGen이 만들었고 사내 프로덕션에서 쓰지만 로컬 CLI 렌더에 HeyGen API/계정이 필요 없다. Apache 2.0 라이선스.

결론: 두 리포는 상호 보완적이며 모두 로컬에서 완전 동작한다. Manim이 3b1b 스타일 수학 컷(PNG 정지 또는 MP4 클립)을 생성하고, hyperframes가 그 산출물을 HTML 컴포지션에 얹어 자막/타이틀/전환/오디오를 붙인 최종 발표용 MP4로 만드는 조합이 성립한다.

## 핵심 발견

### 1. manim_skill 구조 (스킬 팩, 엔진 아님)

- 리포 루트에 skills/ 3개, tests/ 2세트(manimce, manimgl). 각 스킬은 SKILL.md(YAML frontmatter의 name/description로 자동 트리거) + rules/*.md(주제별 가이드) + examples/*.py 구성.
- 스킬 3종:
  - manim-composer: 막연한 아이디어를 scene 단위 계획(scenes.md)으로 변환하는 기획 스킬. description에 "3b1b style", "explain like 3Blue1Brown" 트리거가 명시돼 있다. 코드 작성 전 단계.
  - manimce-best-practices: Manim Community Edition(`from manim import *`, `manim` CLI) 구현 가이드.
  - manimgl-best-practices: ManimGL(3Blue1Brown 원본, `from manimlib import *`, `manimgl` CLI, OpenGL/인터랙티브) 구현 가이드.
- 설치: `npx skills add adithya-s-k/manim_skill` (Anthropic Agent Skills 오픈 표준 준수, Claude Code/Cursor/Copilot 등 호환).
- 참고: 사용자의 현재 환경 MEMORY/스킬 목록에 manim-composer, manimce-best-practices, manimgl-best-practices가 이미 등록돼 있다. 즉 이 스킬 팩은 이미 설치된 상태로 보인다.
- 실제 렌더에는 별도 로컬 설치 필요: Python 3.7+, FFmpeg, LaTeX(TeX Live/MiKTeX/MacTeX), 그리고 `pip install manim`(CE) 또는 `pip install manimgl`(GL). 스킬 리포 자체는 엔진을 번들하지 않는다.

### 2. Manim PNG 정지컷 출력 — 가능 (확인됨)

manimce-best-practices/rules 문서에서 직접 확인:
- `manim -s file.py SceneName` — 마지막 프레임만 PNG로 저장(-s = save last frame). 썸네일/정지컷 표준 방식(cli.md).
- `manim --format png file.py SceneName` — PNG 시퀀스(프레임 연속) 출력(cli.md).
- config.md: `save_last_frame` 설정 플래그, 출력 포맷으로 mp4/gif/mov/webm/png 지원 명시, 출력 경로는 media/images/SceneName.png.
- ManimGL: `manimgl scene.py MyScene -s --skip_animations`로 최종 프레임 이미지 저장(cli.md). `-s`는 마지막 프레임으로 스킵.

즉 프레젠테이션에 넣을 3b1b 스타일 수식/도형 정지 슬라이드를 PNG로 바로 뽑을 수 있다. 애니메이션이 필요하면 MP4/GIF/WebM/PNG시퀀스로 뽑는다.

### 3. hyperframes 정체 — 로컬 HTML→MP4 렌더러 (HeyGen API 비의존)

- 슬로건 "Write HTML. Render video. Built for agents." 컴포지션은 data-* 속성이 붙은 순수 HTML 파일. React/빌드스텝 불필요, index.html이 브라우저에서 그대로 재생됨.
- 렌더 원리: 헤드리스 Chrome(Puppeteer)로 각 프레임을 시크(seek)하며 캡처하고 FFmpeg로 인코딩. 결정론적(같은 입력 → 같은 프레임 → 같은 출력)이라 CI/회귀테스트 친화적. Remotion에서 영감을 받았고 동일하게 headless Chrome + FFmpeg를 쓰나 저작 모델이 React 대신 순수 HTML.
- 애니메이션은 어댑터 방식: GSAP, CSS 애니메이션, Anime.js, WAAPI, Lottie, Three.js, 커스텀 런타임 지원. 시크 가능한(library-clock) 타임라인이 핵심.
- 모노레포 패키지(bun workspaces): core(파서/생성기/린터/런타임/프레임 어댑터), engine(Puppeteer+FFmpeg 캡처 엔진), producer(캡처+인코드+오디오믹스 전체 파이프라인), cli(hyperframes), studio(브라우저 편집 UI), player(임베드 웹컴포넌트), shader-transitions, aws-lambda/gcp-cloud-run(선택적 분산 렌더), sdk.
- CLI 명령: `init`, `preview`, `lint`, `validate`, `inspect`, `render`, `benchmark`, `doctor`, `browser`, `lambda`. 렌더는 `npx hyperframes render ./comp.html -o output.mp4`(MP4 또는 WebM). 비대화형 기본값이라 에이전트 자동화에 적합.
- HeyGen 의존성: 로컬 렌더 경로에는 없음. README가 "HeyGen에서 프로덕션 사용"이라고만 밝히며 hyperframes를 "호스티드 저작 워크플로의 렌더링 코어"로 설명. AWS Lambda/GCP Cloud Run는 선택적 자체 배포 분산 렌더이지 HeyGen 클라우드 호출이 아니다. cloud.ts의 `render`(asset_id/url 제출)는 별도 호스티드 경로로 보이나 로컬 CLI 렌더와 무관하며 필수 아님.
- 스킬 20종을 함께 배포. 라우터 `/hyperframes`(먼저 읽는 인텐트 라우터) + 워크플로 스킬(product-launch-video, website-to-video, faceless-explainer, pr-to-video, slideshow, motion-graphics, music-to-video, general-video, remotion-to-hyperframes 등). 설치 `npx skills add heygen-com/hyperframes`. faceless-explainer, slideshow 스킬이 실제 존재함을 확인.
- 정지 이미지 출력: keyframes 진단 명령에 `--shot out.png`로 렌더된 모션의 단일 프레임을 PNG로 뽑는 경로가 있고, capture 파이프라인은 스크린샷을 다룬다. 다만 주 산출물은 영상(MP4/WebM)이다.

### 4. 결합 영상화 파이프라인 성립 여부 — 성립 (양방향 로컬)

핵심: hyperframes 컴포지션은 표준 HTML이므로 `<img>`, `<video>`, `<audio>` 요소를 그대로 쓴다. Manim이 뽑은 산출물을 미디어로 얹으면 된다.

- 경로 A (정지컷 합성): Manim `-s`/`--format png`로 3b1b 스타일 PNG 컷 생성 → hyperframes HTML의 `<img>`로 배치 → GSAP/CSS로 페이드·줌·팬(켄번스)·자막 애니메이션 부여 → BGM/나레이션 오디오 트랙 추가 → `hyperframes render`로 발표용 MP4. 정지 소스에 모션을 입히는 가장 깔끔한 조합.
- 경로 B (클립 합성): Manim으로 수학 애니메이션을 MP4로 렌더 → hyperframes HTML의 배경 `<video>`로 삽입 → 상단에 타이틀/로어서드/캡션/전환(shader-transitions) 오버레이 → 최종 MP4로 재인코딩. 여러 Manim 클립을 씬 전환으로 이어붙일 때 유용.
- 순수 프레젠테이션(발표 슬라이드덱) 관점: hyperframes slideshow 스킬은 렌더된 영상이 아니라 탐색 가능한 덱(프래그먼트 리빌/분기/핫스팟/프레젠터 모드)을 만든다. Manim PNG를 슬라이드 배경/삽화로 넣고, 영상 필요 구간만 Manim MP4 임베드하는 하이브리드 덱이 가능. 정적 PPT류가 목표라면 Manim PNG를 바로 슬라이드 이미지로 써도 된다(hyperframes 없이도 됨).

## 재사용 가능 자산 (라이선스 명시)

- adithya-s-k/manim_skill — MIT License (Copyright 2026 Adithya S Kolavi). 스킬 문서/예제 코드/베스트프랙티스 자유 재사용·수정·재배포 가능(저작권 고지 유지). 설치: `npx skills add adithya-s-k/manim_skill`.
- heygen-com/hyperframes — Apache License 2.0. 상업적 사용 자유, per-render 수수료 없음, 특허 라이선스 조항 포함. npm 패키지 `hyperframes`(CLI) 및 `@hyperframes/*` 스코프. 설치: `npx skills add heygen-com/hyperframes`, 런타임 `npx hyperframes ...`(Node >=22, bun 모노레포).
- Manim 엔진 자체(스킬 아님, 실행 필수): Manim Community `pip install manim`(MIT), ManimGL `pip install manimgl`(3b1b, MIT). 별도 설치 필요, 리포에 미포함.
- hyperframes producer 번들 폰트: @fontsource(Inter, Montserrat, Oswald, EB Garamond, JetBrains Mono, Space Mono, IBM Plex Mono 등 다수, 대부분 OFL). 슬라이드 타이포에 그대로 활용 가능.
- hyperframes catalog 블록: 애니메이션 차트(data-chart), 전환(flash-through-white 등 shader), 소셜 오버레이 등 `npx hyperframes add <block>`으로 설치.

## 통합 권고 (deck-factory 파이프라인 관점)

1. 기획: manim-composer 스킬로 설명 주제를 scenes.md(씬 단위 계획)로 분해. 3b1b 톤 트리거가 내장돼 있음.
2. 컷 생성: 정지 슬라이드가 목적이면 manimce-best-practices 가이드로 씬을 짜고 `manim -s scene.py SceneName`으로 PNG를 뽑는다. 발표에 모션이 필요한 구간만 `manim -qh scene.py SceneName`으로 MP4를 뽑는다. CE(안정·문서화 우수)를 기본으로 하고, 인터랙티브/고급 3D가 필요하면 ManimGL.
3. 합성/영상화: hyperframes HTML 컴포지션 하나에 Manim PNG(`<img>`)·MP4(`<video>`)·나레이션(`<audio>`)을 배치하고 GSAP 시크 타임라인으로 등장/전환을 잡은 뒤 `hyperframes render -o deck.mp4`. 발표장 재생용 단일 MP4 또는 slideshow 스킬로 탐색형 덱 산출.
4. 로컬 사전조건 스크립트화: FFmpeg + LaTeX(texlive) + Python manim + Node>=22 + Puppeteer용 Chrome. hyperframes는 `npx hyperframes doctor`, `npx hyperframes browser`로 Chrome 설치를 점검·설치한다. LaTeX 미설치 시 Manim의 MathTex가 실패하므로 texlive는 필수.
5. 최소 결합 검증 PoC: Circle/수식 한 컷을 Manim으로 PNG 출력 → 3슬라이드 hyperframes HTML에 임베드 → render로 5초 MP4 뽑기까지 한 번 관통해 두 툴체인의 로컬 설치·버전 궁합을 먼저 확정할 것.
6. 라이선스 안전: MIT + Apache 2.0 조합이라 상업/사내 배포에 제약 낮음. Manim 엔진(MIT)까지 포함해 전 구간 permissive. 산출 영상에 폰트/카탈로그 에셋 라이선스만 개별 확인.

## 리스크

- Manim은 무거운 로컬 의존성을 요구한다. 특히 LaTeX(texlive-full는 수 GB), FFmpeg, Cairo(ARM macOS는 `brew install pkg-config cairo` 별도). ManimGL은 OpenGL/GPU 의존이 커 헤드리스 CI/WSL 환경에서 렌더가 까다로울 수 있다(테스트 병렬시 OOM 경고도 리포에 명시).
- 두 리포 모두 "엔진을 가르치는 스킬"과 "실행 엔진"이 분리돼 있음을 혼동하지 말 것. manim_skill을 설치해도 manim 바이너리는 별도 `pip install`이 필요하고, hyperframes 스킬을 설치해도 렌더에는 Node/Chrome/FFmpeg가 필요하다.
- hyperframes는 Node >=22 및 bun 기반 모노레포로 비교적 신생(버전 0.6~0.7대, 활발히 진화 중). API/CLI 플래그가 바뀔 수 있어 버전 핀 권장.
- hyperframes 시크 애니메이션은 "library-clock"(시크 가능) 패턴을 요구한다. 임의의 wall-clock JS 애니메이션은 프레임 결정론이 깨질 수 있어 GSAP 타임라인 등 지원 어댑터를 써야 한다. Manim MP4를 `<video>`로 넣을 때 프레임 동기화/시크 정확도는 실측 검증 필요.
- 색공간/해상도 정합: Manim 기본 1080p/특정 배경색과 hyperframes 캔버스 해상도·배경을 맞춰야 합성 이음매가 안 생긴다.
- cloud.ts의 호스티드 render 경로와 AWS/GCP 분산 렌더는 로컬 목표엔 불필요. 잘못 물리면 계정/키 요구가 끼어들 수 있으니 로컬 `render` 명령만 쓸 것.
- 접근 실패 소스: 문서 사이트(hyperframes.heygen.com), hyperframes.dev 플레이그라운드는 이번에 직접 fetch하지 않고 리포 내 README/소스로만 검증했다. 세부 CLI 플래그(예: render의 해상도/fps 옵션 전체)는 실제 `hyperframes render --help`로 재확인 권장.

## 출처

1. adithya-s-k/manim_skill 로컬 clone — README.md, LICENSE(MIT), skills/manim-composer/SKILL.md, skills/manimce-best-practices/rules/{cli.md,config.md}, skills/manimgl-best-practices/rules/cli.md
2. heygen-com/hyperframes 로컬 clone — README.md, LICENSE(Apache 2.0), package.json, packages/engine/package.json, packages/producer/package.json, packages/cli/README.md, packages/cli/src/commands/{render.ts,cloud.ts,keyframes.ts}, packages/cli/src/capture/, CLAUDE.md, skills/(faceless-explainer, slideshow 확인)
3. https://github.com/adithya-s-k/manim_skill
4. https://github.com/heygen-com/hyperframes
5. https://docs.manim.community/ (Manim CE 공식 문서, README 링크 — 직접 fetch 안 함)
6. https://hyperframes.heygen.com/introduction (hyperframes 공식 문서, README 링크 — 직접 fetch 안 함)
