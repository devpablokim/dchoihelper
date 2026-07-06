# Claude 스킬 레이어드 아키텍처 베스트 프랙티스

## 개요

anthropics/skills 공식 리포를 clone(shallow)해서 20개 스킬의 실제 파일 구조를 직접 분석했다. 특히 문서 생성/디자인 계열(pptx, docx, xlsx, pdf, theme-factory, brand-guidelines, canvas-design, frontend-design)과 메타 스킬(skill-creator)을 대상으로 SKILL.md 구성, progressive disclosure(references 분리), scripts 활용, 스킬 간 조합, 서브에이전트+파일 핸드오프 패턴을 확인했다. 추가로 Anthropic 엔지니어링 블로그(Agent Skills)에서 progressive disclosure 3레벨과 컨텍스트 예산 원칙을 대조 확인했다.

리포에는 "디자인토큰 → 에셋 생성기 → 조립기" 3층 스택에 그대로 매핑되는 실물 예제가 존재한다. 토큰층은 theme-factory / brand-guidelines, 에셋 생성기층은 canvas-design, 조립기층은 pptx가 각각 표본이 된다. 아래 권고 구조는 이 3개 스킬의 실제 구현을 근거로 도출했다.

## 핵심 발견

### 1. 공통 스킬 해부 구조 (skill-creator가 규정한 정본)

```
skill-name/
├── SKILL.md            (필수: YAML frontmatter[name, description] + 마크다운 본문)
├── scripts/            (결정적/반복 작업용 실행 코드 - 컨텍스트에 로드 안 하고 실행만)
├── references/         (필요할 때만 컨텍스트로 읽어들이는 문서)
├── assets/             (산출물에 들어가는 파일: 템플릿, 아이콘, 폰트)
└── agents/             (선택: 서브에이전트에게 넘길 지시서)
```

Progressive disclosure는 3레벨 로딩 시스템으로 규정됨:
- 레벨1 메타데이터(name+description): 항상 시스템 프롬프트에 상주(~100단어). 트리거 판단용.
- 레벨2 SKILL.md 본문: 스킬이 트리거되면 로드(이상적으로 500줄 미만).
- 레벨3+ 번들 리소스: 필요할 때만. 스크립트는 컨텍스트에 로드하지 않고 실행만 하므로 사실상 무한.

명시된 규칙(skill-creator SKILL.md 원문):
- "SKILL.md를 500줄 미만으로 유지하고, 한계에 접근하면 계층을 하나 더 추가하고 다음에 어디를 읽어야 하는지 명확한 포인터를 넣어라."
- "reference 파일은 SKILL.md에서 언제 읽어야 하는지 안내와 함께 명확히 참조하라."
- "큰 reference 파일(>300줄)에는 목차를 포함하라."
- 도메인 조직화: 여러 도메인/프레임워크를 지원하면 variant별로 references/{aws,gcp,azure}.md로 쪼개고 SKILL.md는 워크플로+선택 로직만. Claude는 관련 reference 하나만 읽는다.

### 2. 조립기(assembler) 표본 = pptx

- SKILL.md는 얇은 라우터. 상단에 Quick Reference 표(작업→가이드 매핑)를 두고 "Read/analyze는 markitdown, Edit은 editing.md 읽어라, Scratch 제작은 pptxgenjs.md 읽어라"로 분기만 한다.
- 실제 상세 워크플로는 references로 분리: editing.md(205줄, 템플릿 언팩→편집→clean→pack), pptxgenjs.md(420줄, 제로베이스 제작 튜토리얼). 두 경로는 상호배타적이라 한 번에 하나만 로드됨(컨텍스트 절약).
- scripts/가 무겁다: office/unpack.py, office/pack.py, office/validate.py(ISO-IEC29500 XSD 스키마 전체 번들 대조 검증), thumbnail.py, add_slide.py, clean.py. 즉 결정적이고 반복적인 XML 조작/검증은 전부 스크립트로 내려서 토큰 생성 대신 코드 실행으로 처리.
- QA 섹션이 강제 규정으로 존재: "문제가 있다고 가정하고 버그 헌트하라. 첫 렌더는 거의 항상 틀리다." 시각 검수는 반드시 서브에이전트에게 시킬 것("USE SUBAGENTS — even for 2-3 slides. 너는 코드를 계속 봐서 있는 그대로가 아니라 기대한 것을 본다. 서브에이전트는 신선한 눈을 가진다"). 슬라이드를 이미지로 변환(soffice→pdf→pdftoppm) 후 고정된 검수 프롬프트로 겹침/오버플로/저대비 등을 점검하고, fix→re-verify 루프를 최소 1회 완주하기 전엔 성공 선언 금지.

### 3. 디자인 토큰(design-token) 표본 = theme-factory / brand-guidelines

- theme-factory: SKILL.md(워크플로+테마 목록)만 얇게 두고, 실제 토큰은 themes/*.md 10개 파일로 분리. 각 토큰 파일은 ~20줄로 매우 작다(예: tech-innovation.md = 컬러 4종 HEX + 헤더/본문 폰트 페어 + "Best Used For" 용도 힌트). Claude는 사용자가 고른 테마 파일 하나만 읽는다 — 전형적 progressive disclosure. 프리셋에 없으면 즉석 커스텀 테마를 같은 형식으로 생성 후 리뷰받고 적용하는 경로도 규정.
- brand-guidelines: 번들 파일 없이 SKILL.md 한 장으로 컬러(Main/Accent HEX)+타이포(Poppins/Lora, Arial/Georgia 폴백)+적용 규칙(24pt+는 헤딩 폰트, 셰이프는 accent 순환)만. 순수 "포스트 프로세싱 스타일러" 성격 — 이미 만든 아티팩트에 브랜드 룩을 덧입힘.
- 관찰: 토큰층은 SKILL.md 본문이 짧고, 토큰 자체는 (a) 소형 데이터 파일로 분리하거나(theme-factory) (b) 아예 본문에 인라인(brand-guidelines)한다. 스크립트가 거의 없다 — 토큰은 데이터이지 로직이 아니기 때문.

### 4. 에셋 생성기(asset-generator) 표본 = canvas-design

- 명시적 2단계 파이프라인: (1) Design Philosophy 생성(.md 산출) → (2) 그 철학을 캔버스에 시각적으로 표현(.pdf/.png 산출). 중간 산출물(.md 철학 파일)을 디스크에 남겨 다음 단계가 소비하는 파일 핸드오프 구조.
- assets/에 해당하는 canvas-fonts/ 디렉토리에 실제 폰트 TTF 40여 종 + 각 폰트의 OFL 라이선스 텍스트를 번들. 산출물에 직접 들어가는 자산이라 assets 계열.
- 생성 로직 자체는 프롬프트(디자인 지침)로 유도하되 폰트/렌더링은 파일 자산에 의존.

### 5. 스킬 간 의존/조합 패턴 (가장 중요한 발견)

- 공식 스킬들은 서로를 하드코딩으로 호출하지 않는다. 20개 SKILL.md 전수 grep 결과, 한 스킬이 다른 스킬 이름을 명시적으로 invoke하는 사례는 사실상 없다(유일한 약한 언급: web-artifacts-builder가 "available tools including other Skills"라고 두루뭉술하게 지칭). theme-factory가 만든 토큰을 pptx가 소비하지만, pptx SKILL.md는 theme-factory를 언급조차 안 한다.
- 조합은 오케스트레이터(Claude 본체) 레벨에서 일어난다. Claude가 상황 보고 theme-factory를 트리거해 토큰을 고르고, 이어서 pptx를 트리거해 덱을 조립한다. 스킬끼리의 결합은 "import"가 아니라 "모델의 판단 + 공유 파일시스템 아티팩트"를 통해 이뤄진다 — 느슨한 결합(loose coupling).
- 결정적 시사점: 레이어 분리 스킬을 만들 때 "스킬 A가 스킬 B를 부른다"는 강결합 메커니즘에 의존하지 말 것. 대신 각 층을 독립 트리거 가능하게 만들고, 층 사이는 디스크의 파일(토큰 JSON, 에셋 PNG, 매니페스트)로 넘기는 게 공식 리포의 실제 관행이다.

### 6. 공유 substrate: DRY보다 자기완결성 우선

- docx / pptx / xlsx 각각이 scripts/office/(pack/unpack/validate + 전체 XSD 스키마 세트 + validators/)를 자기 폴더에 통째로 복제 보유. 공유 라이브러리로 빼지 않고 의도적으로 중복.
- Anthropic의 선택: 스킬은 자기완결(self-contained) 폴더여야 한다는 원칙이 DRY보다 우선. 각 스킬을 독립적으로 설치/이식 가능하게 유지하기 위한 트레이드오프. 레이어 스택에서도 층 간 공유 유틸은 "복제해서 각 층에 넣기"가 이식성 면에서 안전하다(단, 유지보수 부담은 감수).

### 7. 서브에이전트 + 파일 핸드오프 정본 = skill-creator

- 병렬 팬아웃: 각 테스트 케이스마다 서브에이전트 2개(스킬 있는 런 + 베이스라인)를 같은 턴에 동시 스폰. "나중에 베이스라인 따로 돌리지 말고 한 번에 다 띄워라"(동시 완료 유도).
- 역할 분리 지시서(agents/): 서브에이전트를 스폰할 때 agents/grader.md, agents/analyzer.md, agents/comparator.md를 읽혀서 역할을 부여. 즉 서브에이전트 지시서를 스킬에 번들.
- 파일 기반 스키마 락 핸드오프: 각 런은 결과를 run 디렉토리에 파일로 저장. grader가 grading.json 생성(필드 text/passed/evidence는 뷰어가 의존하므로 정확히 그 이름이어야 함 — load-bearing), 집계는 benchmark.json/benchmark.md, 버전 진행은 history.json, 타이밍은 timing.json(서브에이전트 완료 시 받는 total_tokens/duration_ms 즉시 저장). references/schemas.md가 이 JSON 계약을 문서화.
- 컨텍스트 예산 관점: 큰 파이프라인(평가 N개 × 2런 × 채점 × 집계)을 서브에이전트로 쪼개 각자 자기 컨텍스트에서 돌리고, 메인은 요약 JSON만 받는다. total_tokens를 런별로 기록해 비용을 가시화.
- "반복 작업 발견 시 스크립트화": 여러 테스트 서브에이전트가 매번 비슷한 헬퍼 스크립트(create_docx.py 등)를 독립적으로 작성하면, 그게 스킬이 그 스크립트를 번들해야 한다는 강한 신호. 한 번 써서 scripts/에 넣고 스킬이 쓰게 하라 → 모든 미래 호출이 바퀴 재발명을 안 함.

### 8. 컨텍스트 예산 원칙 (블로그 대조)

- 메타데이터는 항상 상주하므로 description을 타이트하게. 트리거 판단만 되면 됨.
- "상호배타적이거나 함께 거의 안 쓰이는 컨텍스트는 경로를 분리하면 토큰 사용이 준다"(pptx의 editing vs pptxgenjs 분기가 실증).
- 스크립트 실행은 결정적 신뢰성 + 저비용: "리스트 정렬을 토큰 생성으로 하는 건 정렬 알고리즘 실행보다 훨씬 비싸다."
- 파일시스템+코드실행이 있으면 번들 컨텍스트는 사실상 무한 — 전부 컨텍스트에 로드하지 않기 때문.

## 우리 3층 스택 권고 구조 (디자인토큰 → 에셋 생성기 → 조립기)

핵심 설계 원칙: 세 층을 독립 트리거 가능한 자기완결 스킬로 만들고, 층 사이는 디스크 파일(스키마 락된 매니페스트/토큰 JSON/에셋 PNG)로 핸드오프한다. 스킬끼리 하드 호출하지 않는다.

### Layer 1 — deck-tokens (디자인 토큰)
- 표본: theme-factory + brand-guidelines.
- 구조: 얇은 SKILL.md(선택 워크플로 + 토큰 목록) + tokens/{theme}.json|md 소형 파일들. 큰 프리셋 라이브러리는 파일당 하나로 쪼개서 선택된 것만 읽게(progressive disclosure).
- 산출: 디스크에 tokens.json 하나(팔레트 HEX, 폰트 페어, 스페이싱 스케일, 모션 등). 이게 다음 층의 입력 계약.
- 스크립트: 거의 불필요(토큰=데이터). 있다면 대비비율/접근성 검증기 정도.

### Layer 2 — deck-assets (에셋 생성기)
- 표본: canvas-design(2단계 파일 핸드오프) + 우리 codex-imagegen(배치 스폰 회수).
- 구조: SKILL.md는 라우터. references/에 에셋 종류별 지침(차트, 히어로 이미지, 아이콘, 배경). scripts/에 결정적 생성기(SVG/차트 렌더, 이미지 후처리). assets/에 폰트 등 산출물 자재.
- 입력: Layer1의 tokens.json을 읽어 팔레트/폰트를 강제 적용.
- 산출: assets/ 디렉토리에 PNG/SVG + assets-manifest.json(각 에셋의 id, 경로, 종류, 소스 토큰, 치수). 대량 생성은 서브에이전트/코덱스 병렬 스폰으로 팬아웃, 파일로 회수(레이스 방지 = 작업별 디렉토리 격리).
- QA: 생성 에셋도 서브에이전트 시각 검수(신선한 눈).

### Layer 3 — deck-assembler (조립기)
- 표본: pptx.
- 구조: 얇은 SKILL.md 라우터 + Quick Reference 표. references를 상호배타 경로로 분리(예: 템플릿 기반 editing.md vs 제로베이스 build.md). scripts/에 pack/validate/thumbnail 등 결정적 조작.
- 입력: tokens.json + assets-manifest.json을 읽어 배치. 토큰으로 스타일, 매니페스트로 에셋 참조.
- 산출: 최종 덱(.pptx/.pdf/.html) + 콘텐츠 QA(markitdown grep로 placeholder 잔존 검사) + 시각 QA(soffice→pdftoppm→서브에이전트 검수, fix/re-verify 루프 최소 1회).

### 오케스트레이션 층 (선택, 얇게)
- 세 층을 순서대로 태우는 로직은 별도 얇은 "deck-factory" 오케스트레이터 스킬이나 /plan 워크플로에 둔다. 이 층은 각 스킬을 트리거하고 파일 경로만 이어준다 — 스킬 내부에 다른 스킬 호출을 박아넣지 않는다.
- 층 간 계약(tokens.json, assets-manifest.json 스키마)은 skill-creator처럼 references/schemas.md 한 곳에 문서화하고 필드명을 load-bearing으로 고정.

### 패키징
- marketplace.json 방식으로 3개 스킬 + 오케스트레이터를 한 플러그인(deck-factory)으로 묶어 배포 가능. 각 스킬은 자기완결 폴더 유지.

## 재사용 가능 자산 (라이선스 명시)

- anthropics/skills 리포 전체 — GitHub github.com/anthropics/skills. 스킬별 라이선스 혼재.
  - Apache License 2.0 (개방, 상업 이용/수정 가능, 출처표기): theme-factory, brand-guidelines, canvas-design, skill-creator, algorithmic-art, frontend-design, internal-comms, mcp-builder, slack-gif-creator, web-artifacts-builder, webapp-testing, claude-api. 각 폴더 LICENSE.txt에 Apache 2.0 전문.
  - Proprietary / source-available (© 2025 Anthropic, PBC. All rights reserved. 참조/학습용, 재배포·상업 재사용 제한): docx, pptx, xlsx, pdf. 각 폴더 LICENSE.txt에 "Proprietary. LICENSE.txt has complete terms". 구조 패턴은 참고하되 코드 그대로 재배포는 불가로 취급.
- canvas-design/canvas-fonts/ — 폰트 TTF 40여 종, 전부 SIL Open Font License 1.1(OFL). 각 폰트 옆 *-OFL.txt에 저작권/라이선스. 임베드/배포 가능(OFL 조건 준수: 폰트 자체 판매 금지, 예약명 규칙). 우리 에셋 생성기 assets/폰트로 그대로 채용 가능한 후보(예: Outfit, Geist Mono, Instrument Sans/Serif, Bricolage Grotesque, Work Sans, Lora, IBM Plex 계열).
- theme-factory/themes/*.md — 10개 프리셋 토큰(컬러 HEX + 폰트 페어 + 용도). Apache 2.0. 우리 tokens 스키마의 출발 템플릿으로 재사용/개조 가능.
- pptx SKILL.md의 컬러 팔레트 표(Midnight Executive 등 10종)와 폰트 페어링 표, 시각 QA 검수 프롬프트 — Proprietary 스킬 소속이라 문구 그대로 복붙 재배포는 지양하되, 팔레트 HEX값/QA 체크리스트 아이디어는 자체 재작성해 채용.
- skill-creator/references/schemas.md의 JSON 계약 패턴(evals/grading/history/benchmark) — Apache 2.0. 우리 층간 매니페스트 스키마 문서화 방식의 참고 템플릿.

## 통합 권고 (우리 파이프라인에 붙이는 법)

- 3층을 각각 독립 스킬로 만들고 층간은 파일 핸드오프(tokens.json → assets-manifest.json → 최종 덱)로 결합. 스킬 상호 하드 호출 금지 — 공식 리포의 실제 관행과 일치.
- 각 SKILL.md는 500줄 미만 라우터로 유지, 상세는 references/로 분리하고 "언제 읽는지" 포인터 명시. 300줄 넘는 reference엔 목차.
- 결정적/반복 작업(팔레트 검증, SVG/차트 렌더, 덱 pack/validate)은 전부 scripts/로 내려 토큰 대신 코드 실행. 여러 실행이 같은 헬퍼를 재작성하면 그걸 스크립트로 승격.
- 대량 에셋 생성은 서브에이전트/코덱스 병렬 스폰(우리 codex-imagegen/codex-spawn 자산 활용), 작업별 디렉토리 격리로 레이스 방지, 파일로 회수. 이게 컨텍스트 예산을 지키는 핵심 — 메인은 매니페스트 요약만 받는다.
- 층간 계약 스키마(필드명 load-bearing)를 references/schemas.md 한 곳에 고정하고 QA 스크립트가 그 스키마로 검증.
- 최종 조립 후 서브에이전트 시각 QA를 강제(pptx 패턴 이식): 이미지 변환 → 신선한 눈 검수 → fix/re-verify 루프 최소 1회.
- 폰트는 canvas-design의 OFL 폰트를 assets/에 번들해 이식성 확보(외부 CDN 의존 제거). 특히 Artifact/HTML 덱은 CSP상 외부 폰트 불가라 임베드 필수.

## 리스크

- Proprietary 스킬(docx/pptx/xlsx/pdf) 코드/프롬프트 문구를 그대로 복사해 재배포하면 라이선스 위반 소지. 구조 패턴만 참고하고 문구는 자체 재작성할 것. Apache 2.0 스킬은 출처표기하에 재사용 가능.
- 자기완결성 원칙(scripts/office 복제)을 따르면 층간 공유 유틸이 중복되어 유지보수 부담 증가. DRY와 이식성의 트레이드오프를 의식적으로 선택해야 함.
- 느슨한 결합은 오케스트레이터(Claude)의 판단에 의존 → 층 순서가 자동 보장되지 않음. 매니페스트 존재/스키마 검증을 각 층 진입 시 강제(가드)해 순서 오류를 조기 실패시킬 것.
- 매니페스트 필드명이 load-bearing인데 문서화가 흩어지면 뷰어/조립기가 조용히 깨진다(skill-creator가 grading.json 필드명 경고로 명시한 실제 함정). 스키마를 단일 소스로.
- progressive disclosure 남용 위험: reference를 과하게 쪼개면 모델이 필요한 파일을 안 읽고 넘어갈 수 있음. SKILL.md에 "언제 무엇을 읽어라"를 분명히 써야 함.
- 공식 리포는 스냅샷(shallow clone, 2026-07 시점)이며 향후 구조/라이선스가 바뀔 수 있음. 재사용 전 원본 LICENSE 재확인 필요.
- Agent Skills 스펙 원문은 리포 spec 폴더에 없고 agentskills.io/specification로 외부 이동됨(리포엔 3줄 포인터만). 스펙 세부는 외부 문서를 별도 확인해야 함.

## 출처 링크

1. anthropics/skills GitHub 리포 (shallow clone, 로컬 분석): https://github.com/anthropics/skills
2. skills/pptx/SKILL.md, editing.md, pptxgenjs.md, scripts/office/ (조립기 표본; Proprietary LICENSE.txt)
3. skills/theme-factory/SKILL.md, themes/*.md (디자인 토큰 표본; Apache 2.0)
4. skills/brand-guidelines/SKILL.md (토큰/스타일러 표본; Apache 2.0)
5. skills/canvas-design/SKILL.md, canvas-fonts/ (에셋 생성기 표본; Apache 2.0, 폰트 OFL 1.1)
6. skills/skill-creator/SKILL.md, references/schemas.md, agents/*.md, scripts/ (서브에이전트+파일 핸드오프 정본; Apache 2.0)
7. .claude-plugin/marketplace.json (플러그인 패키징: document-skills / example-skills / claude-api)
8. spec/agent-skills-spec.md → 외부 이동: https://agentskills.io/specification
9. Anthropic Engineering, "Equipping agents for the real world with Agent Skills": https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
10. Anthropic 지원 문서, skill 생성 가이드: https://support.claude.com/en/articles/12512198-creating-custom-skills
