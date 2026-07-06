# critical

1. 2.3 layout-manifest / P2 / P7의 오버플로 계약이 서로 맞지 않음.

   문제: layout-manifest는 슬롯 overflow를 truncate|split으로 허용하지만, P2는 텍스트 콘텐츠 슬롯 전체에 split 경로를 필수화하고, P7은 split을 먼저 수행한 뒤 그래도 초과하면 copy-reject로 보낸다. 이러면 body overflow는 대부분 copy-reject에 도달하지 않고, title overflow는 불릿 경계 분할 규칙을 적용할 수 없어 "강제 연속 슬라이드 분할이라는 항상 성립하는 종료 폴백"이 성립하지 않는다. truncate도 텍스트 손실을 만들 수 있는데 감사 로그나 허용 대상이 없다.

   수정안: 슬롯 kind별 overflowAction을 고정하라. title은 rewrite/reject만 허용하고 split/truncate 금지, body/list는 rewrite 후 split 또는 split 후 rewrite 중 하나를 명시, source는 truncate 금지, caption만 lossy truncate 허용 여부를 별도 플래그와 로그로 관리한다. splitGranularity도 bullet|sentence|paragraph로 스키마에 넣고, copy-reject가 실제로 도달 가능한 순서로 P7 루프를 다시 쓴다.

2. P5 이미지 재조정 경로가 계약에 없음.

   문제: P5는 final layout 슬롯과 이미지의 네거티브 스페이스가 어긋나면 plan 단계가 크롭 오프셋 조정 또는 이미지 브리프 재요청을 한다고 쓰지만, image-manifest에는 path/kind/width/height/tokensRef/altText만 있고 deck-plan의 contentRef는 문자열뿐이다. crop, object-position, overlay, safe area, focal point를 표현할 곳이 없고 image-reject.json 같은 재요청 계약도 없다. 현재 계약으로는 P7이 이미지를 재배치하거나 재생성 요청을 파일 핸드오프로 전달할 수 없다.

   수정안: image-manifest에 focalBox, textSafeRegions, backgroundVariance, ocrFindings, recommendedCropCandidates를 추가한다. deck-plan의 slots 값을 단순 contentRef 문자열이 아니라 contentRef + transform 객체로 확장한다. 재생성이 필요하면 copy-reject와 대칭인 image-reject.json을 만들고 attempt 상한과 종료 폴백을 정의한다.

3. P3/P8 사이에 출처 계약이 끊겨 grader hard fail을 유발함.

   문제: P3 입력 chart-request.json에는 caption/source가 있지만 chart-manifest 계약에는 source, caption, units, data provenance가 없다. deck-plan contentRef도 chart asset만 가리킨다. 반면 5.3 hard fail은 수치 포함 슬라이드의 출처 라인 부재를 즉시 반려한다. 차트 기반 슬라이드는 assembler가 출처를 렌더할 안정적 근거가 없어 최종 grader에서 반복적으로 실패한다.

   수정안: chart-manifest.assets[]에 caption, sourceLabel, sourceUrl, retrievedAt, dataHash, units, caveat를 필수 또는 조건부 필수로 넣는다. deck-plan은 chart 슬롯과 source/caption 슬롯 바인딩을 함께 검증해야 한다. assembler는 차트가 숫자를 포함하면 source DOM을 자동 렌더하거나 명시적으로 deck-plan에 바인딩되지 않은 경우 plan 단계에서 실패시킨다.

4. P7의 deck-plan 단일 소스 주장과 P9의 HTML 직수정 방식이 충돌함.

   문제: P7은 deck-plan을 다운스트림의 단일 소스로 유지한다고 하지만 P9는 editor가 slides/*.html을 직접 수정한다고 한다. 편집자가 텍스트, 위치, 이미지, slot 속성을 바꾸면 deck-plan, copy.json, layout-manifest의 capacity, deck-manifest가 모두 stale이 된다. 이후 재채점, 재익스포트, 재compose 중 어느 경로가 진짜인지 불명확하다.

   수정안: 둘 중 하나를 선택하라. 첫째, editor를 final artifact editor로 정의하고 edit-manifest.json을 남기며 deck-plan/deck-manifest를 invalidated 상태로 표시한다. 이 모드에서는 재compose가 편집본을 덮어쓰지 못하게 한다. 둘째, editor를 structured patch editor로 바꾸고 모든 편집을 deck-plan/copy/tokens/layout override 패치로 기록한 뒤 compose가 다시 HTML을 만든다.

5. P3의 유형 x 엔진 100% 렌더 CI는 리서치 근거와 맞지 않아 그대로는 실패함.

   문제: P3은 30개 유형 x 10개 엔진 전 셀의 렌더 성공률 100%를 요구한다. 그러나 chart-libs 리서치 자체가 엔진별 역할을 분담했다. Chart.js는 기본적으로 PNG/canvas 경로이고, Cytoscape.js는 headless 좌표 계산 위주라 SVG 직렬화가 별도이며, D3는 최후 폴백으로 한정되어 있다. 모든 엔진이 모든 유형을 렌더해야 한다는 게이트는 지원 불가능한 셀 때문에 CI를 막는다.

   수정안: 매트릭스를 supported|required_fallback|not_applicable로 나누고, CI hard gate는 유형별 기본 엔진과 지정 fallback만 대상으로 삼아라. MVP는 Vega-Lite, ECharts, Mermaid, Graphviz 4개 엔진으로 시작하고, Plotly/Cytoscape/Chart.js/D3는 실제 수요가 있는 유형부터 확장한다.

# major

1. Phase 0에서 11개 리포와 스키마 v1을 먼저 고정하는 순서가 비현실적이다. 가장 불확실한 capacity, overflow, slide DOM, editor patch 계약은 P2/P7/P9 PoC를 돌려봐야 안정된다. Phase 0은 contracts/tokens/layout/copy/compose/grader 최소 세로 슬라이스를 한 리포에서 검증한 뒤, 스키마가 2회 이상 변경 없이 통과한 후 리포를 분할하는 순서로 바꿔라.

2. 11개 GitHub 리포 + vendored 검증 스크립트 + diff CI는 MVP에는 과잉 설계다. skill-architecture 리서치는 자기완결성 원칙을 보여주지만, 처음부터 모든 레이어를 별도 리포로 쪼개라는 근거는 아니다. packages/ 또는 apps/ 구조의 단일 인큐베이션 리포에서 경계를 유지하고, 외부 소비자가 생긴 계약만 독립 리포로 승격하라.

3. 의미론 hard gate가 자동 파이프라인을 막을 수 있다. 5.3/5.4는 판정자 검증 실패 시 사람 판정으로 승격한다고 하지만, CLI/CI 모드에서 사람이 없으면 export가 멈춘다. deterministic gate, semantic advisory, release review를 분리하고, 무인 실행에서는 hard fail이 아니라 needsHumanReview로 종료하는 명확한 모드를 둬라.

4. grader 캘리브레이션이 너무 무겁고 Phase 2에 많은 위험을 묶는다. 공개 IR/PDF를 HTML로 3벌 수작업 리빌드하고 OCR+CV 폴백까지 맞추는 작업은 grader 구현과 별도 프로젝트급이다. 먼저 synthetic HTML 골든셋과 자체 생성 덱으로 규칙을 안정화하고, 상용/공개 덱 리빌드는 Phase 5 검증 준비로 늦춰라.

5. 좌표계와 자산 경로가 모호하다. 계획은 1280x720 CSS px를 정본으로 두면서 slides-grab의 720pt/405pt, 960x540 bbox 좌표계를 호환한다고만 한다. 또한 ./assets/가 slides/*.html 기준인지 프로젝트 루트 기준인지 불명확하고, viewer.html은 "단일 파일"이라고 하면서 로컬 assets 폴더에 의존한다. deck-constants에 좌표 변환 공식과 assetRoot 기준을 명시하고, viewer는 single-html inline bundle 모드와 folder bundle 모드를 분리하라.

6. capacityFloors를 kind별 전 템플릿 최소값으로 두면 deck-copy가 가장 작은 슬롯 하나에 맞춰 모든 본문을 과도하게 줄인다. 템플릿 archetype 또는 slot role별 하한으로 나누고, copy 단계는 "보수적 기본 예산"만 보며 실제 fit은 plan이 담당하도록 완화하라.

7. 제목 슬롯 좌표를 모든 템플릿에서 슬라이드 너비 1% 이내로 고정하는 기준은 커버, 섹션 구분, 인용, 빅스탯 템플릿과 충돌한다. 이 규칙은 본문형 슬라이드의 action title에만 적용하고 cover/section/quote/stat 계열은 명시적으로 예외 처리하라.

8. 5.2 환경 게이트가 모든 E2E에 Chromium, FFmpeg, LaTeX, Kroki, 폰트를 전부 요구한다. 차트나 모션을 쓰지 않는 덱도 LaTeX/Kroki 때문에 실패할 수 있다. doctor를 core, charts, motion, imagery, editor 프로파일로 쪼개고 사용된 기능의 doctor만 hard gate로 삼아라.

9. deck-motion은 3급 베스트 에포트인데 구현 범위와 검증 기준은 1급 기능처럼 크다. Manim/Hyperframes는 환경 의존성이 크므로 core deck pipeline 밖의 optional plugin으로 두고, Phase 4 완료 조건도 MP4 포함 E2E가 아니라 "motion asset이 없어도 최종 덱이 완성되는가"를 먼저 보장하라.

10. P5의 이미지 수율 60%, OCR 문자 0건 기준은 근거보다 강하다. image-and-text 리서치는 네거티브 스페이스가 프롬프트만으로 해결되지 않는다고 말할 뿐 안정 수율을 보장하지 않는다. 초기에는 수율을 측정 지표로만 두고, 실패 시 stock/solid background/vector pattern 폴백을 계약에 넣어라.

11. 외부 서비스에 대한 데이터 경계가 부족하다. gpt-image 계열, Gamma/Beautiful.ai 벤치마크, 공개/자체 호스팅 렌더러는 모두 브리프와 데이터 유출 가능성이 있다. privacyMode를 두고 public/sensitive/confidential 입력별로 사용 가능한 생성기와 벤치마크 경로를 제한하라.

12. Phase 5 블라인드 비교는 슬라이드 단위 30쌍으로 표본을 늘리지만, 서로 다른 덱의 서로 다른 위치 슬라이드를 비교하면 서사 맥락이 사라진다. slide role과 index를 맞춘 paired comparison, 덱 단위 평가, 핵심 슬라이드 subset 평가를 분리하고 신뢰구간은 덱 클러스터 효과를 고려하라.

13. "한 문장 브리프"에서 실제 발표 덱으로 가는 source ingest와 narrative planning 단계가 없다. outline.md는 계약에 있지만 브리프를 어떤 근거 자료로 확장하고, 어떤 사실을 인용하며, 어떤 순서로 스토리를 짜는지가 스킬로 분리되어 있지 않다. deck-research 또는 deck-storyline 단계를 추가해 source pack, claims table, outline.md를 만든 뒤 copy/chart가 소비하게 하라.

14. 접근성 계약이 altText를 매니페스트에만 두고 slide DOM 필수 규칙으로 강제하지 않는다. img alt, SVG title/desc, decorative 표시, 표(table) semantic, 읽기 순서까지 slide-html 계약과 grader 규칙에 넣어라.

15. 1.2의 폰트 override와 5.3 hard fail 문구가 충돌한다. 1.2는 본문 하한을 grader.yaml에서 18pt까지 낮출 수 있다고 하는데, 5.3은 본문 24pt 미만을 hard fail로 고정한다. hard fail은 "configured body floor 미만"으로 바꾸고, 24pt는 기본값으로만 남겨라.

# minor

1. TossFace 상태가 PLAN과 research/toss-design.md에서 다르다. 리서치는 원본 그대로 재배포가 무료로 허용된다고 정리한다. Phase 0 항목은 "허용 여부 확인"이 아니라 "LICENSE 고지 포함, 수정 금지, 원본 번들만 허용"으로 갱신하라.

2. 5.3 hard fail 설명에서 "consulting-quality 규칙 33"을 참조하지만 research/consulting-quality.md의 후보 규칙은 31개이고 오버플로/자동 축소는 28번이다. 규칙 번호 매핑표 작성 전에 참조 번호를 정리하라.

3. chart-request, 이미지 브리프, scenes.md는 리포 로컬 정본이라고만 되어 있어 deck-factory가 입력을 자동 생성할 때 필요한 최소 공통 필드가 없다. 사용자 대면 입력도 최소 공통 envelope(requestId, brief, lang, audience, privacyMode, outputDir)을 두는 편이 안전하다.

4. gpt-image-2를 모델명으로 고정하지 말고 imageProvider/model 필드로 추상화하라. 모델명과 약관은 바뀔 수 있으므로 계약은 capability 중심이어야 한다.

5. copy.json의 sourceLine 단일 문자열은 여러 주장과 여러 출처를 담기 어렵다. claims[].{text, sourceRef, confidence}와 sources[]를 분리하면 P8 신뢰성 규칙과 연결하기 쉽다.

6. 표(table) 밀도 규칙을 채점 후보로 쓰면서 slide HTML 계약에는 table 요소나 table slot kind가 없다. 표를 금지할 것인지, semantic table을 허용할 것인지 결정하라.

7. "각 스킬 단독 상업 완성도"는 좋은 목표지만 모든 리포의 초도 게이트로 두면 출시가 늦어진다. core pipeline 통과와 standalone polish를 별도 milestone으로 나눠라.

8. slides-grab design-gate 지문 패턴을 이식한다고 되어 있지만 deck-grader와 design-gate의 책임 경계가 흐리다. design-gate는 artifact freshness, grader는 quality verdict로 분리해 이름과 출력 파일을 다르게 둬라.

9. worker 명칭(codex/opus/sonnet/fable)과 동시성 15는 구현 인프라가 전제되어 있다. 실제 GitHub Actions, 로컬 CLI, subagent runner 중 무엇을 쓰는지 실행 명령 단위로 낮춰라.

10. "상업성 있는 수준"의 실패 UX 기준은 README와 오류 안내 정도로는 약하다. 최소 예제 갤러리, 샘플 입력, before/after, known limitations를 각 리포 릴리스 조건에 넣어라.

verdict: revise
