# 토스(Toss) 공식 디자인 자산 전수 조사

## 개요

토스(비바리퍼블리카)가 공식적으로 외부에 공개한 디자인 관련 자산을 TDS(Toss Design System), 전용 서체(Toss Product Sans, 토스페이스), toss.tech 디자인 아티클, 오픈소스 프론트엔드 라이브러리, Simplicity 디자인 컨퍼런스 다섯 갈래로 나누어 조사했다. 결론부터 말하면, 토스는 "쓰는 이야기"(디자인 시스템 운영 철학, 서체 제작기, 컨퍼런스 세션 영상)는 폭넓게 공개하지만, "가져다 쓸 수 있는 자산" 자체는 거의 전부 비공개이거나 강한 사용 제한이 걸려 있다. 예외적으로 완전 개방된 것은 이모지 폰트 토스페이스(TossFace)와 프론트엔드 유틸리티 라이브러리(es-toolkit, overlay-kit 등, 전부 MIT)뿐이다. TDS 컴포넌트 라이브러리(Figma UI Kit, npm 패키지)와 Toss Product Sans 서체는 "앱인토스(Apps in Toss)" 미니앱 개발이라는 제한된 목적에만 쓸 수 있고, 그 범위를 벗어난 상업적 재사용은 라이선스로 명시적으로 금지되어 있다.

## 핵심 발견

### 1. TDS(Toss Design System) — 공개 범위는 "앱인토스 생태계 한정", 일반 공개 아님

- TDS는 토스 사내 디자인 플랫폼 팀이 운영하는 내부 디자인 시스템이며, 별도의 공개 웹사이트(예: 공개 Storybook, 공개 문서 사이트)나 일반인이 자유롭게 접근 가능한 GitHub 오픈소스 저장소가 없다. `npm i @toss/tds-react-native` 패키지는 npm에 공개(public)되어 있으나 README가 없고, 소스 코드 저장소(GitHub)도 공개되어 있지 않다. 즉 컴파일된 패키지만 배포될 뿐, TDS 자체는 오픈소스가 아니다.[6]
- 유일하게 외부에 개방된 통로는 "앱인토스(Apps in Toss)" 미니앱 개발자센터(developers-apps-in-toss.toss.im)를 통한 것이다. 이곳에서 TDS Mobile Figma UI Kit(`.fig` 파일)을 다운로드할 수 있고, `@toss/tds-react-native` SDK를 미니앱 개발에 쓸 수 있다.[9][10]
- 단, Figma UI Kit에는 별도의 "TDS Mobile UI Kit 라이선스"가 명시되어 있으며(한국어판 우선), 허용 범위는 오직 "앱인토스용 애플리케이션의 개발/디자인/프로토타입 제작"으로 한정된다. 금지 행위로 (1) 다른 프로젝트·제품·서비스에 사용, (2) 상업적 판매·제3자 제공, (3) 복사·수정·편집·재가공, (4) 재배포를 명시적으로 나열한다. 즉 앱인토스 생태계 바깥에서 일반 웹/앱 프로젝트에 TDS 컴포넌트를 가져다 쓰는 것은 라이선스 위반이다.[11]
- toss.tech 아티클(`toss-design-system`, `toss-design-system-guide`, `rethinking-design-system`, `tds-component-making`)을 통해 TDS의 설계 철학과 API 패턴(Flat vs Compound 하이브리드, 컴포넌트 확장성 설계, 접근성/다크모드 대응 등)은 상세히 공개되어 있다. 이는 "읽고 배우는 자료"로서 재사용 가치가 있으나, 코드나 컴포넌트 자체를 가져다 쓸 수 있는 자산은 아니다.[3][4][5]

### 2. Toss Product Sans — 비공개 전용 서체, 다운로드 경로 없음

- Toss Product Sans는 2020년 산돌(Sandoll)과 협업해 제작한 토스 전용 서체이며, 2번째 버전부터는 이도타입(Leedotype)과 공동 개발 중이다.[7]
- 산돌 포트폴리오 페이지에서 "브랜드 전용 폰트(Custom Font)" 카테고리로 분류되어 있다. 이는 산돌이 일반 판매하는 "오리지널 폰트"(라이선스 구매 가능)와 구분되는 카테고리로, 토스만을 위해 독점 제작된 서체라는 의미다. 즉 제3자가 산돌을 통해 라이선스를 구매해 쓸 수 있는 상품이 아니다.[2]
- 폰트 식별 커뮤니티 눈누(noonnu.cc)에도 등록되어 있지 않으며, "폰트 사용에 대한 라이센스 문의는 저작권자에게 문의해주세요"라는 안내만 있다.[1]
- 토스피드 아티클 댓글에 실제로 "토스 폰트는 비공개인가요?"라는 사용자 질문이 달려 있으나 토스 측 공식 답변(공개 여부 확답)은 확인하지 못했다. 정황상 비공개로 판단된다.[7]
- 결정적 증거: 앱인토스 개발자센터의 TDS Figma UI Kit 안내문에는 "Toss Product Sans는 별도 자산으로 배포가 어려워, Figma에서는 SF Pro를 사용해요"라고 명시되어 있다. 즉 토스가 공식적으로 배포하는 디자인 자산(Figma Kit)에서조차 이 서체 파일 자체는 포함하지 않는다 — 실제 앱에서는 자동 적용되지만 폰트 파일을 외부에 내주지는 않는다는 뜻이다.[10]
- 결론: Toss Product Sans는 다운로드 경로도, 상업적 이용 가능한 공개 라이선스도 존재하지 않는다. 상업적 이용 불가.

### 3. TossFace(토스페이스) — 완전 무료, 단 수정 재배포 금지 (OFL 아님, 커스텀 라이선스)

- GitHub `toss/tossface` 저장소(스타 358개, 최신 v1.6.1)에서 ttf/otf/woff/woff2 전체 폰트 파일과 CDN 웹폰트(jsDelivr)를 무료로 제공한다.[13]
- 라이선스 원문(저장소 LICENSE 파일과 `toss.im/tossface/copyright` 페이지 두 곳에서 동일 확인)은 커스텀 "토스페이스 라이선스"이며, OFL(Open Font License)이 아니다. 온라인 커뮤니티(news.hada.io)에 "OFL이다"라는 언급이 있었으나 실제 라이선스 원문 대조 결과 사실이 아니다 — 별도의 자체 작성 라이선스다.[12][14]
- 허용: 사용, 연구, 재배포(원본 그대로, 저작권 안내 포함 시) 무료.
- 금지: (1) 2차적저작물(수정본) 제작, (2) 폰트 자체의 유료 판매, (3) 상표권·디자인권 등 지식재산권 등록, (4) 전시회·공모전 출품, (5) 소스코드로 변환해 복제·전송·게재하는 행위.
- 즉 "있는 그대로" 상업적 프로젝트(앱, 웹, 인쇄물, 마케팅 자료 등)에 넣어 쓰는 것은 자유롭지만, 글자 모양을 변형하거나 파생 폰트를 만드는 것은 금지된다. 실무적으로는 "무료 상업적 이용 가능, 수정 금지형 라이선스"로 이해하면 된다.[14]
- Figma 커뮤니티 플러그인("Tossface")도 존재해 Figma 안에서 바로 이모지를 넣어볼 수 있다(저작권은 토스 소유 명시).[8]

### 4. toss.tech 디자인 아티클 — 원칙/철학 공개, 재사용 가능한 "읽을거리" 자산

toss.tech `/category/design` 카테고리에 디자인 챕터가 정기 발행하는 아티클이 누적되어 있다. 디자인시스템 원칙과 직결되는 주요 아티클:

- "토스 디자이너가 제품에만 집중할 수 있는 방법" — TDS 컴포넌트 설계 3원칙(케이스 패턴화, 심미적 경험 설계, 전체 사용자 접근성 보장) 사례.[3]
- "디자인 시스템 다시 생각해보기" — "디자인 시스템도 제품이다"라는 관점 전환, Flat API와 Compound API를 함께 제공하는 하이브리드 전략, 컴포넌트 detach/fork 문제에 대한 대응 철학.[5]
- "제품이 커지면 디자인 시스템 가이드는 어떻게 개선돼야 할까?" — TDS 컴포넌트 가이드 문서화 방법론.[4]
- "이런 것도 컴포넌트로 만들어도 될까?" — 신규 컴포넌트 추가 시 가설 검증 프로세스(1편, `tds-component-making`).
- "토스 디자인 원칙 Value first, Cost later" — 가치를 먼저 보여준 뒤 비용/결정을 요구하는 제품 원칙.
- "토스의 8가지 라이팅 원칙들" — UX 라이팅 시스템.
- "토스가 디자인 직무를 2개로 줄인 이유" — 2026년 4월 디자인 챕터 조직 개편(6개 직무 → 2개 통합).

이 아티클들은 텍스트/이미지 콘텐츠 저작권이 토스에 있으며 별도 재배포·상업적 이용 라이선스가 명시되어 있지 않다(일반 블로그 저작권 원칙 적용, 인용/링크 수준의 참고는 통상 허용되나 전문 복제·재배포는 별도 허가 필요로 간주해야 함).

### 5. 오픈소스 프론트엔드 라이브러리 — 전부 MIT, 상업적 이용 완전 자유

토스 Slash 팀이 slash.page(허브 사이트)를 통해 공개하는 라이브러리 7종 전부 GitHub `toss/` 조직에 공개되어 있고, 라이선스 파일을 직접 대조한 결과 전부 MIT (Copyright Viva Republica, Inc.)로 확인했다.[15][16]

| 패키지 | 설명 | GitHub 스타 | 디자인 연관성 |
|---|---|---|---|
| es-toolkit | lodash 대체 유틸리티(2~3배 빠름, 최대 97% 작은 번들) | 10.9K | 낮음(순수 로직) |
| overlay-kit | 모달/팝업/다이얼로그 등 오버레이 선언적 관리 | 682 | 높음(UI 패턴/상호작용 설계) |
| use-funnel | 멀티스텝 화면 플로우(퍼널) 타입세이프 관리 | 553 | 높음(UX 플로우 설계) |
| es-hangul | 한글 파싱/조사 처리 유틸리티 | 1.8K | 중간(한국어 UX 텍스트 처리) |
| suspensive | React Suspense 실전 빌딩 블록 | 1.0K | 낮음 |
| es-git | Node 환경 Git 데이터 접근 유틸리티 | 314 | 낮음 |
| react-simplikit | 경량 React 유틸리티/훅 | 306 | 낮음 |

이 중 디자인/UI 작업에 실질적으로 재사용 가치가 높은 것은 overlay-kit(모달·토스트·다이얼로그 상태 관리 패턴)과 use-funnel(다단계 온보딩/결제 플로우 설계)이다. 둘 다 MIT라 상업 프로젝트에 제약 없이 통합 가능하다.

### 6. Simplicity — 토스 디자인 컨퍼런스, 세션 영상은 공개(다운로드 가능한 자료 파일은 확인 못함)

- 토스는 2021년부터 매년(21, 23, 24, 25 확인; 22는 명확한 존재 확인 못함) "Simplicity"라는 이름의 디자인 컨퍼런스를 열고, 전용 웹사이트(`toss.im/simplicity-XX`)와 유튜브 재생목록("Simplicityㅣ디자인 컨퍼런스", 28개 영상 이상)으로 세션을 공개한다.[17][18][19]
- Simplicity 24는 "Product Designer (Tools)" 직군 특별편으로 Wise Whys/Noise to Melody/Beyond Frames 3개 트랙, 11개 세션 구성이었다.[18]
- Simplicity 25는 그래픽·인터랙션·UX 라이팅·리서치·플랫폼 디자인 등 다양한 분야를 다뤘고, 세션 음성을 실제 디자이너 목소리를 학습시킨 AI 보이스로 제작하는 등 제작 방식 자체도 이슈가 됐다.[20]
- toss.tech에 "Simplicity 4" 시리즈(세션 시각 자료 제작 노하우 아티클, "아름답고 이해하기 쉬운 세션 자료 만들기")가 있어, 컨퍼런스 발표 자료(슬라이드) 디자인 원칙을 엿볼 수 있다.
- 세션 영상은 유튜브/자체 웹사이트에서 스트리밍 형태로 공개되며, 발표자료(PDF/Keck) 자체를 다운로드할 수 있는 공식 배포 페이지는 이번 조사에서 발견하지 못했다. (참고: 별개 행사인 개발자 컨퍼런스 "SLASH"의 일부 세션 페이지에는 "발표자료 다운로드 공유"라는 문구가 있었으나, 이는 Simplicity가 아닌 SLASH 21의 TDS 관련 개발 세션이었다. Simplicity와 SLASH는 서로 다른 컨퍼런스이므로 혼동 주의.)

## 재사용 가능 자산(라이선스 명시)

1. TossFace(토스페이스) 이모지 폰트 — 무료, 커스텀 라이선스(수정·재판매·IP등록·공모전출품·소스코드변환 금지, 원본 그대로 상업적 사용은 자유). GitHub: https://github.com/toss/tossface, 다운로드: https://github.com/toss/tossface/releases/latest, 저작권 안내: https://toss.im/tossface/copyright
2. es-toolkit — MIT. https://github.com/toss/es-toolkit
3. overlay-kit — MIT. https://github.com/toss/overlay-kit (모달/오버레이 UI 패턴, 디자인 작업에 실무 재사용 가치 높음)
4. use-funnel — MIT. https://github.com/toss/use-funnel (멀티스텝 UX 플로우 관리)
5. es-hangul — MIT. https://github.com/toss/es-hangul
6. suspensive — MIT. https://github.com/toss/suspensive
7. es-git — MIT. https://github.com/toss/es-git
8. react-simplikit — MIT. https://github.com/toss/react-simplikit
9. Simplicity 세션 영상(유튜브 공개, 학습·참고용) — https://www.youtube.com/playlist?list=PL1DJtS1Hv1PgAekdTPF0lKtfsqAis3HXR
10. toss.tech 디자인 아티클(원칙·철학 학습 참고용, 재배포는 별도 문의 필요) — https://toss.tech/category/design

### 재사용 불가/제한 자산 (참고용으로만 기록)

- TDS Figma UI Kit(`.fig`) — 앱인토스 개발 목적 외 사용, 수정, 상업적 판매, 재배포 전부 금지. 일반 프로젝트용 디자인 시스템으로 전용 불가.
- `@toss/tds-react-native` npm 패키지 — 소스 비공개, 앱인토스 SDK 용도로 배포되는 컴파일 패키지. 라이선스 명시 없음(README 부재).
- Toss Product Sans — 다운로드 경로 자체가 없음. 산돌의 "브랜드 전용 폰트"로 토스 독점. 상업적 이용(제3자) 불가.

## 통합 권고

- deck-factory 파이프라인에 "토스 스타일 슬라이드/UI"를 만들고 싶다면, TDS 컴포넌트나 Product Sans 폰트를 실제로 가져다 쓰는 것은 라이선스상 불가능하다. 대신 (1) toss.tech 아티클에서 확인한 디자인 원칙(Flat+Compound 하이브리드, Value first-Cost later, 접근성 5원칙, 여백/타이포 균형 원칙)을 텍스트 규칙으로 추출해 자체 디자인 토큰/스타일 가이드에 반영하는 방식이 현실적이다.
- 시각적으로 "토스st" 느낌을 재현하려면 Product Sans 대신 오픈소스 대체 서체(예: Pretendard, Spoqa Han Sans 등 상업적 이용 가능한 한글 웹폰트)로 유사한 균형감(숫자·기호를 국문보다 크게, 라운드한 속공간)을 흉내내는 접근이 안전하다.
- 이모지가 필요하면 TossFace를 원본 그대로(수정 없이) CDN 링크로 불러와 쓰는 것은 라이선스상 문제없다. 단, 자체 아이콘 세트로 가공·재배포하면 라이선스 위반이므로 금지.
- UI 상호작용 로직(모달/오버레이 관리, 멀티스텝 플로우)에는 overlay-kit, use-funnel을 코드 레벨로 그대로 도입해도 무방하다(MIT). 다만 이들은 "시각 디자인 자산"이 아니라 "동작 패턴 라이브러리"이므로 비주얼 스타일은 자체 제작해야 한다.
- Simplicity 세션 영상은 발표 슬라이드의 레이아웃/그래픽 감각을 벤치마킹하는 참고 자료로만 쓰고, 화면 캡처를 그대로 자산화(재배포)하는 것은 피해야 한다.

## 리스크

- Toss Product Sans를 "토스 폰트"라는 이름으로 웹에서 무단 배포하거나 임베딩하는 3rd-party 페이지(예: dtaxi.tistory.com, fontmeme.com 유사 사이트)가 검색에 잡히는데, 공식 라이선스 근거가 없으므로 절대 신뢰하면 안 된다. 실제 폰트 파일 출처가 불분명한 배포본을 프로젝트에 쓰면 저작권 분쟁 리스크가 있다.
- TDS Figma Kit/npm 패키지는 "공개돼 있다"는 사실만 보고 라이선스 조건(앱인토스 전용, 재배포·상업적 판매·수정 금지)을 놓치기 쉽다. 그대로 컴포넌트를 뜯어서 사내 디자인 시스템에 포팅하면 명백한 라이선스 위반이다.
- TossFace를 "OFL"로 잘못 소개하는 국내 커뮤니티 게시물이 존재한다(news.hada.io 댓글 등). 실제로는 OFL이 아니라 커스텀 라이선스이며 "수정 금지" 조항이 있으므로, OFL 기준으로 파생 폰트를 만들 수 있다고 착각하면 안 된다.
- Simplicity 세션 발표자료(슬라이드 PDF)의 공식 다운로드 페이지를 이번 조사에서 확인하지 못했다. "발표자료 다운로드 가능"이라고 오인하지 않도록 주의(그 문구는 별개 행사인 SLASH 컨퍼런스 세션 페이지에서 발견된 것).
- 산돌 페이지(sandoll.co.kr/TossProductSans)는 JS 렌더링 위주라 크롤러로 본문 상세 라이선스 조항까지는 확인하지 못했다(네비게이션만 수집됨). 완전한 확답이 필요하면 산돌에 직접 문의가 필요하다는 점을 리스크로 남긴다.

## 출처

1. https://noonnu.cc/posts/12791 (토스피드 폰트 - 무슨 폰트? 눈누)
2. https://www.sandoll.co.kr/TossProductSans (산돌 토스프로덕트산스 포트폴리오 페이지)
3. https://toss.tech/article/toss-design-system (토스 디자이너가 제품에만 집중할 수 있는 방법)
4. https://toss.tech/article/toss-design-system-guide (제품이 커지면 디자인 시스템 가이드는 어떻게 개선돼야 할까?)
5. https://toss.tech/article/rethinking-design-system (디자인 시스템 다시 생각해보기)
6. https://www.npmjs.com/package/@toss/tds-react-native (npm 패키지, README 없음)
7. https://toss.im/tossfeed/article/beginning-of-tps (서체 고민 없이 본질에만 집중할 수 있도록 — Toss Product Sans 제작기)
8. https://www.figma.com/community/plugin/1315040601403942607/tossface (Tossface Figma 플러그인)
9. https://developers-apps-in-toss.toss.im/design/prepare/design.html (앱인토스 개발자센터 — 디자인 도구/TDS Figma 라이브러리 안내)
10. https://developers-apps-in-toss.toss.im/design/prepare/design.html (동일 페이지, Product Sans 미배포 관련 유의사항)
11. https://developers-apps-in-toss.toss.im/design/prepare/figma-ui-license.html (TDS Mobile UI Kit for Apps-in-toss License 전문)
12. https://news.hada.io/topic?id=6062 (토스페이스 vs 다른 벤더 이모지 비교 — OFL 오인 언급 포함, 실제 라이선스와 대조 필요)
13. https://github.com/toss/tossface (토스페이스 GitHub 저장소)
14. https://toss.im/tossface/copyright (토스페이스 저작권 안내 및 라이선스 전문) / raw LICENSE: https://raw.githubusercontent.com/toss/tossface/main/LICENSE
15. https://slash.page/ (Slash 라이브러리 허브)
16. https://github.com/toss (toss GitHub 조직, es-toolkit/overlay-kit/use-funnel/es-hangul/suspensive/es-git/react-simplikit 각 저장소 LICENSE 파일 직접 대조)
17. https://toss.im/simplicity-24 (Simplicity24 컨퍼런스 웹사이트)
18. https://toss.im/simplicity-21 (Simplicity21 컨퍼런스 웹사이트)
19. https://www.youtube.com/playlist?list=PL1DJtS1Hv1PgAekdTPF0lKtfsqAis3HXR (Simplicityㅣ디자인 컨퍼런스 유튜브 재생목록)
20. https://www.velopers.kr/post/4515 (Simplicity 25 소개 — 3자 요약, 1차 출처 아님, 참고용)
21. https://toss.tech/category/design (Toss Tech Design 카테고리 목록)
22. https://toss.tech/series/simiplicity4 (Simplicity 세션 자료 제작기 시리즈)
