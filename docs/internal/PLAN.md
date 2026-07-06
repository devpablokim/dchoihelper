# deck-factory 마스터플랜

웰메이드 프레젠테이션 자동 생성 파이프라인.
HTML/CSS 기반, 발표장에서 작은 글씨가 나오지 않는 덱과 그 안의 글을 만든다.
품질 주장은 실측 가능한 두 프로토콜로 한정한다 —
상용 도구(Gamma, Beautiful.ai)와의 블라인드 동급 비교,
그리고 MBB 스타일 체크리스트 기반 블라인드 평가 (둘 다 6절 Phase 5).
"맥킨지급"이라는 절대 주장은 하지 않는다 — 실물 MBB 덱은 조달 불가라 직접 실측할 수 없기 때문이다 (P8).

작성일: 2026-07-03
근거 리서치: /home/seunghyeong/deck-factory/research/ 하위 10개 문서 (본문 각주 번호는 문서 말미 출처 목록 참조)


## 1. 비전과 최종 산출물 정의

### 1.1 비전

한 문장의 브리프에서 시작해,
디자인 토큰이 강제된 HTML 슬라이드 덱과 그 안의 카피, 차트, 이미지, 3b1b 스타일 컷까지
자동 생성하고 기계 채점기로 합격시킨 뒤 사람이 비주얼 에디터로 마감하는 공장.

각 스킬은 레이어로 분리되어 단독 사용이 가능하고,
조합은 파일 핸드오프로만 일어난다. 통짜 금지.

### 1.2 최종 산출물 물리 스펙

이 절의 좌표계·치수·폰트 하한 수치의 기계 판독 정본은 deck-contracts의 deck-constants.json(2.3) 한 파일이다.
아래 서술은 사람용 복사본이며, grader.yaml 기본값·slide-mode.cjs 이식본·capacity 역산 스크립트는
전부 그 파일을 소비한다 (동기화 방식은 2.3 계약 참조). 수치가 어긋나면 CI diff가 실패한다.

- 슬라이드 단위: 자체 완결형 HTML 파일 1장 = slide-NN.html
  (slides-grab 계약 계승 [4], 파일 구조·필수 속성은 2.3의 슬라이드 HTML 산출물 계약으로 고정)
- 종횡비: 16:9 고정. 저작 해상도 1280x720 CSS px 기준 (slides-grab의 720pt x 405pt / 960x540 좌표계와 호환 매핑 유지)
- 스케일링: reveal.js 계열의 "고정 해상도 저작 + transform: scale 비율 유지 축소" 패턴을
  프레임워크 도입 없이 뷰어 레이어에 직접 구현 [6].
  이것이 막는 것은 뷰포트 축소로 글씨가 작아지는 실패모드다.
  저작 시점에 작은 폰트가 지정되는 실패모드는 별개이며,
  레이아웃 템플릿(자유 CSS 금지, P2)과 grader hard fail(5.3)의 이중층이 막는다.
- 폰트 하한 (기본값, grader 설정 YAML로 오버라이드 가능 [7]):
  - 본문 24pt 이상 (720p 기준 32px). 미만이면 hard fail
  - 액션 타이틀 36pt 이상 권장, 하한 28pt
  - 캡션/출처/페이지번호 18pt 이상, 12pt 미만 hard fail
  - 슬라이드당 폰트 크기 종류 3종 이하, 폰트 패밀리 2종 이하
  - 절대 하한: 본문 18pt, 캡션 12pt는 grader.yaml 오버라이드로도 내릴 수 없는 바닥값으로
    grader에 고정한다. 오버라이드는 기본값과 절대 하한 사이에서만 허용된다
  - 불변식: 조립기는 어떤 경우에도(콘텐츠 오버플로 포함) 폰트를 토큰 하한 미만으로 축소하지 않는다.
    오버플로는 폰트 축소가 아니라 P7 plan 단계의 결정론적 해소 루프로 처리하며,
    이 루프는 kind별 터미널 — body는 강제 연속 슬라이드 분할,
    해소 불가 kind(title/source)는 releaseBlocked 마킹(2.3 deck-plan/deck-manifest) —
    이라는 항상 성립하는 종료 폴백을 가진다 (P7).
    releaseBlocked 슬라이드가 남은 덱은 final 익스포트가 차단되고 draft로만 나간다 (P7 익스포트 게이트)
- 서체 정책 (자산 계약과 정합):
  - 기본 서체: Pretendard (OFL) [3][4]. ./assets/fonts/ 로컬 번들만 허용.
    CDN 로드는 자산 계약(원격 URL 금지)과 오프라인 발표장 재생 요건에 어긋나므로 금지
  - 캐주얼 톤 보조 서체: 배민 폰트 계열 (OFL 계열). 동일하게 로컬 번들만
  - 이모지: TossFace는 수정 금지 커스텀 라이선스이나,
    원본 그대로의 재배포는 저작권 안내 동봉 조건으로 무료 허용됨이 라이선스 원문으로 확인됐다 [1].
    따라서 ./assets/fonts/에 무수정 원본만 번들하고 LICENSE 고지 파일을 동봉한다.
    수정·재가공·파생 폰트 제작은 금지 (OFL이 아님)
- 텍스트는 시맨틱 태그(h1~h6, p, ul/ol/li) 강제. 이미지에 텍스트 굽기 금지 (WCAG 1.4.5) [10]
- 명암비: 본문 4.5:1, 큰 텍스트(18pt+ 또는 14pt+볼드) 3:1 미만이면 fail (WCAG 2.2) [7][10]
- 자산 계약: 로컬 자산은 ./assets/ 상대경로만 허용, 원격 URL/절대경로 금지 (image-contract 이식) [4].
  폰트 파일도 예외 없이 이 계약을 따르며(./assets/fonts/), grader의 원격 URL 검사 대상에 포함한다
- 익스포트 포맷 (단일 소스 오브 트루스에서 병렬 산출 [6]):
  - 1급: PDF (Playwright page.pdf, 발표/전달용), PNG (슬라이드별, 썸네일/검수용)
  - 2급: 웹 뷰어 — 두 모드를 분리한다.
    folder bundle 모드: viewer.html + slides/ 폴더 구조 (발표장 재생 기본,
    자산은 2.3 assetRoot 정의대로 slides/assets/에 slide-NN.html과 병치),
    single-html inline bundle 모드: 자산을 data URI로 인라인한 자체 완결 1파일 (단일 파일 전달용).
    둘 다 폰트 로컬 번들이라 오프라인 동작
  - 3급(베스트 에포트): PPTX (slides-grab html2pptx 경로, 실험적임을 명시 [4]), MP4 (모션 덱, hyperframes 경유 [5])

### 1.3 품질 목표

- 최종 덱이 자동 채점기(5.3, P8)에서 hard fail 0건, 카테고리 가중합 90점 이상.
  90점은 grader.yaml에 고정된 가중치·규칙별 배점·집계식으로 산출하고,
  레퍼런스 덱 골든셋 캘리브레이션으로 합격선의 대응 근거를 문서화한다 (P8)
- 상업 벤치마크: Gamma/Beautiful.ai 산출물과 블라인드 비교에서 동급 이상.
  조달·블라인드화·루브릭·통과선·판정자 검증을 포함한 프로토콜은 6절 Phase 5에 정의
- MBB 스타일 적합: 실물 MBB 덱은 조달 불가하므로(P8) "맥킨지급"을 직접 실측할 수 없다.
  대신 consulting-quality 리서치에서 도출한 MBB 스타일 체크리스트
  (피라미드 구조의 시각 위계, 액션 타이틀 결론성, MECE, 원 메시지, 타이틀 테스트 [7])를
  앵커드 루브릭으로 고정하고, Phase 5의 블라인드 평가 트랙에서 항목별 통과율을 측정한다.
  결과는 "맥킨지급"이 아니라 "MBB 스타일 체크리스트 통과율 N%"로만 보고한다
- 각 파이프라인 산출물은 단독으로도 상업성 있는 수준.
  이 주장은 5.1의 단독 상업 완성도 게이트(콜드런 품질 바, README/예제, 실패 UX)로 검증한다


## 2. 레이어 아키텍처

anthropics/skills 리포 분석 결과를 정본으로 삼는다 [8].
핵심 원칙 세 가지.

- 각 레이어는 독립 트리거 가능한 자기완결 스킬. 스킬 간 하드 호출 금지.
- 층간 결합은 디스크 파일(스키마 락 매니페스트)로만. 필드명은 load-bearing으로 고정.
- SKILL.md는 500줄 미만 라우터, 상세는 상호배타 references로, 결정적 작업은 scripts로.

### 2.1 레이어 맵

L0 디자인 파운데이션
- deck-tokens: 브리프 → tokens.json (팔레트 역할체계, 폰트 페어, 타입 스케일, 스페이싱, 대비 검증 결과)
- 프리셋: 기존 design-apple/linear/notion/stripe/vercel 5종 재사용 +
  국내 신규 프리셋(토스 원칙 재구성, SEED 구조 차용, KRDS 참조) + Astryx 테마 7종 증류판

L1 에셋 생성기 (병렬, 서로 독립)
- deck-storyline: 브리프 + 원자료 → source-pack.json + claims.json + outline.md
  (소스 수집·주장 정리·내러티브 순서 결정 — deck-copy/deck-charts가 소비하는 상류 단계, P10)
- deck-charts: 데이터 → SVG/PNG 차트·다이어그램 + chart-manifest.json
- deck-motion: 주제 → manim PNG 정지컷 / MP4 클립 + motion-manifest.json
- deck-imagery: 이미지 브리프 → 배경/히어로 PNG(생성기는 provider/model 추상화, 기본 gpt-image-2) + image-manifest.json
- deck-copy: 아웃라인 → 슬라이드별 액션 타이틀 + 본문 카피 (copy.json)
- deck-layouts: tokens.json → 결정론적 레이아웃 템플릿 카탈로그 + layout-manifest.json (L1이지만 L2의 입력 자재)

L2 조립과 검증
- deck-assembler: 두 단계로 분리 —
  plan 단계(비결정 판단 허용): copy.json + 각 매니페스트 + layout-manifest.json을 읽어
  슬라이드→레이아웃→슬롯 바인딩을 만들고,
  수용량 검사와 오버플로 해소(대체 레이아웃 재바인딩, 연속 슬라이드 분할, 카피 반려)를
  이 단계 안에서 전부 끝낸 뒤 최종 deck-plan.json을 산출한다.
  레이아웃 선택, 분할 등 모든 구조 결정은 plan에서만 일어난다.
  compose 단계(결정론): 확정된 deck-plan.json과 입력 파일들을 소비만 하여
  slides/*.html + 뷰어 + 익스포트 산출.
  compose는 어떤 선택도 하지 않으며, 슬라이드 수·layoutId·바인딩을 바꾸지 않는다
- deck-grader: 덱 채점기. 조립기와 오케스트레이터가 서브프로세스로 호출하는 독립 도구 (P8)
- deck-editor: 비주얼 마감 에디터 (slides-grab bbox 편집 아키텍처 이식, P9).
  장기 구동 서버, 비결정 편집, 에이전트 서브프로세스 스폰, 샌드박스 격리를 수반하므로
  조립기와 리포·런타임 프로파일을 분리한다. slides-grab 원본도 edit를 별도 커맨드로 분리한다 [4]

L3 오케스트레이터
- deck-factory: 얇은 라우터 스킬. 각 레이어를 순서대로 트리거하고 파일 경로만 이어준다.
  층 순서 보장은 각 스킬 진입 시 매니페스트 존재/스키마 검증 가드로 조기 실패시킨다 [8].

### 2.2 단독 사용 시나리오 (레이어 독립성 검증 기준)

- deck-tokens만: "발표용 다크 테크 토큰 하나 뽑아줘" — tokens.json만 산출
- deck-storyline만: "이 자료 뭉치로 발표 아웃라인 잡아줘" —
  source-pack.json + claims.json + outline.md만 산출
- deck-layouts만: "이 tokens.json으로 발표 레이아웃 20종 카탈로그 만들어줘" —
  덱 없이 layouts/ + layout-manifest.json만 산출 (theme-factory 유사 단독 산출물)
- deck-charts만: "이 CSV로 ECharts 산키 다이어그램 SVG 뽑아줘" — 토큰 없이 기본 팔레트로 동작
- deck-motion만: "푸리에 변환 3b1b 컷 PNG 3장" — 덱 없이 PNG만 산출
- deck-imagery만: "이 무드로 네거티브 스페이스 확보된 히어로 배경 5장" — 토큰 없이 기본 무드 프리셋으로 동작
- deck-copy만: "이 초안으로 슬라이드 카피 뽑아줘" — copy.json 또는 마크다운 반환.
  layout-manifest.json이 없는 단독 실행에서는
  deck-contracts에 문서화된 기본 보수 수용량 예산으로 린트하는 degrade 경로를 쓴다.
  gn-voice와의 디스패치 경계: 기존 산문을 개인 문체로 다듬는 요청은 gn-voice,
  아웃라인/원문에서 구조화된 copy.json을 생성하는 요청은 deck-copy.
  이 경계를 양쪽 스킬 description에 명기해 "슬라이드 글로 바꿔줘"류 입력의 충돌을 막는다
- deck-assembler만: 사람이 직접 만든 매니페스트와 deck-plan.json으로도 조립 가능.
  오케스트레이터가 없으면 오버플로 반려 단계는 건너뛰고 kind별 터미널 폴백으로 직행 (P7)
- deck-grader만: "이 HTML 덱 채점해줘" —
  생산 경로와 무관하게 임의의 slides/*.html에 grade-report.json 산출
- deck-editor만: "이 슬라이드 HTML에서 이 영역만 고쳐줘" —
  생산 경로와 무관하게 임의의 slides/*.html에 bbox 지정 편집

### 2.3 파일 핸드오프 계약 (스키마 단일 소스)

계약 스키마는 deck-contracts 리포 한 곳에 정의하고
각 레이어 리포는 검증 스크립트를 복제 보유한다 (자기완결성 우선, DRY보다 이식성 [8]).

- deck-constants.json: 좌표계·치수·폰트 하한 상수의 물리적 단일 소스 (정본: deck-contracts).
  canvas{w:1280, h:720},
  coordTransforms: 호환 좌표계 변환 공식의 기계 판독 정의 —
  pt 좌표계(720x405)는 px = pt x PT_TO_PX(16/9), 에디터 bbox 좌표계(960x540)는 px = bbox x 4/3.
  모든 소비처는 이 공식으로만 변환하고 자체 변환 상수 금지,
  assetRoot: 자산 상대경로 기준의 명시적 정의 — ./assets/는 각 슬라이드 HTML 파일 위치 기준
  상대경로로 해석하며(브라우저 의미론 그대로), 덱 패키지 구조는
  slides/slide-NN.html과 slides/assets/를 병치하는 형태로 고정한다.
  viewer folder bundle 모드와 익스포터도 이 기준을 가정하고,
  single-html inline bundle 모드는 data URI 인라인이라 경로 무관 (1.2 익스포트 포맷),
  fontFloors{기본값(본문 24pt/타이틀 28pt/캡션 18pt 등 1.2 전체), absoluteFloors(본문 18pt, 캡션 12pt)},
  capacityMargin(수용량 안전 마진 계수, 기본 0.05).
  1.2의 물리 스펙 수치는 이 파일의 서술적 복사본이며, 기계가 읽는 정본은 이 파일 하나다.
  나머지 소비처가 이 파일을 쓰는 방식도 계약으로 고정한다 —
  (a) grader.yaml의 기본값 섹션은 이 파일에서 sync 스크립트로 생성하고(수기 수정 금지)
      CI가 생성본과 diff 검사 (P8),
  (b) slide-mode.cjs 이식본(P7)은 상수를 하드코딩하지 않고 vendored deck-constants.json을 로드,
  (c) deck-layouts의 capacity 역산 스크립트는 하한 폰트·마진 값을 이 파일에서 읽는다 (P2).
  오버라이드는 grader.yaml에서만, 기본값과 absoluteFloors 사이 범위 규칙(1.2)은 검증 스크립트가 강제
- tokens.json: palette(role 기반 + raw), fonts(pair, fallback, 라이선스 표기), typeScale(pt),
  spacing, contrastPairs(검증된 전경/배경 조합), motion
- outline.md: 덱 아웃라인 (제목만 읽어도 논지가 통해야 함 — titles test [7][10])
- copy.json: slides[].{id, actionTitle, bullets[], claims[], sourceLine, lang, register, rejectAttempt?}
  claims[].{text, sourceRef, confidence}: 슬라이드가 딛는 주장과 출처의 구조화 목록 —
  sourceRef는 claims.json(P10)의 출처 id를 가리키고 P8 신뢰성 규칙과 연결된다.
  sourceLine은 렌더용 요약 문자열로 유지하되 claims에서 파생 생성한다.
  rejectAttempt: 반려 재작성 산출에만 존재 — 소비한 copy-reject.json의 attempt 값을 그대로 에코해
  plan이 몇 번째 재진입분인지 파일만 보고 판별하게 한다 (아래 copy-reject.json 카운터 규약)
- layout-manifest.json: 레이아웃 카탈로그 기술서. 계약명은 이 형태로 고정한다.
  templates[].{id, archetype(cover|section|content|quote|stat|closing), aspectSafe, slots[]}
  slots[].{id, kind(title|body|image|chart|caption|media|table|source), capacity, maxGlyphsHint,
  bbox{x,y,w,h}, splitGranularity(bullet|sentence|paragraph)?, allowLossyTruncate?}
  오버플로 동작은 슬롯별 자유 필드가 아니라 kind별 overflowPolicy로 계약에 고정한다 (스키마가 강제):
  - title: 반려 재작성(copy-reject)만 허용. split·truncate 금지.
    반려 상한 도달 시 releaseBlocked 종료 (아래 copy-reject.json 종료 조건)
  - body: 반려 재작성 후에도 초과면 splitGranularity 경계 연속 슬라이드 분할. truncate 금지
  - source: truncate 금지. 초과 시 반려 재작성만. 반려 상한 도달 시 releaseBlocked 종료 (title과 동일)
  - caption: allowLossyTruncate=true인 슬롯에 한해 손실 truncate 허용 —
    발생 시 deck-plan.json 해당 슬라이드에 truncatedContent 감사 기록 필수
  - image|chart|media|table: 텍스트 오버플로 비대상 (바인딩 게이트가 치수 정합만 검사)
  capacity{budgetPx{hangul, latin}, maxLines}:
  해당 슬롯을 하한 폰트로 렌더했을 때의 실측 advance-width 예산(px)과 행 수 상한.
  글자 수는 비례폭 폰트(Pretendard)에서 렌더 폭을 예측하지 못하므로
  수용량 계약의 단위는 글자 수가 아니라 스크립트별(한글/라틴) 측정 폭이다.
  maxGlyphsHint는 사람이 읽는 근사 힌트로만 두고 어떤 게이트에도 쓰지 않는다.
  capacityFloors{archetype: {kind: capacity}}: 템플릿 archetype별·슬롯 kind별 최소 수용량 요약 —
  전 템플릿 단일 최소값은 가장 작은 슬롯 하나가 전체 카피를 과압축시키므로 쓰지 않는다.
  바인딩 전 단계(deck-copy)는 자기 슬라이드의 archetype 추정에 해당하는 하한만
  보수적 기본 예산으로 소비하고, 실제 fit 확정은 plan 단계가 담당한다.
  kind=media는 정지 이미지와 영상을 모두 수용하는 슬롯으로,
  풀슬라이드 영상 템플릿(video-full)의 바인딩 대상이다.
  스키마 원본은 deck-contracts에 두고 deck-layouts와 deck-assembler가 vendored 사본 + diff CI로 공유
- deck-plan.json: 슬라이드↔레이아웃↔슬롯↔콘텐츠 바인딩의 단일 소스.
  slides[].{id, layoutId, slots{slotId: binding}, needsHumanReview?, rejectCount?, releaseBlocked?, truncatedContent?}
  binding: {contentRef, transform?} 객체.
  transform(이미지/미디어 바인딩 전용): {crop{x,y,w,h}?, objectPosition?, overlay{color,opacity}?} —
  plan 단계의 이미지 재조정(크롭 오프셋, 오버레이)이 파일 계약으로 표현되는 자리다 (P5).
  텍스트/차트 바인딩은 transform 없이 contentRef만 갖는다.
  rejectCount: 해당 슬라이드가 거친 copy-reject 왕복 횟수의 최종 기록 (감사 추적용, 0 또는 생략 가능).
  releaseBlocked: 오버플로 해소에 실패한 슬라이드의 릴리스 차단 마커 (생략 시 false).
  title/source 반려 상한 도달, measured-overflow 재왕복 실패 등 해소 불가 종료가 이 필드를 기록하고,
  deck-manifest.json의 releaseBlocked/exportStatus 집계와 P7 익스포트 게이트가 소비한다 —
  releaseBlocked=true 슬라이드가 하나라도 있으면 final 익스포트가 성립하지 않는다.
  contentRef 형식: "copy:{slideId}.{field}" 또는 "asset:{chart|image|motion}:{assetId}".
  배열 필드 arity 규칙: "copy:{slideId}.bullets"는 kind=body 슬롯에 목록(ul)으로 렌더하고,
  수용량 검사는 전체 불릿의 렌더 폭·행 합산 기준으로 한다.
  분할은 불릿 경계에서만 일어나며 원문 순서를 유지해
  뒤쪽 불릿부터 연속 슬라이드로 이월한다 — compose가 임의 판단할 여지를 없애는 결정론 규칙.
  asset:motion의 풀슬라이드 영상은 kind=media 슬롯에만 바인딩한다.
  차트-출처 페어링 규칙: 수치를 포함하는 chart 자산이 바인딩된 슬라이드는
  같은 슬라이드에 kind=source(또는 caption) 슬롯 바인딩이 반드시 존재해야 하며,
  그 내용은 chart-manifest의 sourceRef가 가리키는 claims/source-pack 항목에서
  파생 생성된 sourceLabel을 쓴다 (sourceRef 강제는 아래 chart 자산 필드 계약).
  이 페어를 plan 산출 시 스키마 수준에서 검증하고 미충족이면 plan이 실패 종료한다 —
  compose가 아니라 plan에서 막아 grader hard fail(출처 라인 부재)의 구조적 원인을 제거한다 (P3/P8).
  생산 주체는 deck-assembler의 plan 단계(단독 사용 시 사람이 직접 작성 가능).
  plan은 수용량 검사와 오버플로 해소를 전부 마친 확정 바인딩만 산출하고,
  해소에 실패한 슬라이드는 releaseBlocked=true로 명시 마킹하므로(P7)
  "해소 완료"와 "해소 실패 마킹" 외의 제3 상태(조용한 미해소)가 존재하지 않는다.
  compose 단계와 그 이후 층은 이 바인딩을 소비만 하고 선택하지 않는다 —
  조립 결정론(P7)은 이 계약 수준에서 보장된다
- copy-reject.json: plan 단계가 수용량 초과 슬라이드를 deck-copy로 반려할 때 쓰는 계약.
  rejects[].{slideId, slotId, capacity, measured, attempt, attemptedLayouts[], reason}
  attempt: 슬라이드당 재진입 카운터 (1부터 시작). 카운터는 이 파일 필드로만 영속하며,
  plan/오케스트레이터의 메모리 상태나 계약 밖 재진입 카운터에 의존하는 것을 금지한다 —
  어느 층이 재시작돼도 파일만 보고 루프 위치가 복원돼야 한다.
  종료 조건 (계약 수준):
  - plan은 반려 산출 시 직전 copy-reject.json의 해당 슬라이드 attempt에 +1 한 값을 기록하고,
    attempt > 2인 rejects 항목은 스키마 검증 실패로 정의한다 (상한 2회가 스키마에 박힌다)
  - deck-copy는 재작성 copy.json에 rejectAttempt로 attempt를 에코한다 (위 copy.json 규약)
  - rejectAttempt=2인 재작성분이 다시 수용량을 초과하면 plan은 반려를 산출할 수 없으므로(스키마 위반)
    kind별 터미널 액션으로 종료한다 — body는 강제 연속 슬라이드 분할,
    title/source는 분할·truncate 금지 kind이므로 카피는 그대로 두되 해소 실패로 확정하고
    deck-plan.json 해당 슬라이드에 releaseBlocked=true를 기록한다
    (카피 유지는 해소로 간주되지 않으며, 이 슬라이드는 final 익스포트에서 차단된다 — P7 익스포트 게이트),
    caption은 allowLossyTruncate 슬롯에 한해 truncate + truncatedContent 기록.
    어느 경우든 deck-plan.json 해당 슬라이드에
    needsHumanReview=true와 rejectCount(최종 attempt 값)를 기록하고,
    releaseBlocked 발생분은 deck-manifest.json의 releaseBlocked=true·exportStatus=draft로 집계된다 (P7)
  반려 왕복은 오케스트레이터(L3)가 파일로만 중재한다 (층간 직접 호출 금지 원칙 유지)
- chart-manifest.json / image-manifest.json / motion-manifest.json:
  assets[].{id, path, kind, engine, width, height, tokensRef, altText} (공통 코어)
  chart 자산 추가 필드: caption, sourceRef, sourceLabel, sourceUrl, retrievedAt, dataHash, units, caveat? —
  수치 데이터를 렌더한 차트는 sourceRef·retrievedAt·dataHash가 조건부 필수.
  sourceRef는 자유 문자열이 아니라 claims.json의 claims id 또는 source-pack.json의 소스 id 참조로
  강제하고, sourceLabel은 그 참조 대상에서 파생 생성되는 표시용 값으로 격하한다
  (직접 입력 금지 — 조작 가능한 문자열이 출처 계층을 우회하는 경로를 계약에서 제거).
  claims/source-pack이 없는 단독 사용에서는 sourceRef 생략을 허용하되,
  그 산출물은 P8 신뢰성 게이트를 통과하지 못하는 degrade 등급임을 매니페스트에 명시한다.
  plan의 차트-출처 페어링 검증과 grader 신뢰성 규칙(sourceRef 무결성 검증 포함, P8)이 이 필드를 소비한다
  image 자산 추가 필드: provider, model(생성기 추상화 — 특정 모델명을 계약에 굽지 않는다),
  focalBox, textSafeRegions[], backgroundVariance, ocrFindings[], recommendedCropCandidates[] —
  plan 단계가 텍스트 배치·크롭 재조정(deck-plan binding.transform)을 파일만 보고 결정하는 근거
  motion 자산은 durationMs, fps 필드를 추가로 필수화한다
  (MP4 클립·합성 MP4의 렌더 계약, 프레임 결정론 검증의 기준값)
- image-reject.json: plan 단계가 이미지 재생성을 deck-imagery로 반려할 때 쓰는 계약 —
  copy-reject.json과 대칭 구조.
  rejects[].{slideId, slotId, reason(textSafeMismatch|contrast|ocr|variance), requiredRegions[], attempt}
  attempt 카운터·슬라이드당 상한 2회·파일 영속 규칙은 copy-reject와 동일 (attempt>2는 스키마 위반).
  상한 도달 시 터미널 폴백: 토큰 파생 단색/그라데이션 배경 또는 벡터 패턴으로 대체 바인딩하고
  needsHumanReview=true를 기록한다 — 이미지 수율이 덱 완성을 막지 않는다 (P5)
- slides/*.html: 슬라이드 HTML 산출물 계약 (정본: deck-contracts, 스키마가 아니라 DOM 규약 + 검증 스크립트).
  grader/editor/exporter의 상호 독립은 이 계약이 근거다 —
  셋은 서로의 존재가 아니라 이 규약만 가정한다.
  - 파일 구조: 슬라이드당 자체 완결형 HTML 1파일(slide-NN.html), 외부 참조는 ./assets/ 상대경로만(자산 계약),
    저작 해상도는 deck-constants.json의 canvas 값
  - 필수 루트: <section class="slide" data-slide-id data-layout-id> 1개.
    단독 생산물(비 deck-factory 경로)은 data-layout-id 생략 가능
  - 슬롯 규약: 각 슬롯 컨테이너에 data-slot-id,
    data-slot-kind(title|body|image|chart|caption|media|table|source),
    콘텐츠 출처 추적용 data-content-ref(deck-plan의 contentRef 문자열 그대로, 단독 생산물은 생략 가능)
  - 필수 메타(head): generator 이름/버전, deck-constants 버전, tokens.json 참조(사용 시)
  - 텍스트는 시맨틱 태그(1.2), 스크립트로 레이아웃을 바꾸는 동적 코드 금지(정적 렌더 보장)
  - 접근성 규약 (DOM 필수 규칙 — 매니페스트 altText만으로 갈음하지 않는다):
    콘텐츠 img는 alt 필수, 임베드 SVG 차트는 title/desc 요소 필수,
    장식 이미지는 alt="" + role="presentation" 명시,
    표는 kind=table 슬롯의 시맨틱 table(th/scope 포함)로만 허용(이미지 표 금지),
    DOM 순서가 읽기 순서와 일치. grader가 이 규약 전부를 접근성 규칙군으로 채점한다
  - 검증: deck-contracts의 slide-html 검증 스크립트가 DOM 파싱으로
    루트/슬롯 속성·메타·자산 계약·캔버스 치수를 검사. compose 산출물은 이 검증 통과가 필수(P7),
    grader는 진입 시 같은 검증을 실행해 전 규칙 채점 여부를 결정
  - 소비 규약: grader는 data-slot-kind로 규칙 적용 대상을 식별(계약 미준수 입력은 폴백 규칙 부분집합만),
    editor는 data-slot-id·bbox로 편집 스코프를 지정(미준수 입력은 bbox 전용 모드),
    뷰어/익스포터는 루트 요소와 캔버스 치수만 가정
- deck-manifest.json: 조립기의 최종 산출 기술서 (슬라이드 목록, 사용 자산, 익스포트 경로).
  기계 판독 릴리스 상태 필드 3종을 필수로 갖는다 —
  exportStatus(final|draft): 이번 익스포트의 등급.
  final은 releaseBlocked=false·reviewRequired=false·grader 게이트 통과(P7)가 전부 성립할 때만 허용,
  reviewRequired(bool): 사람 리뷰 대기 여부 —
  deck-plan에 needsHumanReview=true 슬라이드가 하나라도 있으면 true,
  releaseBlocked(bool): deck-plan slides[].releaseBlocked의 OR 집계 —
  true면 exportStatus는 draft만 허용된다.
  draft 격리 규약: exportStatus=draft인 산출물은 exports/draft/ 디렉토리에만 기록하고
  전 파일명에 -draft 접미사를 붙인다 (예: deck-draft.pdf).
  final 산출물은 exports/final/에 기록한다 — 두 디렉토리는 섞이지 않으며,
  전달용 경로(exports/final/)에 draft 산출물을 쓰는 시도를 익스포터가 거부한다
- edit-manifest.json: deck-editor(P9)가 slides/*.html을 직수정할 때 남기는 편집 감사 계약.
  edits[].{slideId, scope(slotId|bbox), type, timestamp, tool}
  이 파일의 존재 자체가 deck-plan.json·deck-manifest.json을 invalidated 상태로 표시한다 —
  이후 재compose는 편집본 덮어쓰기를 기본 거부하고,
  명시적 --discard-edits 플래그로만 편집을 폐기하고 재생성할 수 있다.
  편집 후 유효한 재검증 경로는 grader 재채점과 익스포터 재실행뿐이다 (P9 최종 산출물 에디터 모드)
- measured-overflow.json: compose 직후 실측 렌더 게이트가 오버플로를 검출했을 때
  compose가 plan으로 반환하는 계약 (P7의 추정/실측 이음매 규약 전용).
  overflows[].{slideId, slotId, budgetPx, measuredPx, measuredLines}
  compose는 검출 시 어떤 수정도 하지 않고 이 파일을 산출하며 실패 종료한다 —
  해소 책임은 전적으로 plan에 있다 (P7)
- grade-report.json: 채점기 출력 (룰별 pass/fail/근거수치, 카테고리 점수, 종합점수, hard fail 목록)

사용자 대면 입력 계약은 리포 로컬 정의를 허용하되 스키마 정본 위치를 지정하고,
전부 최소 공통 envelope을 공유한다 (envelope 정본은 deck-contracts) —
{requestId, brief, lang, audience, privacyMode(public|sensitive|confidential), outputDir}.
privacyMode는 외부 전송 경계를 강제한다: sensitive 이상은 외부 이미지 생성 API·퍼블릭 렌더러·
상용 벤치마크 투입을 차단하고 로컬/자체 호스팅 경로만 허용한다.
- chart-request.json: 정본은 deck-charts (유형×엔진 매트릭스 포함)
- 이미지 브리프: 정본은 deck-imagery
- scenes.md: manim-composer 산출 규격을 그대로 정본으로 삼는다 (별도 재정의 금지)
- source-pack.json / claims.json: 정본은 deck-storyline (P10) —
  source-pack은 수집 원자료 목록{id, path|url, license, retrievedAt},
  claims는 주장 테이블{id, text, sourceIds[], confidence}.
  outline.md와 copy.json의 claims[]가 이를 참조한다


## 3. GitHub 리포 분할 맵

최종 형태는 아래 리포 분할이다. 단 도달 경로는 인큐베이션 방식을 쓴다 —
처음부터 리포를 쪼개지 않고, 단일 인큐베이션 리포(kimsh-1/deck-factory-incubator)의
packages/ 디렉토리 구조로 아래 레이어 경계를 그대로 유지하며 개발한 뒤,
계약 스키마가 2회 연속 마일스톤에서 변경 없이 통과하고 세로 슬라이스 E2E가 안정된 패키지부터
아래 독립 리포로 승격한다.
승격 기준: 스키마 안정(2회 연속 무변경) + 외부 소비자 발생 + 5.1 초도 게이트 통과.
가장 불확실한 capacity·overflow·slide DOM·editor 계약은 PoC를 돌려봐야 안정되므로,
이 순서가 vendored diff CI의 유지비를 계약 안정 이후로 미룬다.
의존 방향은 아래로만 흐르고 순환은 없다.
"의존"은 코드 import가 아니라 파일 계약 소비를 뜻한다.

| 리포 | 담는 것 | 파일 계약상 의존 |
|---|---|---|
| kimsh-1/deck-contracts | 계약 JSON 스키마 + 검증 스크립트 원본 + 문서. 아주 작게 유지 | 없음 (최하단) |
| kimsh-1/deck-tokens | L0 스킬. 토큰 스키마, 프리셋 라이브러리, 대비 검증기 vendored 사본(정본은 deck-contracts) | deck-contracts |
| kimsh-1/deck-layouts | 레이아웃 템플릿 카탈로그 (HTML 조각 + 슬롯 정의) + layout-manifest.json, 오버플로 검사기 | deck-contracts, deck-tokens 산출물 |
| kimsh-1/deck-charts | 차트 스킬. 라우팅 로직 + 엔진별 렌더 스크립트 + 테마 어댑터 | deck-contracts, deck-tokens 산출물 |
| kimsh-1/deck-motion | manim + hyperframes 파이프라인 스킬 (배경 HEX를 토큰과 정합) | deck-contracts, deck-tokens 산출물 |
| kimsh-1/deck-imagery | 이미지 생성 스킬 (프롬프트 컴파일 + 배치 생성 + 구도 필터) | deck-contracts, deck-tokens 산출물 |
| kimsh-1/deck-storyline | 소스 수집·주장 정리·아웃라인 스킬 (source-pack + claims + outline.md, P10) | deck-contracts |
| kimsh-1/deck-copy | 프레젠테이션 카피 스킬 (액션 타이틀 + 서술형 개조식 + 윤문 연계) | deck-contracts, deck-layouts 산출물(capacityFloors 수용량 하한 소비, 부재 시 degrade), deck-storyline 산출물(outline/claims, 부재 시 사용자 직접 입력) |
| kimsh-1/deck-grader | 덱 채점기 CLI (DOM 파서 + 31규칙 + 가중합 리포트, P8) | deck-contracts |
| kimsh-1/deck-assembler | L2 조립기 (plan + 결정론 compose) + 뷰어 + 익스포터 | deck-contracts, 위 전부의 산출물 |
| kimsh-1/deck-editor | 비주얼 마감 에디터 (slides-grab 이식, 장기 구동 서버, P9) | deck-contracts (자산/이미지 계약만) |
| kimsh-1/deck-factory | L3 오케스트레이터 스킬 + E2E 시나리오 + 플러그인 패키징(marketplace.json) | 전부 (산출물 소비) |

운영 규칙.

- 각 리포는 SKILL.md + AGENTS.md 이중 포맷 + scripts/ + tests/ (skill-forge 표준 준수)
- deck-contracts의 스키마 변경은 버전 태그로만. 각 리포는 스키마 사본을 vendored로 두고
  CI에서 원본과 diff 검사 (조용한 깨짐 방지 [8]).
  인큐베이션 기간에는 vendored 사본 없이 리포 내 contracts 패키지를 직접 참조하고,
  독립 리포 승격 시점에 vendored + diff CI 체계로 전환한다
- slides-grab에서 이식하는 코드는 MIT 고지 유지. 단 디자인 스타일 데이터 90/95종은
  원본 라이선스 미확인이므로 이식하지 않는다 (8절 리스크)
- deck-assembler와 deck-editor는 런타임 프로파일이 상반된다
  (결정론 배치 도구 vs 장기 구동 비결정 서버). 한 리포로 합치지 않는다


## 4. 파이프라인별 상세 스펙

워커 역할 분담은 skill-forge 플레이북을 따른다.
codex = 코드 구현 (동시성 15), opus = 판단·적대 검증, sonnet = 테스트 작성·실행, fable = 오케스트레이션.
opus가 게이트 판정자로 들어가는 항목은 전부 5.4의 판정 프로토콜을 따른다.
실행 기반은 실행 명령 단위로 고정한다 — 워커 병렬은 GitHub Actions가 아니라 로컬 CLI 러너다.
codex 병렬은 codex-spawn(범용)·codex-imagegen(이미지)의 백그라운드 codex exec 스폰으로,
opus/sonnet 판정·테스트는 Claude 서브에이전트로, 전체 진행은 skill-forge 러너 플레이북으로 구동한다.
GitHub Actions CI는 게이트 검증(스키마 diff, 골든 스냅샷, 렌더 게이트)만 담당하고 생성 작업을 돌리지 않는다.

### P1. deck-tokens — 국내 기준 디자인시스템

목적.
토스 공식 에셋 조사 결과, 국내 디자인시스템 서베이, 기존 design-* 스킬 5종, Astryx를
하나의 토큰 체계로 통합한다.
중요한 제약: 토스 TDS 컴포넌트와 Toss Product Sans는 라이선스상 사용 불가 [1].
따라서 "토스 자산 도입"이 아니라 "토스 원칙의 토큰 재구성"이 정확한 목표다.

입출력 계약.
- 입력: 브리프 (청중, 톤, 라이트/다크, 브랜드 컬러 유무)
- 출력: tokens.json (deck-contracts 스키마)

기존 자산 재사용 vs 신규.
- 재사용: design-apple/linear/notion/stripe/vercel 5종을 프리셋으로 등록.
  이들은 런타임에 호출되는 데이터 소스가 아니라 프롬프트 가이던스 스킬이므로,
  실제 작업은 각 스킬 문서의 HEX/폰트 상수를 추출해 tokens.json 프리셋으로 새로 작성하는 것이다
  (컴포넌트 재사용이 아니라 상수 추출 — 공수 산정에 이 성격을 반영).
  dataviz 스킬의 팔레트 검증기는 deck-contracts의 대비 검증 스크립트 정본으로 승격하고,
  deck-tokens는 vendored 사본 + diff CI로 소비한다.
- 신규: 국내 프리셋 3종 이상 —
  (a) toss-inspired: toss.tech 아티클에서 추출한 원칙(숫자·기호를 국문보다 크게, Value first 등)을
      Pretendard 기반으로 재구성 [1],
  (b) seed-inspired: 당근 SEED의 역할 기반 색상 + 팔레트 색상 2단 구조 차용 (Apache-2.0) [3],
  (c) krds-public: KRDS 공공 톤 (라이선스 원문 확인 후).
  Astryx 테마 7종은 CSS 변수만 증류해 프리셋화 (MIT, React/StyleX는 도입하지 않음) [2].
  Astryx는 공개 Beta라 구조 변동 가능성이 있으므로
  증류 시점의 npm 버전과 커밋 해시를 프리셋 메타데이터에 기록한다.
  theme-factory의 테마당 소형 파일 구조를 그대로 따른다 [8].

정량 합격기준 (측정 방법 포함).
- 모든 프리셋의 contrastPairs가 WCAG 4.5:1 / 3:1 통과 — 검증 스크립트가 상대 휘도 공식으로 계산, 1건이라도 미달 시 프리셋 반려
- 프리셋당 팔레트 6색 이하 (그레이스케일 제외, ΔE<10 유사색 병합 후 카운트) [7]
- 폰트는 전부 라이선스 필드 필수 (OFL/MIT/커스텀 구분), 라이선스 불명 폰트 등록 시 스키마 검증 실패.
  로컬 번들 경로(./assets/fonts/) 부재 폰트도 등록 거부 (1.2 서체 정책)
- 토큰만으로 렌더한 스타일 타일 5종을 opus가 원본 레퍼런스(스크린샷)와 비교해 5점 척도 4 이상 (5.4 프로토콜)

상업 벤치마크: 당근 SEED 문서 사이트의 토큰 문서화 수준, Astryx 테마 패키징.

워커 배정: codex가 스키마/검증기/프리셋 변환 스크립트, opus가 프리셋 심미·라이선스 판정,
sonnet이 스키마 위반 케이스 테스트, fable이 리포 구성과 게이트 진행.

테스트 전략: 프리셋 전수 스키마 검증 + 대비 계산 골든 테스트 + 잘못된 토큰(대비 미달, 라이선스 누락) 거부 테스트.

### P2. deck-layouts — 에셋용 레이아웃 시스템

목적.
상용 AI 툴의 핵심 메커니즘인 "결정론적 레이아웃 템플릿 카탈로그"를 구현한다 [6].
LLM에게 자유 CSS를 맡기지 않고, 템플릿 선택 + 콘텐츠 채움으로 역할을 제한한다.
Beautiful.ai Smart Slides, Canva의 템플릿 시각적 DNA 고정이 벤치마크.
Tome의 자유 캔버스 실패 사례가 반면교사 [6].

입출력 계약.
- 입력: tokens.json
- 출력: layouts/ (템플릿 HTML 조각 + 슬롯 정의 JSON) + layout-manifest.json (2.3 스키마)

기존 자산 재사용 vs 신규.
- 재사용: slides-grab 템플릿 13종(MIT)을 출발점으로 슬롯 구조로 재작성 [4].
  anthropics/skills의 canvas-design 2단계 파일 핸드오프 패턴, OFL 폰트 번들 후보 [8].
- 신규: 레이아웃 20종 이상 (커버, 액션타이틀+증거, 빅스탯, 2단 비교, 풀블리드 이미지+오버레이,
  차트 중심, 타임라인, 인용, 목차, 섹션 구분, 클로징 등).
  각 템플릿에 슬롯별 수용량 계약(capacity: 스크립트별 advance-width 예산 + 행 수 상한, 2.3)과
  kind별 overflowPolicy·splitGranularity(2.3에 계약으로 고정된 값)를 명세.
  capacity는 하한 폰트로 렌더한 실측에서 역산 — 임의값 금지, 글자 수 단위 금지.
  역산 스크립트가 쓰는 하한 폰트·캔버스·마진 값은 deck-constants.json(2.3)에서 로드한다 (자체 상수 금지).
  kind=body 슬롯은 연속 슬라이드 분할(split) 경로를 카탈로그 전체에서 필수 지원
  (P7 해소 루프의 body 터미널 폴백이 항상 성립해야 하므로 비분할 body 슬롯 금지 —
  title/source는 분할 금지 kind라 이 요구의 대상이 아니다, 2.3 overflowPolicy).
  archetype별·kind별 최소 수용량 요약(capacityFloors)을 layout-manifest.json에 산출 (2.3).
  폰트 축소로 오버플로를 흡수하는 동작은 카탈로그 전체에서 금지 (1.2 불변식).

정량 합격기준.
- 모든 템플릿이 수용량 예산(capacity) 상한 콘텐츠 주입 시 오버플로 0건 —
  한글 전각 근사 케이스와 라틴 최악폭 글리프(W 연속) 케이스를 각각 주입하고,
  Playwright로 렌더 후 scrollHeight > clientHeight 검사 자동화.
  이 실측 렌더 검사가 수용량 보증의 최종 게이트다 (글자 수 대조는 게이트가 아님)
- 모든 템플릿의 텍스트 computed font-size가 스펙 하한 이상 — DOM 검사 스크립트
- 제목 슬롯 좌표 고정 (편차 슬라이드 너비의 1% 이내)은 본문형(archetype=content) 템플릿의
  액션 타이틀에만 적용 — cover/section/quote/stat/closing 계열은 명시적 예외 [7]
- 풀블리드 계열 템플릿은 텍스트 영역 반투명 오버레이/블러 처리 내장, 대비 재계산 통과 [10]
- layout-manifest.json이 deck-contracts 스키마 검증 통과,
  capacity 역산 근거(스크립트별 실측 스크립트 출력)와 capacityFloors 동봉

상업 벤치마크: Beautiful.ai Smart Slides의 레이아웃 후보 교체 UX.

워커 배정: codex가 템플릿 마크업과 오버플로 검사기, opus가 각 템플릿 시각 판정(스크린샷 검수, 5.4 프로토콜),
sonnet이 경계 콘텐츠(최장 텍스트, 빈 슬롯) 테스트, fable이 카탈로그 커버리지 관리.

테스트 전략: 템플릿 x 극단 콘텐츠 매트릭스 렌더 스냅샷 + 오버플로/폰트하한 CI 게이트.
매트릭스(20종 x 극단 콘텐츠)의 실행 동시성과 러닝타임을 실측해 CI 게이트 채택 전에 예산을 문서화.

### P3. deck-charts — 도표 생성

목적.
오픈소스 10종을 디자인 토큰이 주입되는 단일 도표 스킬로 묶는다.
채택 10종과 역할분담은 리서치 결정을 따른다 [9]:
Vega-Lite(+vl-convert, 기본 엔진) / ECharts(renderToSVGString) / Observable Plot — 통계 삼각편대,
Mermaid / Graphviz / Kroki(자체 호스팅) — 다이어그램 삼각편대,
Plotly(+Kaleido) / Cytoscape.js / Chart.js — 틈새, D3 — 최후 폴백 (LLM에 기본 비노출).

입출력 계약.
- 입력: chart-request.json (유형, 데이터 또는 데이터 경로, 캡션,
  sourceRef — claims.json/source-pack id 참조, 2.3) + tokens.json
- 출력: SVG(기본) + PNG(래스터 폴백) + chart-manifest.json
- 화이트리스트 유형 30종 × 채택 엔진 10종의 매핑 매트릭스를 chart-request.json 계약 문서에 명시
  (유형마다 기본 엔진 1 + 폴백 엔진, 커버리지가 표로 한눈에 보이게).
  각 셀은 supported | required_fallback | not_applicable 세 상태로 분류한다 —
  엔진별 역할 분담(리서치 결정 [9])상 모든 엔진이 모든 유형을 렌더하지 않으며,
  Chart.js는 PNG/canvas 경로, Cytoscape.js는 headless 좌표 계산 위주(SVG 직렬화 별도 검증),
  D3는 최후 폴백 한정이므로 not_applicable 셀이 정상이다.
  MVP 채택 엔진은 Vega-Lite, ECharts, Mermaid, Graphviz 4종으로 시작하고,
  Plotly/Cytoscape.js/Chart.js/D3는 실제 수요가 확인된 유형부터 단계 확장한다
- 출처 필드 전달: chart-request.json의 출처 입력은 자유 문자열이 아니라
  sourceRef(claims.json의 claims id 또는 source-pack id 참조, 2.3)로 받고,
  chart-manifest의 sourceRef, caption, sourceUrl, retrievedAt, dataHash, units 필드(2.3)로
  반드시 전달된다. sourceLabel은 sourceRef가 가리키는 항목에서 파생 생성한다 —
  plan의 차트-출처 페어링 검증과 grader 신뢰성 규칙(sourceRef 무결성, P8)의 근거

기존 자산 재사용 vs 신규.
- 재사용: dataviz 스킬의 방법론(형태 휴리스틱, 색 공식, 팔레트 검증기)을 라우팅/테마 규칙의 상위 문서로.
- 신규: 유형 분류 라우터, 엔진별 렌더 스크립트(전부 scripts/, 컨텍스트 비로드 실행),
  tokens.json → 엔진별 테마 변환 어댑터 공통층, Kroki Docker 셋업 스크립트.

정량 합격기준.
- 유형×엔진 매트릭스의 supported·required_fallback 셀(유형별 기본 엔진 + 지정 폴백)에 대해
  골든 입력 → 렌더 성공률 100% (CI hard gate). not_applicable 셀은 게이트 대상에서 제외 —
  전 셀 100%는 지원 불가능한 셀 때문에 CI를 영구히 막으므로 게이트로 삼지 않는다.
  한글 폰트 PoC에서 실패한 엔진은 기준을 완화하는 대신 채택 목록에서 제외하고
  해당 유형의 라우팅을 폴백 엔진으로 갱신한다 — 분기를 미리 고정
- 산출 SVG의 색상이 토큰이 정의한 스케일에서 파생된 색만 사용 —
  카테고리 팔레트 멤버이거나 토큰에 정의된 순차/발산 램프 양끝 사이의 보간색만 허용
  (히트맵·램프는 팔레트에 문자 그대로 없는 보간색을 정당하게 쓰므로 단순 멤버십 대조는 오탐).
  SVG 파싱해 fill/stroke 추출 후 팔레트 멤버십 + 램프 보간 판별 스크립트로 대조
- 차트 텍스트(축 라벨, 데이터 라벨) 폰트가 토큰 폰트와 일치, 한글 라벨 렌더 깨짐 0건 —
  한글 골든 렌더를 PNG로 떠서 opus 시각 판정 (한글 폰트 임베딩은 리서치에서 미검증이라 초기 PoC 필수 [9])
- 3D 효과/중복 범례/불필요 그리드 미사용 — Tufte 근사 규칙을 렌더 옵션 기본값으로 강제하고 grader가 재검 [7]
- 카테고리 3개 이하인데 범례 사용 시 fail (직접 라벨링 강제) [7]

상업 벤치마크: think-cell의 직접 라벨링/주석 자동화 관행 [7].

워커 배정: codex가 엔진 어댑터 병렬 구현 (MVP 4종 우선, 확장 엔진은 수요 확인 시 — codex-spawn, 엔진당 1워커),
opus가 시각 품질·팔레트 준수 판정,
sonnet이 골든 렌더 회귀 테스트, fable이 라우팅 스펙과 게이트.

테스트 전략: 유형별 골든 SVG 스냅샷 + 팔레트 추출 자동 대조 + Chromium 의존 엔진(mermaid/Kaleido)은 Kroki 컨테이너 격리 경로로 이중화.
유형×엔진 렌더 매트릭스(supported+폴백 셀만, MVP 4엔진 기준)의 러닝타임과 동시성을 실측해
CI 게이트 채택 전에 예산을 문서화한다 (P2와 동일 요구).

### P4. deck-motion — 3b1b 스타일 정지컷/영상

목적.
manim으로 3b1b 스타일 PNG 정지컷과 MP4 클립을 만들고,
hyperframes로 자막/전환/오디오를 얹은 발표용 MP4 또는 하이브리드 덱 자산을 만든다 [5].
포지셔닝: 코어 덱 파이프라인 밖의 옵셔널 플러그인이다 (산출물이 3급 베스트 에포트, 1.2).
motion-manifest가 없어도 파이프라인 전체가 완결되며,
core E2E와 5.2 환경 게이트는 이 리포의 의존성(LaTeX/FFmpeg)을 요구하지 않는다
(doctor motion 프로파일 전용, 5.2).

입출력 계약.
- 입력: 주제 브리프 → scenes.md (manim-composer 산출) + tokens.json (배경 HEX 정합용)
- 출력: PNG 정지컷(manim -s), MP4 클립(manim -qh), 합성 MP4(hyperframes render) + motion-manifest.json

기존 자산 재사용 vs 신규.
- 재사용: manim-composer / manimce-best-practices / manimgl-best-practices 3종 스킬 (이미 설치됨, 재구축 금지).
  hyperframes 스킬 팩과 CLI (Apache 2.0).
- 신규: 두 툴체인을 잇는 글루 — scenes.md → 씬별 렌더 잡 분배(codex-spawn),
  해상도/배경색 정합 규칙(Manim 배경 HEX를 tokens.json과 일치), doctor 스크립트(FFmpeg/LaTeX/Node22/Chrome 점검).

정량 합격기준.
- PoC 게이트 선행: 수식 1컷 PNG → 3슬라이드 hyperframes HTML → 5초 MP4 관통이 로컬(WSL)에서 성공해야 본 빌드 착수 [5]
- 씬 렌더 성공률 95% 이상 (실패분 자동 재시도 1회 포함), 렌더 로그에 LaTeX 오류 0건
- PNG 배경색이 슬라이드 배경 토큰과 HEX 일치 (픽셀 샘플링 검사) — 합성 이음매 방지 [5]
- MP4는 지정 fps/해상도 준수, 프레임 결정론 검증(동일 입력 2회 렌더 해시 비교)
- 산출 컷을 opus가 3b1b 레퍼런스 대비 스타일 판정 4/5 이상 (5.4 프로토콜)

상업 벤치마크: 3Blue1Brown 본편의 컷 구성 밀도.

워커 배정: codex가 manim 씬 코드 대량 생성(동시성은 GPU/OOM 고려해 15가 아닌 4~6으로 제한 [5]),
opus가 씬 계획 검토와 컷 판정, sonnet이 doctor/렌더 스모크 테스트, fable이 PoC 게이트 판단.

테스트 전략: doctor 스크립트를 CI 진입 조건으로, 씬 템플릿 3종 골든 렌더, WSL 환경에서 ManimGL은 옵션 처리(CE 기본).

### P5. deck-imagery — 배경/필요 이미지 생성

목적.
이미지 생성기로 텍스트 없는 배경, 네거티브 스페이스 확보된 히어로 이미지를 양산한다.
생성기는 provider/model 필드로 추상화하고(기본값 gpt-image-2) 계약은 capability 중심으로 유지한다 —
모델명·약관 변동이 계약을 깨지 않게 한다 (2.3 image 자산 필드).
필요시 통짜 이미지 프레젠테이션(카드뉴스형)용 컷 경로도 지원.

입출력 계약.
- 입력: 슬라이드별 이미지 브리프 + tokens.json (배경 HEX, 무드)
- 출력: prompts.jsonl → PNG 배치 → 구도 필터 통과분 + image-manifest.json

기존 자산 재사용 vs 신규.
- 재사용: image-prompt 스킬의 C12 플레이북과 티어드 네거티브 (핵심 자산, 재구축 금지).
  codex-imagegen 러너 (PARALLEL 제어, 세션 폴더 회수).
- 신규: C12 플레이북에 4종 세트 표준 삽입 [10] —
  (a) 피사체 점유율 수치, (b) 네거티브 스페이스 위치를 텍스트 배치 의도와 결합,
  (c) 배경색 HEX 고정, (d) 텍스트/로고/워터마크 금지 화이트리스트 네거티브.
  구도 자동 필터: 텍스트 배치 예정 영역의 색상 분산도를 측정해 균일하지 않으면 탈락 (수율 보정 [10]).
  필터 산출(focalBox, textSafeRegions, backgroundVariance, ocrFindings, recommendedCropCandidates)은
  image-manifest 자산 필드로 기록한다 (2.3).
  브리프의 텍스트 배치 의도가 최종 레이아웃 슬롯의 텍스트 영역과 어긋나면
  plan 단계가 (a) deck-plan binding.transform(crop/objectPosition/overlay)으로 재조정하거나
  (b) image-reject.json(2.3)으로 재생성을 반려한다 — 둘 다 파일 계약으로만 흐르고,
  반려 상한(2회) 도달 시 토큰 파생 단색/그라데이션/벡터 패턴 배경 폴백으로 종료한다 (2.3 터미널 규칙).
  후처리: 대비 미달 시 반투명 오버레이/블러+밝기 다운 자동 적용 스크립트.

정량 합격기준.
- 배치 생성 수율: 요청 컷 대비 구도 필터 통과분을 런별 측정 지표로 기록.
  60%는 hard 게이트가 아니라 관리 기준선이다 —
  리서치가 안정 수율을 보장하지 않으므로 [10] 수율 미달이 파이프라인을 막지 않는다.
  미달 시 프롬프트 완화 재시도 → 그래도 부족하면
  단색/그라데이션/벡터 패턴 배경 폴백(2.3 image-reject 터미널)으로 덱 완성을 보장
- 텍스트 예정 영역 위 실제 텍스트 오버레이의 대비 4.5:1(또는 큰 텍스트 3:1) — 오버레이 색 기준 재계산으로 검증 [10]
- 생성물 내 원치 않는 문자 렌더 0건 — OCR 스캔으로 자동 검출, 검출 시 탈락
- 이미지에 카피를 굽지 않음 (WCAG 1.4.5) — 텍스트는 항상 HTML 레이어

상업 벤치마크: Gamma의 이미지 소스 정책 선택 UX, 상용 스톡 수준의 배경 균질성.

워커 배정: codex가 프롬프트 컴파일 확장과 필터/후처리 스크립트, codex-imagegen이 생성 실행(동시성 15),
opus가 무드/브랜드 적합 판정(5.4 프로토콜), sonnet이 필터 정확도 테스트(양성/음성 샘플), fable이 수율 관리.

테스트 전략: 구도 필터에 라벨링된 합격/불합격 이미지 셋으로 정밀도 검사, OCR 검출 회귀 테스트.

### P6. deck-copy — 프레젠테이션 글 윤문

목적.
아웃라인에서 슬라이드별 액션 타이틀과 본문 카피를 만든다.
한국어 기본값은 서술형 개조식 (조사 유지 + ~함/~임 종결, 행정업무규정 제7조 근거) [10],
영문은 10~15단어 완결문 + 능동태 + 정량화 [7][10].
라벨형 제목(현황, Overview류) 금지, 결론형 강제.

입출력 계약.
- 입력: outline.md (deck-storyline P10 산출 또는 사용자 직접 작성) + claims.json(있으면).
  수용량 상한은 layout-manifest.json의 capacityFloors(archetype별·슬롯 kind별 최소 수용량, 2.3)에서
  자기 슬라이드의 archetype 추정에 해당하는 하한만 보수적 기본 예산으로 소비한다 —
  전 템플릿 단일 최소값 기준은 과압축을 만들므로 쓰지 않는다.
  deck-copy 실행 시점에는 슬라이드→레이아웃 바인딩이 아직 존재하지 않으므로
  (바인딩은 P7 plan 단계 소관), 특정 슬롯의 capacity를 대조하는 사전 fit은 불가능하다.
  여기서의 fit은 보수적 하한 기준의 1차 방어일 뿐이고,
  수용량 봉인의 최종 담당은 plan 단계의 수용량 검사와 copy-reject.json 반려 재진입이다 (P7, 2.3).
  layout-manifest.json이 없는 단독 사용에서는
  deck-contracts에 문서화된 기본 보수 예산으로 degrade (2.2)
- 출력: copy.json (slides[].actionTitle/bullets/claims/sourceLine, 2.3 스키마) + titles-test 리포트

기존 자산 재사용 vs 신규.
- 재사용: gn-voice — 개인화 문체가 필요할 때 후단 결합.
  디스패치 경계는 2.2에 정의: 기존 산문 개인화는 gn-voice, 구조화 카피 생성은 deck-copy,
  양쪽 description에 경계 문구를 명기.
  humanize-korean — AI 티 제거 2차 패스. 기술 문서 성격 카피에는 gn-voice 미적용 (기존 정책 준수).
- 신규: 액션 타이틀 린터 (완결문 여부, 15단어/2줄 상한, 등위접속사 검출, 라벨형 패턴 블랙리스트) [7],
  개조식 압축 팩트체크 패스 (시점/주체/조건 소실 검출 — 원문 대비 개체 보존 검사) [10],
  6x6 근사와 발화 시간(130~150wpm) 계산기,
  오버플로 반려 처리기: P7 plan 단계가 산출한 copy-reject.json(2.3)을 소비해
  반려된 슬라이드의 카피를 명시된 수용량 예산 이내로 재작성하거나 슬라이드 분할안을 반환.
  재작성 copy.json에는 소비한 attempt를 rejectAttempt로 반드시 에코한다 (2.3 카운터 규약 —
  카운터는 파일 필드로만 흐르고, deck-copy가 자체 재진입 상태를 기억하지 않는다).
  재진입은 슬라이드당 2회 상한(2.3, attempt>2는 스키마 위반)이며,
  상한 도달 이후의 종료는 plan의 kind별 터미널
  (body 강제 분할, title/source releaseBlocked 마킹)이 담당한다 (P7).

정량 합격기준.
- 타이틀 테스트: 제목만 이어 읽어 논지가 통하는가 — opus가 제목 시퀀스만 보고 스토리 재구성, 성공해야 통과 (5.4 프로토콜) [7]
- 제목 15단어 이하 100%, 라벨형 0건, 등위접속사+이중 서술어 0건 — 린터 자동 측정
- 본문 슬라이드당 40단어 이하 권장 / 60단어 초과 fail, 불릿 6줄 이하 [7]
- 슬롯 대상 카피의 측정 렌더 폭이 capacityFloors 예산 초과 0건 —
  린터가 번들 폰트 메트릭으로 스크립트별(한글/라틴) advance-width를 계산해 대조.
  글자 수 카운트가 아니라 폭 측정 기준 (비례폭 폰트에서 글자 수는 폭을 예측하지 못함)
- 압축 팩트체크: 원문의 수치/시점/주체가 카피에서 왜곡된 건 0건 — opus 대조 판정 (5.4 프로토콜)
- 오타 0건 (기존 정책: 오타 금지, 비문은 문체 범위 내 허용)

상업 벤치마크: 맥킨지류 액션 타이틀 관행 (2차 자료 재구성 수치임을 명시 [7]).

워커 배정: codex가 린터/계산기, opus가 타이틀 테스트와 팩트체크 판정, sonnet이 린터 케이스 테스트, fable이 규칙 튜닝.

테스트 전략: 합격/불합격 카피 코퍼스로 린터 정밀도 측정, 한국어/영어 이중 케이스.

### P7. deck-assembler — 덱 조립

목적.
모든 매니페스트를 읽어 최종 HTML 덱을 조립하고 다중 포맷으로 익스포트한다.
비주얼 마감 편집은 deck-editor(P9)로 분리 — 이 리포는 결정론 배치 도구로만 유지한다.

입출력 계약.
- 입력: tokens.json + layout-manifest.json + copy.json + chart/image/motion-manifest
- 중간 산출: deck-plan.json (plan 단계, 2.3 스키마) —
  레이아웃 선택, 슬롯 바인딩, 오버플로 해소(분할 포함)는 전부 여기서만 일어난다.
  반려 발생 시 copy-reject.json(2.3)을 함께 산출
- 출력: slides/*.html + viewer.html + deck-manifest.json(릴리스 상태 필드 포함, 2.3) +
  exports/final/ 또는 exports/draft/(pdf, png, pptx — 2.3 draft 격리 규약) + grade-report.json

기존 자산 재사용 vs 신규 (slides-grab 이식 우선순위 [4]).
- 이식: src/slide-mode.cjs (치수/좌표계 로직 — 단, 상수 값은 하드코딩을 제거하고
  deck-contracts의 deck-constants.json vendored 사본을 로드하도록 개조한다.
  치수·좌표계·폰트 하한의 단일 소스는 slide-mode.cjs가 아니라 deck-constants.json이다, 2.3),
  src/image-contract.js (자산 계약 + 런타임 주입),
  design-gate 지문 패턴. (에디터 계열 이식은 전부 P9로 이동)
- 신규: plan 단계 — copy.json/매니페스트/layout-manifest.json을 읽어
  바인딩 → 수용량 검사 → 재바인딩을 반복하고
  차트-출처 페어링 검증(2.3)과 이미지 transform 재조정/image-reject 반려(P5)를 이 단계에서 수행하며,
  모든 오버플로가 이미 해소된 최종 deck-plan.json을 산출
  (비결정 판단은 여기까지만 허용, 산출물은 스키마 검증 통과 필수).
  오버플로 해소 루프는 plan 내부에서 kind별 overflowPolicy(2.3)에 따라 고정 순서로 처리:
  (1) 수용량 더 큰 대체 레이아웃으로 재바인딩 (layout-manifest 기재 순서),
  (2) 그래도 초과면 copy-reject.json으로 deck-copy에 반려 —
      반려가 분할보다 먼저다. 분할을 먼저 하면 body 오버플로가 copy-reject에 도달하지 못하는
      죽은 경로가 되고, 분할 불가 kind(title/source)는 반려 외 해소 수단이 없기 때문.
      왕복은 오케스트레이터가 파일로만 중재, 카운터는 copy-reject.json의 attempt 필드와
      재작성 copy.json의 rejectAttempt 에코로만 흐른다 (2.3 — 계약 밖 재진입 카운터 금지),
      슬라이드당 상한 2회 (attempt>2는 스키마 위반, 2.3),
  (3) 상한 도달 시 kind별 터미널 액션으로 무조건 종료:
      body는 splitGranularity 경계 강제 연속 슬라이드 분할 (2.3 arity 규칙),
      title/source는 분할·truncate 금지 kind이므로 카피는 유지하되 해소 실패로 확정하고
      해당 슬라이드에 releaseBlocked=true를 기록 (2.3 deck-plan — final 익스포트 차단),
      caption은 allowLossyTruncate 슬롯에 한해 truncate + truncatedContent 감사 기록.
      어느 경우든 해당 슬라이드에 needsHumanReview=true, rejectCount를 deck-plan.json에 기록한다 (2.3).
  (3)은 항상 성립하는 터미널이다 —
  body 분할 경로가 카탈로그 전체에서 필수(P2)이고
  나머지 kind는 releaseBlocked 마킹(또는 감사 기록 동반 truncate) 종료가 정의돼 있어
  데드락과 무한 루프가 없다. 카피 유지는 해소가 아니라 릴리스 차단 상태로만 존재한다 —
  "오버플로 해소 완료 deck-plan"(1.2/2.3)과의 모순은
  releaseBlocked 필드가 해소 실패를 명시 상태로 만들고 익스포트 게이트가 이를 소비함으로써 제거된다.
  단독 사용(오케스트레이터 부재) 시 (2)를 건너뛰고 (3)으로 직행한다.
  어느 단계에서도 폰트 축소는 하지 않는다 (1.2 불변식).
  수용량 검사의 책임 분리 (추정/실측 이음매 규약):
  plan의 수용량 검사는 번들 폰트 메트릭 기반 advance-width 합산과 행 수 계산의
  결정론적 추정이며, 실측 렌더가 아니다. 실측 책임은 compose가 진다 —
  compose는 산출 직후 헤드리스 렌더 실측 게이트(Playwright: 슬롯별 scrollHeight/clientHeight,
  computed font-size)를 자체 실행한다. 이음매 처리 규약:
  (a) plan 추정은 deck-constants.json의 capacityMargin(기본 5%)을 예산에서 차감해 보수화 —
      추정 오차는 마진이 흡수하는 것이 정상 경로,
  (b) 그래도 실측 오버플로가 나오면 compose는 어떤 수정도 하지 않고(결정론 유지)
      measured-overflow.json(2.3)을 산출하고 실패 종료,
  (c) plan이 이를 소비해 해당 슬라이드를 kind별 터미널 경로((3))로 재계획 —
      plan→compose 재왕복은 1회 상한, 재실측도 실패하면 해당 슬라이드에
      needsHumanReview=true + releaseBlocked=true를 기록하고 종료
      (final 익스포트 차단, 아래 익스포트 게이트),
  (d) measured-overflow 발생은 항상 회귀 신호로 로그에 남겨 P2 capacity 역산 보정에 환류한다.
  compose 단계 — 확정 deck-plan.json 바인딩대로 템플릿 슬롯에 콘텐츠 주입.
  자유 CSS 생성 금지, 레이아웃 변경·분할·선택 일절 없음 —
  compose 전후로 슬라이드 수·layoutId·바인딩이 불변이므로
  deck-plan.json이 다운스트림(바인딩 게이트, grader, editor)의 단일 소스로 유지된다.
  산출 slides/*.html은 2.3의 슬라이드 HTML 산출물 계약(루트/슬롯 data 속성, 필수 메타)을 준수하고
  slide-html 검증 스크립트 통과가 compose 완료 조건이다,
  transform scale 뷰어, Playwright 익스포터 (Marp CLI 방식 벤치마크, --format/--range 인터페이스는 Slidev 참고 [6]),
  design-gate를 grader 통과와 연동한 자동 기록 래퍼 —
  책임 경계: design-gate는 산출물 신선도(freshness) 지문 기록(design-gate.json),
  grader는 품질 판정(grade-report.json). 이름과 출력 파일을 분리해 혼동을 차단한다.

정량 합격기준.
- 조립 결정론: 동일한 deck-plan.json + 입력 파일로 compose 2회 실행 시 HTML diff 0.
  plan 단계는 결정론 게이트 대상이 아니며, 산출 deck-plan.json의 스키마 검증 통과만 요구
- 산출 slides/*.html 전수가 slide-html 계약 검증 스크립트(2.3) 통과 —
  grader/editor/exporter 독립 소비의 전제 조건
- compose 실측 렌더 게이트: releaseBlocked=false 슬라이드 전수의 실측 오버플로 0건이어야 익스포트 진행.
  releaseBlocked=true 슬라이드가 존재하면 final 익스포트는 차단되고,
  deck-manifest의 exportStatus=draft·releaseBlocked=true·reviewRequired=true 표기와 함께
  draft 강등 익스포트만 허용된다 (draft 격리 규약은 2.3 deck-manifest — exports/draft/ + -draft 접미사).
  불일치 케이스(추정 통과·실측 초과)는 measured-overflow.json 산출 → plan 재계획 왕복이
  규약대로 완주하는지 케이스 테스트로 증명 (위 이음매 규약 (b)/(c))
- 렌더된 전 텍스트의 computed font-size가 토큰 하한 이상 — 축소 경로(autofit류) 부재의 실측 증명
- grader hard fail 0건 + 90점 이상 + deck-manifest releaseBlocked=false여야
  final 익스포트 게이트(exportStatus=final) 개방
  (design-gate 연동, 90점 산출은 P8 채점 스펙 기준).
  unattended 모드에서는 결정론 hard fail 0건이면 draft 익스포트를 허용하고
  의미론 미판정분은 needsHumanReview로 이월하며,
  releaseBlocked 슬라이드가 존재하면 종료 코드 review-required로 끝난다 (5.3 실행 모드)
- 시각 QA 루프: 슬라이드 PNG 변환 → 신선한 눈 서브에이전트 검수(겹침/오버플로/저대비 체크리스트) →
  fix → re-verify 최소 1회 완주 전 성공 선언 금지
  (anthropics/skills pptx 스킬의 QA 규정을 참고해 자체 재작성 — 원문은 Proprietary라 문구 이식 금지 [8])
- PDF 익스포트에서 텍스트 선택 가능(print 모드), PNG는 지정 해상도 준수
- PPTX는 베스트 에포트로 명시하고 별도 합격기준 없이 스모크만 (원본 계약이 실험적 [4])

상업 벤치마크: Marp/Slidev의 익스포터 인터페이스, Beautiful.ai의 결정론적 배치 재현성 [6].

워커 배정: codex가 이식/조립기/익스포터, opus가 시각 QA 서브에이전트 판정, sonnet이 E2E 스모크와 결정론 테스트, fable이 통합 순서.

테스트 전략: 골든 매니페스트 + 골든 deck-plan → 골든 덱 스냅샷,
오버플로 해소 루프 3분기(대체 레이아웃/반려/kind별 터미널) 각각의 케이스 테스트
(터미널은 body 분할·title 카피 유지+releaseBlocked 마킹·caption truncate 감사 기록을 kind별로 확인)
(반려 상한 도달 케이스는 attempt 카운터 흐름과 needsHumanReview/rejectCount/releaseBlocked 산출,
deck-manifest exportStatus=draft 집계·final 차단까지 확인),
measured-overflow 왕복 케이스(추정 통과·실측 초과 슬라이드 주입 → 재계획 → 재실측 통과),
slide-html 계약 검증 회귀, 익스포트 3포맷 스모크.

### P8. deck-grader — 덱 채점기

목적.
5.3의 구상을 P1~P7과 동급의 파이프라인으로 구현한다.
모든 Phase의 심판이므로 규칙군을 로드맵에 걸쳐 단계 배정한다 (6절).

입출력 계약.
- 입력: slides/*.html (+ 필요시 exports/) + grader.yaml
- 출력: grade-report.json (룰별 pass/fail/근거수치, 카테고리 점수, 종합점수, hard fail 목록)

정량 합격기준.
- 규칙 커버리지 31/31 — consulting-quality의 후보 규칙 → grader 규칙 번호 매핑표를
  리포 docs 부록으로 고정해 구현 범위를 명시 [7]
- 결정 규칙군: 골든 덱 5벌 → 골든 grade-report 스냅샷 일치
- 신뢰성 규칙군의 sourceRef 무결성 검증: 수치 차트 자산의 chart-manifest sourceRef가
  claims.json/source-pack.json의 실존 id를 가리키는지 대조 —
  부재·댕글링이면 hard fail (수치 슬라이드 출처 라인 부재 hard fail의 상류 검증, 5.3/2.3).
  sourceLabel 문자열 존재만으로는 통과하지 못한다
- 채점 스펙이 grader.yaml 기본값으로 존재: 카테고리 가중치(합 100), 규칙별 만점·감점 함수, 집계식 (5.3)
- grader.yaml의 치수·폰트 하한 기본값 섹션은 deck-constants.json(2.3)에서 sync 스크립트로 생성 —
  수기 수정 금지, CI가 생성본과 diff 검사 (상수 단일 소스 계약의 grader 측 소비 방식)
- 캘리브레이션 골든셋 조달 (출처와 라이선스를 Phase 0에서 확정·동결):
  - 출처는 확보 가능하고 라이선스가 명확한 공개 원천만 —
    상장사 공개 IR/어닝 덱, 공공기관 공개 보고 덱,
    유료 계정으로 자체 생성한 Gamma/Beautiful.ai 산출물.
    비공개 MBB 실물 덱은 조달 불가하므로 앵커로 쓰지 않는다
  - 포함/제외 기준(무엇을 상업 수준으로 인정하는가)을 docs에 문서화하고 셋을 동결.
    Phase 5 판정자 검증용 우수/열위 덱 쌍도 이 동결 셋에서 파생시켜 근거를 남긴다
- 캘리브레이션 2단계화 (공수 분리 — 레퍼런스 리빌드는 grader 구현과 별개 프로젝트급이므로):
  - 1단계(Phase 2): synthetic HTML 골든셋(규칙별 양성/음성 케이스 합성 덱) +
    자체 생성 덱으로 규칙·가중치·집계식을 안정화하고 잠정 합격선 90을 기록한다.
    Phase 3의 90점 게이트는 이 잠정 캘리브레이션을 기준으로 한다
  - 2단계(Phase 5 준비): 공개 레퍼런스 덱 리빌드 기반의 상업 수준 대응 캘리브레이션 —
    아래 포맷 정합 절차를 이때 수행하고, 결과로 합격선을 조정하면 이력을 남긴다
- 캘리브레이션 비교가능성 (포맷 정합, 2단계에서 수행):
  grader 1차 경로는 HTML DOM + computed style인데 레퍼런스 원본은 PPTX/PDF로 존재하므로
  두 경로의 점수는 같은 척도가 아니다. 따라서 —
  - 골든셋 중 3벌은 파이프라인 HTML 포맷으로 수작업 리빌드해 전 규칙을 동일 척도로 채점한다.
    벌당 리빌드 공수를 Phase 5 준비 계획에 명시
  - 리빌드 전 원본에는 python-pptx/OCR+CV 폴백 경로에서 실행 가능한 규칙 부분집합만 채점해
    리빌드 충실도를 교차 확인한다
  - 레퍼런스 덱이 grader에 들어가는 파일 형식(HTML 리빌드본)을 계약 수준으로 고정한다
- 캘리브레이션: 위 골든셋 채점으로 합격선 90이 상업 수준 덱의 점수대와 대응함을 확인하고
  근거를 docs에 기록.
  대응하지 않으면 가중치 또는 합격선을 YAML에서 조정하고 조정 이력을 남긴다
- 의미론 hard 게이트(5.3)의 LLM 심사: 앵커드 루브릭 3종·불합격 판정식이 grader.yaml과
  리포 텍스트 파일로 고정돼 있고, 판정자가 기지의 합격/불합격 셋에서
  5.4 통과 임계값(다수결 일치율 90%)을 기록해야 투입.
  미달 시 soft 강등 금지 — 사람 판정 승격으로 hard 게이트 유지 (5.3/5.4 예외 규정)
- CLI 단독 실행 가능, python-pptx / OCR+CV 폴백 경로 동작 스모크

워커 배정: codex가 규칙 구현(카테고리 규칙군 단위 병렬), opus가 의미론 판정과 캘리브레이션 심사,
sonnet이 골든 리포트 회귀와 규칙별 양성/음성 케이스, fable이 규칙 매핑표와 가중치 확정 진행.

테스트 전략: 골든 덱→리포트 스냅샷, 규칙별 양성/음성 케이스, grader.yaml 오버라이드 테스트, 레퍼런스 골든셋 채점 리그레션.

### P9. deck-editor — 비주얼 마감 에디터

목적.
slides-grab의 bbox 편집 아키텍처를 독립 스킬로 이식한다.
생산 경로와 무관하게 임의의 slides/*.html에 동작 — deck-factory 없이 단독 상품성 유지.

포지셔닝: 최종 산출물 에디터(final artifact editor)다.
compose 이후의 HTML을 직수정하며 deck-plan.json으로 역전파하지 않는다 —
대신 편집 사실을 edit-manifest.json(2.3)으로 남겨 deck-plan/deck-manifest를 invalidated로 표시하고,
이후 재compose가 편집본을 덮어쓰는 것을 기본 차단한다 (--discard-edits로만 폐기 가능).
편집 후 유효 경로는 grader 재채점과 익스포터 재실행이다.
P7의 "deck-plan 단일 소스" 주장은 compose까지의 생산 경로에 한정되고,
에디터 통과 이후의 정본은 slides/*.html + edit-manifest.json이다 — 두 주장의 충돌을 여기서 끊는다.

입출력 계약.
- 입력: slides/*.html (아무 출처나 가능)
- 출력: 직수정된 slides/*.html (fs.watch 리로드) + edit-manifest.json (2.3)
- 계약 의존: deck-contracts의 자산 계약(image-contract) + 슬라이드 HTML 산출물 계약(2.3)의
  소비 규약만. 매니페스트 불필요.
  계약 준수 입력에서는 data-slot-id 기반 슬롯 단위 편집, 미준수 입력에서는 bbox 전용 모드로 degrade —
  이 이중 경로가 "임의 HTML에도 동작"과 계약 기반 독립성을 동시에 성립시킨다

기존 자산 재사용 vs 신규.
- 이식: editor-server.js의 /api/apply 흐름 (스크린샷 → sharp bbox 주석 → codex/claude exec → 파일 직수정 → fs.watch 리로드),
  editor-direct-edit (비에이전트 직접 편집)
- 수정: model-registry의 하드코딩 모델 ID를 로컬 CLI 실제 모델명으로 매핑,
  README의 star 요청류 에이전트 지시 제거,
  에이전트 서브프로세스는 격리 환경에서만 구동 (8절 리스크 완화 준수)

정량 합격기준.
- 에디터 API 통합 테스트 green, 격리 환경 구동 확인
- 편집 → grader 재채점 왕복 1회 완주 (편집이 hard fail을 새로 만들지 않는지 확인 경로)
- 편집 승인/되돌리기 UX 최소셋: 편집 단위 undo 1단계 이상, 적용 전 미리보기 —
  단독 상업 완성도(5.1) 주장의 측정 가능한 조작화 (Gamma/Pitch 벤치마크 대비 최소 기능선)
- deck-assembler 산출물이 아닌 임의 HTML 슬라이드에서도 편집 동작 (독립성 증명)

상업 벤치마크: Gamma/Pitch의 슬라이드 단위 스코프 리파인 + 승인/되돌리기 UX [6].

워커 배정: codex가 이식과 서버, opus가 편집 결과 시각 판정, sonnet이 API 통합 테스트, fable이 격리 규정 점검.

테스트 전략: 편집 시나리오 골든 케이스, 격리 환경 스모크, 비생산경로 HTML 입력 케이스,
편집 후 재compose 차단(--discard-edits 없는 덮어쓰기 거부) 케이스.

### P10. deck-storyline — 소스 수집과 내러티브 설계

목적.
"한 문장 브리프"와 실제 발표 덱 사이의 공백을 메운다 —
브리프를 근거 자료로 확장하고(source ingest), 인용할 사실을 주장 테이블로 정리하고,
스토리 순서를 결정해 outline.md를 만든다. deck-copy와 deck-charts가 이 산출물을 소비한다.

입출력 계약.
- 입력: 공통 envelope(2.3) + 브리프 + 사용자 제공 원자료(문서/URL/데이터, 선택)
- 출력: source-pack.json(수집 원자료 목록 + 라이선스 + 수집 시각) +
  claims.json(주장 테이블: id, text, sourceIds[], confidence) +
  outline.md(titles test를 통과하도록 설계된 슬라이드 시퀀스)
- privacyMode(2.3)가 sensitive 이상이면 외부 검색·수집을 차단하고 사용자 제공 자료만 사용

기존 자산 재사용 vs 신규.
- 재사용: deep-research 하니스의 팬아웃 수집·적대 검증 패턴을 소스 수집 단계에 차용.
- 신규: claims 테이블 스키마 검증기, 아웃라인의 titles test 사전 린트(제목 시퀀스 논지 검사),
  주장-출처 커버리지 검사기(출처 없는 수치 주장 검출).

정량 합격기준.
- outline.md의 모든 수치 주장이 claims.json 항목과 연결 — 미연결 수치 0건 (스크립트 검사)
- claims의 모든 sourceIds가 source-pack 실존 항목을 가리킴 — 댕글링 참조 0건
- 타이틀 테스트 사전 린트 통과 (본 검증은 P6/P8에서 반복)
- 압축 팩트체크(P6과 동일 프로토콜): 원자료 대비 claims 왜곡 0건 — opus 대조 판정 (5.4)

워커 배정: codex가 스키마 검증기·커버리지 검사기, opus가 내러티브 구조와 팩트 판정,
sonnet이 검증기 케이스 테스트, fable이 수집 경계(privacyMode) 점검.

테스트 전략: 골든 브리프 → 골든 outline 스냅샷, 출처 누락/왜곡 주입 음성 케이스.


## 5. 품질 게이트 체계

3단 게이트. 상위 게이트는 하위 게이트 통과를 전제한다.

### 5.1 스킬 단위 게이트 (리포별)

skill-forge의 stages.json 게이트를 각 리포에 이식.
- 정적: 스키마 검증, 린트, SKILL.md 500줄 미만, references 상호배타 확인
- 기능: sonnet 작성 테스트 전부 green, 골든 산출물 스냅샷 일치
- 적대: opus가 경계 입력/모호 브리프로 공격, 발견 결함은 테스트로 고정 후 재통과
- 단독 상업 완성도: 1.3의 "단독으로도 상업성 있는 수준" 주장을 게이트로 조작화 —
  (a) 상류 매니페스트 없이 기본 설정으로 콜드런한 산출물이 해당 리포의 품질 바 통과
  (토큰 없이 기본 팔레트로 동작하는 경로도 기본 산출물이 대비 검증 등 품질 하한을 넘어야 함),
  (b) README + 실행 예제 + 대표 입력셋 + 예제 갤러리(before/after 포함) + known limitations 문서 완비,
  (c) 대표 실패 입력(잘못된 스키마, 엔진 미설치)에 대한 명확한 오류 안내 확인.
  마일스톤 분리: 이 게이트는 리포 초도 통과 조건이 아니다 —
  초도 마일스톤은 정적/기능/적대 게이트 + 코어 파이프라인 통과까지이고,
  단독 상업 완성도(standalone polish)는 독립 리포 승격(3절)과 Phase 5 완료의 조건으로
  별도 마일스톤에 둔다 (전 리포 초도 게이트화는 출시를 늦춘다)
- 각 파이프라인의 4절 정량 합격기준이 이 게이트의 통과 조건

### 5.2 파이프라인 통합 게이트

- 계약 게이트: 상류 산출물(tokens.json 등)을 실제로 소비해 다음 층이 동작 — 매니페스트 필드명 호환 CI
- 크로스 검증: deck-charts 산출 SVG를 deck-assembler가 임베드해 렌더했을 때 폰트/색 일치
- 바인딩 게이트: deck-plan.json의 모든 binding.contentRef가 실존 콘텐츠/에셋을 가리키고
  슬롯 kind·arity 규칙(2.3: bullets↔body, motion↔media, durationMs/fps 존재)과 정합하는지,
  차트-출처 페어링(2.3)과 transform 필드의 kind 제약(이미지/미디어 전용)을 지키는지 검사
  (댕글링 참조 0건, kind 불일치 0건)
- 환경 게이트: doctor 스크립트를 프로파일로 분할한다 —
  core(Chromium, 폰트), charts(Kroki 컨테이너·엔진 의존성), motion(FFmpeg, LaTeX),
  imagery(생성기 자격증명), editor(격리 환경).
  해당 덱이 실제로 사용하는 기능의 프로파일만 hard gate로 요구한다 —
  차트·모션 없는 덱이 LaTeX/Kroki 부재로 실패하는 일이 없어야 한다

### 5.3 최종 덱 채점기 (deck-grader, 구현은 P8)

컨설팅 품질 리서치의 31개 규칙을 HTML 파이프라인에 맞게 이식하고 [7],
접근성 규칙군(slide-html 접근성 규약: img alt, SVG title/desc, 장식 표시, 시맨틱 table,
읽기 순서 — 2.3)을 추가한다.
접근성 규칙은 별도 카테고리를 늘리지 않고 기존 6개 카테고리에 배속한다 —
명암비·장식 표시는 컬러, alt/title·시맨틱 table·읽기 순서는 구조 카테고리
(채점 스펙의 "6개 카테고리 가중치 합 100"과 정합 유지).
python-pptx 대신 1차 경로는 DOM + Playwright computed style이고,
PPTX 산출물 검증과 이미지 전용 산출물에는 python-pptx / OCR+CV 폴백 경로를 둔다.

구조 (3단).
1. 구조 파서: 슬라이드별 제목/본문 텍스트, 텍스트 런의 computed font-size/family/color,
   요소 bounding box, 차트 메타를 JSON 추출
2. 규칙 채점: 규칙별 독립 함수, 슬라이드별 pass/fail + 근거 수치 반환.
   임계값은 grader.yaml로 프로젝트별 오버라이드 (수치가 업계 컨센서스 근사치이므로 하드코딩 금지 [7])
3. 종합: 카테고리(구조/타이포/컬러/정렬/데이터시각화/신뢰성) 가중합 + hard fail 즉시 반려

채점 스펙 (grader.yaml 기본값으로 고정 — 이것 없이는 종합점수 산출 불가).
- 카테고리 가중치: 6개 카테고리 가중치의 합 100. 초기값은 P8에서 확정해 YAML에 기록
- 규칙별 점수: 규칙마다 만점과 감점 함수(위반 건수·정도 기반)를 정의
- 집계식: 규칙 점수 → 카테고리 정규화(0~100) → 가중합
- 캘리브레이션: 1단계는 synthetic 골든셋 + 자체 생성 덱으로 잠정 합격선 확정(Phase 2),
  2단계는 레퍼런스 덱 3~5벌 골든셋 채점으로 합격선 90의 상업 수준 대응 근거를 문서화
  (Phase 5 준비, P8 2단계화). 2단계 전의 90은 잠정값이며, 조정 시 YAML에 이력을 남긴다
- 31규칙 매핑표: consulting-quality 후보 규칙 → grader 규칙의 대응을 deck-grader docs 부록으로 고정

hard fail 항목 (기본값, 7종).
- 본문 폰트가 설정된 하한(grader.yaml body floor, 기본 24pt) 미만 —
  하한은 1.2의 오버라이드 범위(절대 하한 18pt 이상) 안의 설정값을 따른다.
  24pt는 기본값일 뿐 하드코딩이 아니다 (1.2 오버라이드 규정과의 문구 충돌 제거)
- 텍스트가 슬롯을 넘쳐 축소(autofit류)로 하한 미만 렌더 —
  computed font-size 기준 검사라 축소 경로와 무관하게 검출 (consulting-quality 규칙 28 [7])
- 수치 포함 슬라이드의 출처 라인 부재, 또는 차트 sourceRef가
  claims.json/source-pack.json의 실존 id를 가리키지 않는 댕글링 (sourceRef 무결성, 2.3/P8)
- 명암비 미달 (4.5:1 / 3:1)
- 차트 3D 효과 존재
- 자산 계약 위반 (원격 URL, 절대경로 — 폰트 파일 포함)
- 의미론 게이트 불합격 (아래 의미론 hard 게이트 명세)

의미론 hard 게이트 (액션 타이틀 결론성, MECE, 원 메시지).
덱의 실질 품질을 담보하는 유일한 항목이므로 soft로 두지 않는다 —
기계검사(타이포/컬러/정렬)만 통과해서 90점·hard fail 0을 달성하는 경로를 구조적으로 차단한다.
- 1차 필터: 대리지표 스크립트 규칙 — 라벨형 제목 패턴, 등위접속사+이중 서술어,
  MECE 대리지표(Other 카테고리 15% 미만, 카테고리 라벨 어휘 중복, 부분합-합계 일치) [7].
  1차 필터 위반은 즉시 fail. 단 1차 통과는 게이트 통과가 아니다 — 2차 LLM 심사로 넘어가는 조건일 뿐
- 2차 LLM 심사 프로토콜 (5.4 전면 적용):
  - 루브릭: 항목별 앵커드 루브릭 3종을 grader 리포에 텍스트 파일로 고정 —
    액션 타이틀 결론성(1: 토픽 라벨 ~ 5: 완결 결론문+본문 증거와 정합),
    MECE(1: 구획 중복·누락 명백 ~ 5: 상호배타·전체포괄), 원 메시지(1: 결론 다수 혼재 ~ 5: 슬라이드당 결론 1개)
  - 복수 심사: 슬라이드당 독립 컨텍스트 3회 판정, 다수결 (5.4 다표본 규정)
  - 불합격 기준 (grader.yaml 기본값, hard fail 판정식):
    (a) 타이틀 테스트(제목 시퀀스만으로 스토리 재구성) 덱 단위 실패,
    (b) 3항목 중 어느 하나라도 다수결 점수 3 미만인 슬라이드가 본문 슬라이드의 20% 초과,
    (c) 단일 슬라이드에서 만장일치 1점 존재.
    셋 중 하나라도 성립하면 hard fail — 슬라이드별 점수·판정 근거는 grade-report에 기록
  - 판정자 자격: 5.4의 사전 검증(캘리브레이션 셋 다수결 일치율 90%)을 통과한 판정자만 투입.
    미달 시 이 게이트는 soft로 강등하지 않는다 — 사람 판정으로 승격해 hard 게이트를 유지한다
    (의미론 3항목은 5.4의 soft 강등 규정의 예외)
실행 모드와 게이트 3층 분류 (무인 파이프라인 보장).
게이트를 결정론 게이트(기계검사 hard fail 6종: 폰트/축소 렌더/출처/명암비/3D/자산),
의미론 게이트(LLM 심사 3항목), 릴리스 리뷰(사람 최종 승인)의 세 층으로 분리한다.
- attended 모드(기본): 세 층 전부 hard — 판정자 미달 시 사람 판정 승격 규정(5.4)이 동작한다
- unattended 모드(CI/CLI 무인 실행): 결정론 게이트만 hard fail로 즉시 반려하고,
  의미론 게이트 불합격 또는 판정자·사람 부재는 파이프라인을 멈추지 않는다 —
  grade-report와 deck-plan에 needsHumanReview=true를 기록하고
  종료 코드 review-required로 끝나며,
  익스포트는 deck-manifest의 exportStatus=draft·reviewRequired=true(2.3)로 표기해
  draft 격리 규약(exports/draft/ + -draft 접미사)대로만 산출한다.
  deck-plan에 releaseBlocked=true 슬라이드가 있는 경우(오버플로 해소 실패 터미널, P7)도
  동일하게 review-required 종료 + draft 강등이며 final 경로는 열리지 않는다.
  릴리스(최종 전달) 승인은 사람 리뷰 없이는 성립하지 않는다 —
  attended 모드에서 releaseBlocked 슬라이드는 사람이 에디터 마감(P9) 또는
  카피 수정 후 재plan을 거쳐 마킹이 해제돼야 final 익스포트가 가능하다.
  사람 승격 대기 상태로 export가 영구히 멈추는 무인 데드락을 이 모드가 제거한다
grader는 CLI 단독 실행 가능해야 하며 (grade-report.json 출력),
assembler의 익스포트 게이트와 오케스트레이터의 완료 판정이 이 리포트를 소비한다.

### 5.4 opus 판정 프로토콜 (모든 opus 게이트 공통)

opus 점수는 실행마다 흔들리므로, 스펙 없는 "opus N/5"는 측정 가능한 기준이 아니다.
게이트로 쓰는 판정은 아래를 전부 갖춘다.

- 앵커드 루브릭: 점수별 서술 기준(무엇이 3점이고 무엇이 4점인지)을 해당 리포에 텍스트 파일로 고정
- 고정 프롬프트: 판정 프롬프트를 scripts/prompts/에 버전 관리
- 사전 검증과 통과 임계값: hard 게이트의 판정자는
  기지의 합격/불합격 캘리브레이션 셋(각 10건 이상, P8 동결 골든셋에서 파생)에서
  다수결 일치율 90% 이상을 기록해야 hard 게이트로 투입한다.
  미달 시 해당 판정은 soft 참고치로 강등하고,
  그 게이트는 대리지표 스크립트 규칙으로 재구성하거나 사람 판정으로 승격한다.
  예외: 5.3 의미론 hard 게이트(액션 타이틀 결론성, MECE, 원 메시지)는 soft 강등이 금지된다 —
  판정자 미달 시 사람 판정으로 승격해서라도 hard 게이트를 유지한다 (5.3 명세).
  unattended 모드에서는 사람 승격이 불가능하므로 5.3의 needsHumanReview 종료 규약이 우선한다
  임계 미달 판정자를 hard 게이트에 쓰는 것을 금지 — 측정만 하고 투입하는 로깅은 게이트가 아니다
- 다표본 다수결: 단발 판정 금지, 홀수 표본(기본 3회) 다수결로 분산 억제
- soft 지표는 grade-report에 참고치로만 기록하고 게이트에서 분리
- 판정 호출 횟수와 비용은 7절의 런별 기록에 포함해 가시화

적용 대상: P1 스타일 타일, P2 템플릿 시각 판정, P3 한글 렌더 판정, P4 3b1b 스타일 판정,
P5 무드/브랜드 적합, P6 타이틀 테스트·압축 팩트체크, P8 의미론 2차 판정,
P10 claims 팩트체크, Phase 5 블라인드 비교.


## 6. 실행 로드맵

Phase 0. 기반 (선행, 짧게)
- deck-contracts 스키마 v1 확정
  (deck-constants.json 상수 단일 소스와 sync/diff 방식,
  layout-manifest.json의 capacity/capacityFloors,
  deck-plan.json(needsHumanReview/rejectCount/releaseBlocked),
  deck-manifest.json(exportStatus/reviewRequired/releaseBlocked + draft 격리 규약),
  copy-reject.json(attempt 카운터)·copy.json(rejectAttempt),
  measured-overflow.json, image-reject.json, edit-manifest.json, 공통 입력 envelope,
  슬라이드 HTML 산출물 계약(DOM 규약 + slide-html 검증 스크립트 + 접근성 규약) 포함).
  단 v1 "확정"은 필드 동결이 아니라 초안 동결이다 —
  capacity·overflow·slide DOM·editor 계약은 세로 슬라이스 PoC를 통과해야 안정되므로,
  스키마 안정 판정(2회 연속 마일스톤 무변경)은 인큐베이션 기간에 한다 (3절 승격 기준)
- 인큐베이션 리포 스캐폴딩: 리포 분할(3절)을 바로 실행하지 않는다.
  단일 인큐베이션 리포의 packages/ 구조로 레이어 경계를 유지하며 개발하고,
  contracts → tokens → layouts → copy → assembler(plan/compose) → grader의
  최소 세로 슬라이스 E2E 1벌을 이 리포 안에서 먼저 관통시킨다 (skill-forge 러너 재사용).
  독립 리포 승격은 3절 승격 기준 충족 시점에 패키지 단위로 수행한다
- vendored 스키마 동기화 방식 확정: 각 리포는 deck-contracts의 버전 태그를 핀한
  sync 스크립트로 사본을 가져오고, CI가 핀 태그 원본과 diff 검사.
  이 방식(스크립트 + 태그 핀)이 동작하는 것까지가 완료 조건
- deck-grader 뼈대: 파서 + 기계검사 hard fail 6종 + grader.yaml 골격(치수·하한 섹션은
  deck-constants sync로 생성) — 이후 모든 Phase의 심판이므로 최우선.
  의미론 hard 게이트(7번째, 5.3)는 LLM 심사 프로토콜이 필요하므로 Phase 2 규칙군 2차에서 투입.
  종합점수 산출은 완료 정의에 넣지 않는다 (채점 스펙과 캘리브레이션이 확정되기 전이므로)
- 레퍼런스 골든셋의 출처·포함기준 확정과 동결 (P8 조달 기준) —
  Phase 5 판정자 검증과 2단계 캘리브레이션(P8)이 이 셋에 매달리므로 기준은 여기서 고정하되,
  HTML 리빌드 등 무거운 조달 작업은 하지 않는다 (리빌드는 Phase 5 준비로 이연)
- 라이선스 확인 잔여 작업 처리 (8절: Montage, KRDS, decktape 등).
  TossFace는 원본 무수정 재배포가 저작권 안내 동봉 조건으로 허용됨이 원문 대조로 확인됐으므로 [1],
  잔여 작업은 LICENSE 고지 파일 동봉과 수정 금지 준수 확인뿐이다 (1.2).
  gpt-image-2 생성물의 상업적 사용 약관 확인을 체크리스트에 포함 (단독 상업 완성도 주장과 정합)
- 검증 근거 영속화: hyperframes·slides-grab 로컬 clone을 커밋 해시 핀으로 재클론해
  영속 위치에 보존 (현재 근거가 세션 휘발성 scratchpad에 있음)
- 완료 정의: 스키마 CI green(동기화 방식 포함), grader가 샘플 HTML 덱에 hard fail 검사를 실행해 리포트 산출,
  골든셋 동결 문서 존재

Phase 1. 파운데이션 (P1 + P2 + grader 규칙군 1차)
- deck-tokens 프리셋 8종 이상 (기존 5 + 국내 3), deck-layouts 템플릿 20종
  (capacity 실측 역산과 capacityFloors 산출 포함)
- deck-grader 규칙군 1차 구현: 타이포/컬러/정렬 — P1/P2 산출물 검증에 즉시 필요
- 완료 정의: 4절 P1/P2 합격기준 전부 통과, 해당 규칙군 골든 리포트 스냅샷 일치,
  토큰 → 레이아웃 → grader 관통 데모 1건

Phase 2. 생성기 병렬 (P3 + P5 + P6 + grader 규칙군 2차, 상호 독립이라 동시 진행)
- codex 워커를 리포 단위로 분산 (deck-charts MVP 4엔진 어댑터 + 확장분이 최대 병렬 지점, P3)
- deck-grader 규칙군 2차: 데이터시각화/신뢰성/접근성 + 의미론 hard 게이트
  (5.3 — 루브릭 3종 고정, 판정자 사전 검증, 불합격 판정식) + 채점 스펙(가중치·배점·집계식) 확정 +
  1단계 캘리브레이션(synthetic HTML 골든셋 + 자체 생성 덱, P8 — 잠정 합격선 90 기록) —
  Phase 3의 90점 게이트 선행 조건.
  공개 레퍼런스 덱 HTML 리빌드와 2단계 캘리브레이션은 Phase 5 준비로 이연 (P8 2단계화)
- deck-storyline(P10)도 이 Phase에서 병렬 구현 — deck-copy가 outline/claims를 소비하므로 P6보다 선행 착수
- P4 deck-motion은 PoC 게이트(5초 MP4 관통)만 이 Phase에서 수행, 본 빌드는 분리
- 완료 정의: 각 파이프라인 합격기준 통과 + tokens.json 소비 크로스 검증 통과 +
  grader가 종합점수를 산출 가능한 상태 (P8 합격기준 중 캘리브레이션까지)

Phase 3. 조립기 (P7) + 에디터 (P9)
- slides-grab 이식 → plan/compose 조립기 → 익스포터 순. deck-editor는 조립기와 독립이므로 병행 진행
- 완료 정의: 골든 매니페스트 + 골든 deck-plan으로 E2E 덱 1벌 산출,
  1단계 캘리브레이션 완료된 grader 기준 90점 이상(잠정 합격선), 시각 QA 루프 1회 완주,
  오버플로 해소 루프 3분기(대체 레이아웃/반려/kind별 터미널) 케이스 통과, deck-editor 왕복 편집 1회.
  골든 매니페스트로 착수를 앞당긴 경우, 캘리브레이션 확정 전에는
  조립 기능 완료(결정론 diff 0 + hard fail 0 + 해소 루프 케이스 통과)까지만 인정하고
  Phase 3 완료 선언은 Phase 2의 1단계 캘리브레이션 종료 후에만 한다

Phase 4. 모션 본 빌드 (P4) + 오케스트레이터 (L3)
- deck-motion 본 구현, deck-factory 얇은 라우터 + 가드
- 완료 정의 1차(선행): motion 자산이 전혀 없어도 브리프 1줄 → 최종 덱 E2E가 완결됨을 먼저 보장
  (deck-motion은 옵셔널 플러그인 — P4 포지셔닝, doctor motion 프로파일 미설치 환경 포함)
- 완료 정의 2차: 브리프 1줄 → 최종 덱 + MP4 컷 포함 E2E, 사람 개입은 아웃라인 검토와 에디터 마감만.
  MP4는 3급 베스트 에포트 등급(1.2)이므로,
  hyperframes 파손 시 manim 클립 ffmpeg concat 폴백 MP4로도 완료를 인정한다 (8절 완화책과 정합)

Phase 5. 상업성 검증과 마감
- 준비: 공개 레퍼런스 덱 골든셋 HTML 리빌드(3벌, 벌당 공수 명시)와 2단계 캘리브레이션(P8) —
  합격선 90의 상업 수준 대응 근거를 이 시점에 확정하고, 조정 시 이력을 남긴다
- 실제 발표 주제 3건으로 덱 생산, Gamma/Beautiful.ai 산출물과 블라인드 비교
- 블라인드 비교 프로토콜 (착수 전 스펙 고정, 5.4 프로토콜 준수):
  - 조달: 유료 계정으로 동일 브리프 3건을 Gamma/Beautiful.ai에 투입해 비교 덱을 생성·확보.
    계정 비용과 생성 절차를 실행 문서에 기록.
    조달 조건에 privacyMode 게이트(2.3 공통 envelope)가 직접 걸린다 —
    외부 서비스 투입은 privacyMode=public 브리프 또는
    민감 정보를 제거·치환한 sanitized synthetic 브리프만 허용하고,
    sensitive/confidential 브리프는 벤치마크 경로 자체가 차단된다.
    실제 발표 주제가 sensitive 이상이면 동등 난이도의 synthetic 브리프로 대체 투입하고
    대체 사실과 sanitize 절차를 실행 문서에 기록한다
  - 블라인드화: 모든 덱을 공통 렌더 포맷(슬라이드별 PNG, 동일 해상도)으로 정규화해
    툴 고유의 뷰어/브랜드 지문을 제거
  - 루브릭: 차원별(구조, 타이포, 컬러, 데이터, 전체 완성도) 앵커드 루브릭 + 페어와이즈 강제선택
  - 표본: 세 트랙으로 분리한다 —
    (a) 슬라이드 단위 페어와이즈(최소 30쌍)는 slide role(커버/본문/차트/클로징)과
    덱 내 위치(index)를 맞춘 쌍만 비교해 서사 맥락 소실을 통제,
    (b) 덱 단위 전체 평가(3건 페어와이즈),
    (c) 핵심 슬라이드 subset(각 덱의 최중요 3장) 평가.
    판정 반복 수(쌍당 3회 다수결)와 최소 표본 수를 착수 전 프로토콜에 고정
  - 통과선: 페어와이즈 선호율 50% 이상(동급 판정), 차원별 평균 격차를 함께 기록.
    신뢰구간은 슬라이드 쌍이 덱에 중첩된 클러스터 구조임을 반영해 산출한다
    (덱 클러스터 효과 무시 금지) — 통과선 판정의 변별력을 명시
  - 판정자 검증: P8 동결 골든셋에서 파생한 우수/열위 덱 쌍으로 판정자의 변별력을 사전 확인해
    자기평가 편향을 통제 (5.4 임계값 적용), 판정은 다표본 다수결
- MBB 스타일 체크리스트 블라인드 평가 (1.3의 MBB 스타일 적합 주장을 측정하는 트랙):
  - 체크리스트: consulting-quality [7]에서 도출한 MBB 스타일 항목
    (액션 타이틀 결론성, 피라미드 시각 위계(제목>부제>본문 크기·색 위계), MECE, 원 메시지,
    타이틀 테스트, 직접 라벨링)을 항목별 앵커드 루브릭으로 착수 전 고정
  - 입력: 위 블라인드 비교와 동일한 정규화 PNG 셋 (툴 지문 제거 상태에서 채점)
  - 판정: 5.4 사전 검증을 통과한 판정자가 항목별 pass/fail 채점, 항목당 3회 다수결
  - 통과선: 자사 덱 3건 전부에서 체크리스트 항목 통과율 90% 이상 + 타이틀 테스트 덱 단위 통과.
    미달 항목은 grader 규칙·deck-copy 린터·템플릿으로 환류
  - 보고: 통과율 수치와 항목별 실패 목록만 보고 (등급 표현 금지)
- 미달 항목을 grader 규칙 또는 템플릿 개선으로 환류
- 완료 정의: 3건 전부 hard fail 0, 블라인드 비교 통과선 충족,
  각 스킬 단독 트리거 시나리오(2.2절)와 단독 상업 완성도 게이트(5.1) 전부 통과

의존성 요약: Phase 0 → 1 → {2, 3은 2의 산출물 일부만 있어도 착수 가능(골든 매니페스트로 대체)} → 4 → 5.
단 Phase 3의 90점 게이트는 Phase 2의 grader 채점 스펙 확정·캘리브레이션 완료에 의존한다.
P4 PoC는 Phase 2에 앞당겨 리스크를 조기 노출한다.


## 7. 컨텍스트 예산 전략

- progressive disclosure 3레벨 준수 [8]: description은 트리거 판단용으로 타이트하게,
  SKILL.md 500줄 미만 라우터, 상세는 상호배타 references (언제 읽는지 포인터 명시, 300줄+엔 목차)
- 결정적 작업(렌더, 검증, 팩/스냅샷)은 전부 scripts/로 — 토큰 생성 대신 코드 실행
- 서브에이전트 분업: 대량 생성(차트 엔진, manim 씬, 이미지 배치)은 codex-spawn/codex-imagegen으로 팬아웃,
  작업별 디렉토리 격리로 레이스 방지, 메인 컨텍스트는 매니페스트 요약만 수신
  (요약 상한: 매니페스트당 30줄 또는 4KB 중 작은 쪽 — 초과분은 파일 경로로 대체)
- 시각 QA는 반드시 신선한 눈 서브에이전트 (만든 에이전트는 기대한 것을 보게 됨 [8])
- 파일 핸드오프 규약: 모든 층간 데이터는 deck-contracts 스키마 파일로만,
  각 스킬 진입 시 존재/스키마 검증 가드로 순서 오류 조기 실패
- 빌드 시에도 동일 원칙: 워커에게는 스펙 파일 경로 + 산출 경로만 주고, 결과는 파일로 회수 (skill-forge 플레이북)
- 런별 total_tokens/duration 기록으로 비용 가시화 (skill-creator timing.json 패턴 [8]).
  opus 판정 게이트(5.4)의 호출 횟수·다표본 배수도 같은 로그에 포함해 판정 비용을 예산화
- 워커 실행 계획은 WORKERS.md 참조


## 8. 리스크 레지스터

| 리스크 | 근거 | 완화책 |
|---|---|---|
| TDS Figma Kit/npm을 자산으로 오인해 포팅 | 앱인토스 전용 라이선스, 수정·재배포 금지 [1] | 코드/컴포넌트 도입 전면 금지, 원칙만 토큰으로 재구성. P1 게이트에 라이선스 체크리스트 |
| Toss Product Sans 무단 배포본 사용 | 공식 다운로드 경로 없음, 3rd-party 배포본 신뢰 불가 [1] | Pretendard로 대체. 폰트 등록 시 라이선스 필드 필수화로 차단 |
| TossFace 라이선스 고지 누락 또는 수정본 배포 | 커스텀 라이선스, 수정 금지 — 원본 무수정 재배포는 저작권 안내 동봉 조건으로 허용 확인됨 [1] | 무수정 원본만 ./assets/fonts/ 번들 + LICENSE 고지 파일 동봉 (1.2). 수정·파생 폰트 제작 금지, Phase 0 체크리스트로 준수 확인 |
| 폰트 CDN 로드가 자산 계약과 충돌 | 원격 URL 금지 계약 + 오프라인 발표장 요건 | 전 폰트 로컬 번들 원칙으로 일원화 (1.2), grader 원격 URL 검사에 폰트 포함 |
| slides-grab 스타일 데이터 90/95종 라이선스 미확인 | corazzon/epoko77-ai 파생 [4] | 스타일 데이터는 이식하지 않음. 필요 시 원본 라이선스 확인 후 별도 결정 |
| slides-grab 에디터의 샌드박스 우회 실행 | codex --dangerously-bypass..., claude acceptEdits [4] | 에디터를 deck-editor 리포로 분리, 로컬 격리 환경 전용, CI/서버에서는 컨테이너 격리. README의 star 요청 지시 제거 |
| god-tibo-imagen 비공식 백엔드 파손 | 사설 Codex 백엔드, 예고 없이 깨짐 [4] | 기본 프로바이더로 채택하지 않음. codex-imagegen 경로 + API 키 폴백 명시 |
| manim 의존성(LaTeX 수GB, Cairo)과 WSL/GPU 제약 | ManimGL OpenGL 의존, OOM 경고 [5] | CE 기본 + GL 옵션화, doctor 게이트, PoC 선행, 렌더 동시성 하향 |
| hyperframes 신생(v0.6~0.7) API 변동, 시크 결정론 | library-clock 요구, 버전 변동 [5] | 버전 핀, GSAP 등 지원 어댑터만 사용, 결정론 해시 테스트, 로컬 render만 사용(cloud 경로 금지). 파손 시 manim 클립 ffmpeg concat으로 3급 MP4 폴백 |
| 한글 폰트가 차트 렌더러에서 깨짐 | 전 렌더러 미검증 [9] | Phase 2 착수 시 한글 골든 렌더 PoC를 엔진별 첫 작업으로. 실패 엔진은 기준 완화 대신 채택 제외 + 폴백 라우팅 갱신 (P3 분기) |
| Kroki 퍼블릭 인스턴스로 데이터 유출 | 슬라이드 데이터 외부 전송 [9] | 자체 호스팅 Docker 강제, 퍼블릭 엔드포인트는 코드에서 차단 |
| Graphviz EPL-2.0 (T0-6 원문 확인), ApexCharts 듀얼 라이선스 | 약한 카피레프트 / 매출 조건 [9] | Graphviz는 서브프로세스 호출만(링크 금지), ApexCharts 미채택 유지 |
| MBB 수치가 공식 규정이 아님 | 2차 자료 재구성 [7] | grader 임계값 전부 YAML 설정화, 문서에 근사치임을 명기, 레퍼런스 골든셋 캘리브레이션으로 보정 (P8) |
| 폰트 하한을 프레임워크가 강제 안 함 (Marp류 함정) | [6] | 템플릿 카탈로그(폰트 축소 금지 불변식) + grader hard fail(축소 렌더 포함, 5.3의 7종)의 이중 방어. 하한값 정본은 deck-constants.json 단일 소스(2.3). LLM에 자유 CSS 비허용 |
| 콘텐츠 과다 시 autofit식 축소로 작은 글씨 재발 | consulting-quality 규칙 28 [7] | 폰트 축소 전면 금지 불변식(1.2) + P7 plan 해소 루프(대체 레이아웃/반려/kind별 터미널 — 강제 분할 또는 releaseBlocked 마킹) + capacity 실측 역산 + Playwright 실측 렌더 게이트로 봉인 |
| 글자 수 기반 상한이 비례폭·한영 혼용에서 수용량을 오판 | Pretendard 비례폭, 스크립트별 폭 상이 | 수용량 계약을 스크립트별 advance-width 예산으로 정의(2.3), 글자 수는 힌트로 격하, 최종 게이트는 렌더 실측(템플릿은 P2, 덱은 P7 compose 실측 게이트) |
| plan 추정(advance-width 합산)과 compose 실측 렌더의 이음매에서 오버플로 누출 | 추정은 렌더 엔진의 줄바꿈·커닝을 완전 재현하지 못함 | 책임 분리 규약(P7): capacityMargin 보수화 + compose 실측 게이트 + measured-overflow.json 반환 → plan 강제 분할 재계획(재왕복 1회 상한) + 발생분 P2 capacity 보정 환류 |
| 오버플로 반려 루프 무한 왕복 또는 데드락 | 팩트보존·비축소·압축불가가 동시 성립하는 케이스 | 카운터를 파일 계약에 영속(copy-reject attempt·copy.json rejectAttempt, attempt>2 스키마 위반, 2.3) + kind별 터미널(body 강제 분할, title/source는 releaseBlocked 마킹 — final 익스포트 차단·draft 강등, 2.3/P7) + 분할 경로 전 템플릿 필수(P2) + needsHumanReview/rejectCount/releaseBlocked 기록 |
| anthropics/skills 일부 스킬(docx/pptx/xlsx/pdf)이 Proprietary | 리서치가 문구 자체 재작성 권고 [8] | 규정과 아이디어만 참고해 자체 재작성, 원문 문구 이식 금지 (P7 시각 QA 루프 포함) |
| 레퍼런스 골든셋과 파이프라인 산출물의 채점 척도 불일치 | grader 1차 경로는 HTML, 레퍼런스는 PPTX/PDF | 골든셋 3벌 HTML 수작업 리빌드로 동일 척도 채점 + 폴백 경로 부분집합 교차 확인 (P8) |
| 네거티브 스페이스 프롬프트 수율 낮음 | 커뮤니티 미해결 이슈 [10] | 배치 생성 + 구도 필터 + 후처리(오버레이/블러)를 파이프라인에 내장, 수율 60% 기준 관리 |
| Astryx Beta 파괴적 변경, MCP 외부 의존 | 0.1.2, Meta 호스팅 [2] | 토큰 증류만 하고 런타임 의존 없음. MCP는 참고 조회용으로만, 하드 의존 금지 |
| PPTX/Figma 익스포트 신뢰 불가 | 실험적 명시 [4][6] | 3급 베스트 에포트로 등급 분리, 합격기준에서 제외, 문서에 한계 명기 |
| 미확인 라이선스 잔여 (Montage, KRDS 공공누리 유형, decktape, awesome-gpt-image-2, hands-on-deck) | [3][6][7][10] | Phase 0 체크리스트로 일괄 확인, 확인 전 해당 자산 미사용. 확인 실패 시 대체재(자체 구현/미채택)로 진행 |
| 개조식 마침표 세부 규정 원문 미열람 | 나무위키 스니펫만 확인 [10] | deck-copy 규칙 확정 전 원문 재확인, 그 전까지는 서술형 개조식 관행 기본값만 적용 |
| Simplicity 발표자료 다운로드 오인 | 공식 배포 미확인 [1] | 영상 참고만, 자산화 금지 |
| opus 판정 드리프트로 게이트 재현성 붕괴 | 실행별 점수 변동 | 5.4 프로토콜(앵커드 루브릭, 고정 프롬프트, 사전 검증, 다표본 다수결)로 통제, soft 지표는 게이트 분리 |
| 채점기 의미론 항목 오탐/미탐 | MECE 등은 대리지표 [7] | 대리지표 1차 필터 + LLM 3회 다수결 hard 게이트(5.3 루브릭·불합격 판정식 고정) + 판정자 사전 검증, 미달 시 사람 판정 승격(soft 강등 금지) |
| 매니페스트 필드명 드리프트로 조용한 깨짐 | skill-creator가 명시한 함정 [8] | deck-contracts 단일 소스 + 각 리포 vendored 사본 diff CI |


## 9. 출처

1. /home/seunghyeong/deck-factory/research/toss-design.md — 토스 공식 디자인 자산 전수 조사
2. /home/seunghyeong/deck-factory/research/astryx.md — Meta Astryx 디자인 시스템 조사
3. /home/seunghyeong/deck-factory/research/korean-design-systems.md — 한국 기업 공개 디자인시스템 서베이
4. /home/seunghyeong/deck-factory/research/slides-grab.md — NomaDamas/slides-grab 코드 구조 분석
5. /home/seunghyeong/deck-factory/research/manim-video.md — manim_skill + hyperframes 영상화 파이프라인
6. /home/seunghyeong/deck-factory/research/deck-frameworks.md — HTML/CSS 프레젠테이션 프레임워크 및 상용 AI 덱 UX
7. /home/seunghyeong/deck-factory/research/consulting-quality.md — 컨설팅 덱 품질 원칙의 기계 채점 체크리스트
8. /home/seunghyeong/deck-factory/research/skill-architecture.md — Claude 스킬 레이어드 아키텍처 베스트 프랙티스
9. /home/seunghyeong/deck-factory/research/chart-libs.md — 도표 오픈소스 16종 서베이와 채택 10종
10. /home/seunghyeong/deck-factory/research/image-and-text.md — 이미지 프롬프트, 풀블리드 가독성, 카피라이팅 규칙

주요 외부 링크 (각 리서치 문서의 출처 목록에서 재인용).

11. https://github.com/toss/tossface — TossFace (커스텀 라이선스, 수정 금지)
12. https://github.com/orioncactus/pretendard — Pretendard (SIL OFL 1.1)
13. https://github.com/daangn/seed-design — 당근 SEED (Apache-2.0)
14. https://github.com/facebook/astryx — Astryx (MIT)
15. https://github.com/NomaDamas/slides-grab — slides-grab (MIT)
16. https://github.com/adithya-s-k/manim_skill — manim 스킬 팩 (MIT)
17. https://github.com/heygen-com/hyperframes — hyperframes (Apache 2.0)
18. https://github.com/vega/vl-convert — Vega-Lite 헤드리스 변환
19. https://apache.github.io/echarts-handbook/en/how-to/cross-platform/server/ — ECharts SSR
20. https://docs.kroki.io/kroki/setup/use-docker-or-podman/ — Kroki 자체 호스팅
21. https://github.com/anthropics/skills — 공식 스킬 리포 (Apache 2.0 / Proprietary 혼재)
22. https://github.com/scanny/python-pptx — 채점기 폴백 경로 (MIT)
23. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — WCAG 명암비 공식
24. https://github.com/marp-team/marp-cli — 익스포터 벤치마크 (MIT)
25. https://pmc.ncbi.nlm.nih.gov/articles/PMC8638955/ — 슬라이드 인지부하 논문 (CC BY 4.0)
