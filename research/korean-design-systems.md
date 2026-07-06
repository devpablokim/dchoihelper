# 한국 기업 공개 디자인시스템 서베이

작성일: 2026-07-02 (리서치 워커)

## 개요

카카오, 네이버, LINE, 우아한형제들(배민), 채널톡, 당근, 클래스101, 뱅크샐러드 8개 사를 중심으로 "외부에서 실제로 접근·재사용 가능한 디자인 자산이 무엇인가"를 기준으로 조사했다. 추가로 토스, 원티드(Wanted) 등 조사 과정에서 발견된 완전 오픈소스 디자인시스템, 대한민국 정부 디자인시스템(KRDS), awesome-design-systems 계열 GitHub 큐레이션 리포, 무료 상업용 한글 폰트를 함께 정리했다.

결론부터 말하면, 한국 기업들의 "디자인시스템"은 대부분 사내 전용이며 외부에는 블로그 회고나 컨퍼런스 발표(우아콘, D2, toss.tech 등) 형태로만 공개된다. 실제로 코드/토큰/Figma 라이브러리까지 퍼블릭으로 공개해 제3자가 가져다 쓸 수 있는 곳은 당근(SEED), 채널톡(Bezier), 토스(부분: 폰트·이모지·브랜드 리소스), 원티드(Montage)뿐이다. 카카오·네이버·배민은 회사 로고/서체(BI·CI, 무료 폰트)는 공개하지만 컴포넌트·토큰 체계는 비공개다. LINE은 디자인시스템 "가이드라인 문서"를 퍼블릭 웹사이트로 공개하지만 다운로드 가능한 코드나 Figma 자산은 없다. 클래스101과 뱅크샐러드는 사실상 비공개(블로그 회고만 존재)에 가깝다.

## 핵심 발견

### 1. 카카오 (Kakao)
- 통합된 "카카오 디자인시스템" 사이트는 존재하지 않는다. 카카오스타일(지그재그) 기술블로그에 "프론트엔드팀의 디자인 시스템 재구축기"(2024) 같은 회고 글은 있으나 결과물 자체는 비공개.
- 카카오디벨로퍼스에 "카카오싱크 디자인 가이드"(로그인 버튼 규격, PNG/PSD 리소스 다운로드)가 있음 — 로그인 버튼 등 특정 위젯에 한정된 좁은 범위.
- 서체는 오픈소스로 공개: kakao/kakao-font (GitHub, OFL-1.1) — Kakao Big Sans, Kakao Small Sans 두 종. Adobe Fonts에도 오픈소스 라이선스로 배포.
- 카카오 CI/BI(로고)는 kakaocorp.com 뉴스룸 페이지에서 이미지 다운로드 가능. 계열사인 카카오뱅크는 별도로 "브랜드 리소스" 페이지(로고 SVG, 앱 아이콘, 컬러 값 #FFE300 Yellow 등, 미디어 패키지 이미지)를 운영 — 사용 가이드라인은 있으나 명시적 오픈 라이선스 표기는 없고 "브랜드 표기용" 성격이 강함(자유 재배포 라이선스 아님).
- 결론: 폰트만 진짜 오픈소스. 컴포넌트/토큰/전체 가이드라인 비공개.

### 2. 네이버 (Naver)
- 네이버파이낸셜의 "deFign"이라는 사내 디자인시스템이 블로그(m.blog.naver.com/naverfinancial)와 NAVER D2 컨퍼런스 발표로만 소개됨. 공개 저장소나 웹사이트 없음.
- 네이버가 공개하는 것은 폰트뿐: 나눔고딕/나눔명조 등 "나눔글꼴"과 마루 부리(세리프), 클로바 나눔손글씨가 오픈 라이선스(OFL 계열)로 배포. 네이버 "한글한글 아름답게" 사이트(m-hangeul.naver.com)에서 다운로드.
- 네이버 브랜드 자료는 navercorp.com/company/gallery 갤러리에서 로고 아이덴티티, 그린팩토리/1784 사옥 이미지 다운로드 가능(보도자료용, 재사용 라이선스 불명확).
- 결론: 컴포넌트/토큰 완전 비공개. 폰트만 공개.

### 3. LINE Design System (LDS)
- designsystem.line.me 에서 완전한 퍼블릭 웹 가이드라인 운영 중. LDSM(메신저용)과 LDSG(글로벌 패밀리 서비스용) 두 축으로 구성.
- 콘텐츠: Foundation(색상/타이포/아이콘 등), UX Guidelines, Case Studies, Design Principle, LINE Voice(보이스&톤), FAQ까지 문서 체계가 상당히 상세함.
- 그러나 이는 "문서 사이트"이며 다운로드 가능한 코드 저장소, Figma 커뮤니티 파일, 디자인 토큰 JSON 등은 공개되어 있지 않다(퍼블릭 GitHub 조직에도 디자인시스템 패키지 없음). FAQ에 "LINE 공통 컴포넌트와 컬러 시스템은 반드시 사용해야 한다"는 문구가 있어 애초에 LINE 내부 서비스팀을 위한 규정 문서이지, 외부 재사용을 겨냥한 오픈소스가 아니다.
- 결론: 프레젠테이션 참고자료(스크린샷, 원칙 문서, 보이스&톤 언어)로는 훌륭하지만 다운로드 가능한 자산은 없음. 저작권 명시 없이 전체가 LINE 소유.

### 4. 우아한형제들 / 배달의민족 (Woowa Brothers / Baemin)
- "우아한공방"이라는 사내 디자인시스템이 우아콘(WOOWACON) 발표로 소개되나(2023) 외부 공개 사이트/코드는 없음.
- 배민 폰트 11종(한나체, 주아체, 도현체, 연성체, 기랑해랑체, 한나체 Air/Pro, 을지로체, 을지로10년후체, 을지로 오래오래체, 글림체, 꾸불림체)은 woowahan.com/fonts 에서 무료 배포. 라이선스는 OFL 기반 — 개인/기업 모두 무료, 수정/재배포 가능, "폰트 자체의 유료 판매"만 금지. 상업적 프레젠테이션/브랜딩에 바로 사용 가능.
- 결론: 컴포넌트/토큰 비공개. 서체(11종, 눈누 등록)만 상업용 무료로 재사용 가능 — 프레젠테이션에서 친근하고 캐주얼한 톤이 필요할 때 유용.

### 5. 채널톡 (Channel.io)
- 채널톡은 "Bezier"라는 디자인시스템을 각 플랫폼별로 오픈소스 공개 중.
  - bezier-react (github.com/channel-io/bezier-react): React 컴포넌트 라이브러리, Apache-2.0 라이선스, star 275.
  - bezier-compose (github.com/channel-io/bezier-compose): Jetpack Compose 구현체, MIT 라이선스.
  - BezierSwift (github.com/channel-io/BezierSwift): iOS/Swift 구현체, MIT 라이선스.
- 실제 npm 패키지로 배포되어 프로덕션에서 바로 import 가능한 수준. 세 플랫폼(Web/Android/iOS) 모두 오픈소스인 점이 국내 기업 중 이례적으로 완성도가 높음.
- 결론: 한국 기업 중 가장 실질적으로 "가져다 쓸 수 있는" 디자인시스템 코드베이스. 다만 컴포넌트 라이브러리이며 프레젠테이션/슬라이드용 자산(색상 팔레트, 아이콘 세트 등)은 코드에서 추출해야 함.

### 6. 당근 (Karrot / 당근마켓)
- SEED Design System — seed-design.io 에서 퍼블릭 문서 사이트 운영. Foundation(Color System, Typography, Iconography), Components, Progress Board(플랫폼별 구현 상태 트래커)까지 문서화 수준이 매우 높음.
- 플랫폼: Figma(전체 토큰/아이콘/컴포넌트/화면 템플릿 + 코드 변환 플러그인), Web(GitHub 공개 저장소), Android, iOS.
- github.com/daangn/seed-design: Apache License 2.0 (Copyright 2021 Danggeun Market Inc.), star 891, fork 58, 153개 브랜치·901개 태그로 매우 활발하게 유지보수 중(최근 커밋 수 시간 전).
- 색상 시스템은 "역할 기반 색상(Role Based Color)"과 "팔레트 색상"으로 구성되어 라이트/다크 테마 적응, 접근성 대비를 표준으로 설계 — 프레젠테이션 팔레트 설계 시 참고할 만한 체계.
- 로고/브랜드 가이드는 seed-design.io/docs/foundation/logo 에 별도로 정리되어 있음(리브랜딩 이후 버전).
- 결론: 국내 기업 중 가장 완성도 높고 활발한 퍼블릭 디자인시스템. Figma 라이브러리까지 개방되어 있어 슬라이드/목업 제작에 직접 활용 가능.

### 7. 클래스101 (CLASS101)
- Vibrant Design System — vibrant-design.com (Docusaurus 기반 사이트). Core Value(Performant/Productive/Consistent) 소개 정도의 랜딩 페이지만 확인되며, 실제 컴포넌트 문서나 코드/Figma 링크는 퍼블릭 페이지에서 노출되지 않음(사내 도구로 소개됨). 별도로 "One Product System(OPS)"라는 프로덕트 시스템도 미디엄 글에 언급되나 이 역시 사내용.
- 결론: 사실상 비공개. 브랜드/마케팅 목적의 소개 페이지 수준.

### 8. 뱅크샐러드 (Banksalad)
- BPL(Banksalad Product Language)를 기술블로그(blog.banksalad.com)에서 회고 형태로만 소개. "BPL 템플릿"이라는 화면 라이브러리 개념이 언급되나 외부 공개 사이트/저장소 없음.
- 결론: 완전 비공개. 블로그 아티클을 2차 자료로만 활용 가능.

### 9. 보너스 — 토스 (Toss / Viva Republica)
- TDS(Toss Design System)는 비공개(사내 전용, toss.tech 아티클로만 소개).
- 단, 아래 두 자산은 실사용 가능한 형태로 공개되어 있어 프레젠테이션 제작에 유용:
  - Tossface (github.com/toss/tossface): 토스가 자체 제작한 이모지 폰트(3,600개 이모지), 오픈소스 공개(저장소 자체 라이선스 파일 LICENSE-TOSSFACE 존재, 상업적 사용 가능하나 저작권 표시 조건 확인 필요). ttf/woff/woff2/svg 형태로 배포, Figma 플러그인도 존재.
  - brand.toss.im: 로고(시그니처/심볼/모노), 브랜드 컬러(Toss Blue #0064FF, Toss Gray #202632), 계열사 로고, 앱 아이콘, 미디어 키트까지 zip으로 다운로드 가능. 단, 이는 "보도자료·미디어용 브랜드 자산"이며 로고 사용 규정(변형 금지 등)이 명시되어 있어 임의 재가공은 불가.

### 10. 보너스 — 원티드 (Wanted) — Montage
- montage.wanted.co.kr: "완전한 오픈소스"를 표방하는 원티드의 정식 디자인시스템. Wanted Figma UI Kit(피그마 커뮤니티 공개 파일)과 GitHub Repository(github.com/wanteddev, "Wanted Web Design System - Montage" 리포, TypeScript)를 함께 제공.
- Design Principles(Extensibility/Consistency/Efficiency), 컴포넌트 문서, 디자이너용 가이드까지 체계적으로 구성. 2024년 첫 공개된 "원티드 디자인 라이브러리"의 확장판.
- 결론: 당근 SEED, 채널톡 Bezier와 함께 국내 3대 완전 공개형 디자인시스템으로 꼽을 만함.

### 11. 보너스 — 대한민국 정부 디자인시스템 (KRDS)
- krds.go.kr — 행정안전부 주도의 "전자정부 디자인시스템". awesome-design-systems(alexpate) 리스트에도 "Korea Design System"으로 등재되어 있으며 Components/Voice&Tone/Designers Kit/Source code 4개 태그를 모두 충족하는 몇 안 되는 사례.
- 리소스 다운로드 페이지에서 React/Vue Storybook, 디자인 리소스를 무료로 제공. 소스코드는 github.com/KRDS-uiux/krds-uiux 에 공개.
- 정부 공공기관 대상이지만 색상 대비(WCAG) 기준, 한글 타이포그래피 스펙 등이 매우 상세해 한국어 프레젠테이션/공공성 있는 UI 참고 자료로 유용.

### 12. awesome-design / awesome-design-systems 계열 큐레이션 리포
- github.com/alexpate/awesome-design-systems (star 25.3k, Unlicense) — 가장 널리 쓰이는 큐레이션. Components/Voice&Tone/Designers Kit/Source code 4개 태그로 각 디자인시스템을 분류한 표 형태. 카카오/네이버/배민/당근 등 한국 기업은 등재되어 있지 않음(단 KRDS는 등재됨) — 국내 디자인시스템의 국제적 인지도가 낮다는 방증.
- github.com/klaufel/awesome-design-systems — 개발자 관점 큐레이션(내용 미상세 확인, 유사 구조로 추정).
- designsystemsrepo.com/design-systems — Jad Limcaco가 운영하는 갤러리형 큐레이션(카드형 UI, 스크린샷 프리뷰 포함). Wanda, Ant Design, Atlassian, Carbon, Polaris, Primer, Spectrum 등 100여 개 등재. 한국 기업 없음. 프레젠테이션에서 "해외 유수 디자인시스템 벤치마킹" 슬라이드를 만들 때 스크린샷 소스로 쓰기 좋음(단 각 이미지 저작권은 각사 소유이므로 출처 표기 필요).
- github.com/VoltAgent/awesome-design-md — "DESIGN.md" 형태로 유명 브랜드 디자인시스템을 분석해 정리한 마크다운 모음(AI 코딩 에이전트가 읽고 UI를 생성하도록 설계). 프레젠테이션 제작 자동화 파이프라인에 참고할 만한 포맷.
- github.com/Cloud-Premises/figma-design-system-resources — Figma 커뮤니티에 공개된 디자인시스템 파일들을 큐레이션.
- github.com/bradtraversy/design-resources-for-developers — 스톡 사진, 웹 템플릿, CSS 프레임워크, UI 라이브러리 등 개발자용 디자인 리소스 총망라 리스트. 슬라이드 제작에 필요한 무료 이미지/아이콘/일러스트 소스를 찾을 때 유용.

## 재사용 가능 자산 (라이선스 명시)

- SEED Design System (당근) — 코드: Apache License 2.0 (github.com/daangn/seed-design). Figma 라이브러리는 seed-design.io에서 링크 제공(퍼블릭 열람 가능, 별도 이용약관 확인 필요). 색상 토큰/타이포/아이콘/컴포넌트 스펙 문서 전체가 seed-design.io에 공개.
- Bezier Design System (채널톡) — bezier-react: Apache-2.0. bezier-compose: MIT. BezierSwift: MIT. 모두 npm/CocoaPods/Gradle로 바로 설치 가능.
- Montage (원티드) — GitHub Repository(TypeScript) + Figma Community 파일. "완전한 오픈소스"를 표방(구체적 라이선스 파일은 리포 내 확인 필요, 조사 시점에 라이선스 텍스트까지는 확인하지 못함 — 사용 전 재확인 권고).
- Kakao Big Sans / Kakao Small Sans (카카오 폰트) — OFL-1.1, github.com/kakao/kakao-font. 상업적 사용/수정/재배포 가능(폰트 단독 판매만 금지). 눈누(noonnu.cc)에도 등록.
- Pretendard — SIL Open Font License 1.1, github.com/orioncactus/pretendard. 상업적 사용/수정/재배포 전면 허용(폰트 단독 판매만 금지). 한국 스타트업/서비스에서 사실상 표준 UI 서체로 채택됨. Thin(100)~Black(900) 풀 웨이트, 웹폰트 CDN도 제공.
- 배민 폰트 11종 (한나체·주아체·도현체·연성체·기랑해랑체·한나체Air·한나체Pro·을지로체·을지로10년후체·을지로오래오래체·글림체·꾸불림체) — OFL 계열, woowahan.com/fonts/license. 개인/기업 무료, 수정/재배포 가능, 폰트 단독 판매만 금지.
- 네이버 나눔글꼴(나눔고딕/나눔명조 등), 마루 부리, 클로바 나눔손글씨 — 오픈 라이선스(OFL 계열), m-hangeul.naver.com/font. 상업적 사용 가능, 폰트 자체 유료 판매만 금지.
- Tossface (토스 이모지 폰트) — github.com/toss/tossface, 자체 라이선스 파일(LICENSE-TOSSFACE) 명시, 오픈소스로 무료 다운로드·상업적 사용 가능(정확한 조건은 파일 원문 재확인 권장). ttf/woff/woff2/svg + Figma 플러그인 제공.
- Toss 브랜드 리소스(로고, 브랜드 컬러 #0064FF, 계열사 로고, 미디어 키트) — brand.toss.im에서 zip 다운로드 가능하나 "로고 변형 금지" 등 사용 규정이 걸려 있어 자유 재배포 라이선스는 아님. 프레젠테이션에 "토스 사례"를 인용할 때 로고 원본 이미지 소스로만 활용.
- 카카오뱅크 브랜드 리소스(심볼/워드마크/시그니처 SVG, 컬러 값 #FFE300 등) — kakaobank.com/view/about/brand/resource. 사용 가이드라인 명시(변형 금지), 오픈 라이선스 아님. 인용 목적으로만 사용.
- KRDS(전자정부 디자인시스템) — krds.go.kr, github.com/KRDS-uiux/krds-uiux. 정부 디자인시스템으로 공공누리 유사 조건일 가능성이 높음(정확한 라이선스 표기는 사이트에서 재확인 필요). React/Vue Storybook, 리소스 무료 다운로드.
- LINE Design System 문서(designsystem.line.me) — 다운로드 가능한 자산 없음, 저작권 LINE 보유. 스크린샷 인용 시 출처 표기 권고, 재배포/재가공 불가로 간주.

## 통합 권고

1. 프레젠테이션/슬라이드 덱 제작 파이프라인에는 한글 서체로 Pretendard를 기본값으로 채택하는 것이 가장 안전하고 범용적이다. 상업적 사용에 제약이 없고, 웹폰트 CDN이 있어 즉시 임베드 가능하며, 이미 국내 스타트업 UI의 사실상 표준이라 "익숙한 느낌"을 준다.
2. 딥/캐주얼 톤이 필요한 슬라이드(예: F&B, 로컬 커머스, 캐주얼 브랜드)에는 배민 폰트(한나체·주아체 등)를, 손글씨/친근한 무드에는 네이버 클로바 나눔손글씨를 보조 서체로 매핑해두면 좋다.
3. 컴포넌트/토큰 체계를 실제로 참고해 우리 덱 팩토리의 디자인시스템(색상 역할 체계, 라이트/다크 테마 토큰 네이밍)을 설계할 때는 당근 SEED의 "역할 기반 색상 + 팔레트 색상" 2단 구조를 1차 레퍼런스로 삼을 것을 권고한다. 문서화 품질이 국내 최고 수준이며 실제 프로덕션에서 라이트/다크 모드를 검증한 체계다.
4. React 기반으로 실제 UI 컴포넌트가 필요한 경우 bezier-react(Apache-2.0)를 그대로 의존성으로 추가하거나, 소스를 참고해 자체 컴포넌트를 구현하는 것이 코드 재사용 관점에서 가장 실용적이다.
5. 카카오뱅크/토스 등 브랜드 리소스는 "그 회사 사례를 인용하는 슬라이드"(예: 국내 핀테크 UI 비교 슬라이드)에서 로고·컬러 값을 정확히 재현하는 용도로만 쓰고, 우리 자체 브랜드 자산으로 변형·재사용하지 않는다(로고 변형 금지 조항이 있음).
6. LINE Design System, 카카오/네이버/배민/뱅크샐러드/클래스101의 사내 디자인시스템은 "디자인 원칙 서술"이나 "국내 디자인시스템 사례 소개" 슬라이드의 텍스트/스크린샷 인용 소스로만 쓰고, 코드나 자산을 그대로 가져오지 않는다.
7. awesome-design-systems(alexpate) 표는 "해외 유수 디자인시스템과 비교했을 때 한국 기업의 오픈소스 공개 수준"을 보여주는 슬라이드 소재로 그대로 활용 가능하다(카카오·네이버·배민이 등재되어 있지 않다는 사실 자체가 흥미로운 데이터 포인트).

## 리스크

- 접근 실패: designsystem.line.me의 하위 페이지(LDSM/LDSG foundation, case studies 등)는 목록만 확인했고 상세 내용까지는 들어가지 않았다. 실제로 다운로드 가능한 자산이 있는지(예: 아이콘 세트 zip)는 완전히 확인하지 못했으므로 재확인이 필요하다.
- klaufel/awesome-design-systems는 검색 결과의 설명만 확인했고 리포 내용을 직접 열람하지 못했다(alexpate 리포와 중복 가능성 있음).
- 클래스101 Vibrant Design System은 vibrant-design.com 루트 페이지만 확인했고 /docs 하위 경로에 실제 컴포넌트 문서가 있는지는 크롤링 시간 관계상 추가 확인하지 못했다. 완전히 비공개로 단정하기보다 "루트 랜딩만 공개, 상세 문서는 미확인"으로 기재하는 것이 정확하다.
- Montage(원티드)의 정확한 오픈소스 라이선스 파일(MIT/Apache 등 구체 조건)은 리포 페이지 상세 열람에 실패해(대용량 응답으로 텍스트 파일 저장 후 grep 처리) 명확히 확인하지 못했다. 실사용 전 github.com/wanteddev 리포에서 LICENSE 파일을 직접 재확인해야 한다.
- Tossface의 LICENSE-TOSSFACE 원문 전체는 확인하지 못했다(제목과 존재만 확인). 상업적 재배포 조건(글리프 변형 허용 여부 등)은 사용 전 원문 확인이 필요하다.
- KRDS(krds.go.kr)의 정확한 라이선스 문구(공공누리 유형 등)는 직접 방문해 확인하지 못했다. "무료로 다운받으실 수 있습니다"라는 소개 문구만 확인했으며, 재배포·상업적 활용 범위는 사이트 내 별도 확인이 필요하다.
- 카카오/네이버/카카오뱅크/토스의 브랜드 리소스(로고·CI)는 모두 "브랜드 표기용"이며 명시적 오픈 라이선스가 아니다. 프레젠테이션에 로고를 삽입할 때는 반드시 각사가 명시한 사용 규정(변형 금지, 배경색 규정 등)을 지켜야 하며, 자유 이용 가능한 자산으로 오인해서는 안 된다.
- 날조 방지 차원에서, 이 문서에 기재된 별(star)/포크 수, 커밋 시각 등 GitHub 메타데이터는 조사 시점(2026-07-02) 스냅샷이며 이후 변동될 수 있다.

## 출처

1. https://kakao.github.io/
2. https://developers.kakao.com/docs/ko/kakaosync/design-guide
3. https://devblog.kakaostyle.com/ko/2024-12-13-1-rebuilding-frontend-design-system/
4. https://www.kakaocorp.com/page/detail/542
5. https://github.com/kakao/kakao-font
6. https://www.kakaocorp.com/page/detail/11340
7. https://www.kakaobank.com/view/about/brand/resource
8. https://fonts.adobe.com/fonts/kakao-big-sans
9. https://noonnu.cc/font_page/1571
10. https://m.blog.naver.com/naverfinancial/223222195784
11. https://d2.naver.com/helloworld/3442203
12. https://m-hangeul.naver.com/font
13. https://help.naver.com/support/contents/contents.help?serviceNo=1074&categoryNo=3497
14. https://m-hangeul.naver.com/font/maru
15. https://navercorp.com/company/gallery
16. https://designsystem.line.me/
17. https://designsystem.line.me/LDSM
18. https://designsystem.line.me/LDSG
19. https://www.woowahan.com/en
20. https://www.woowahan.com/en/fonts
21. https://www.woowahan.com/fonts/license
22. https://noonnu.cc/font_page/53
23. https://design-system-group.gitbook.io/reference/undefined/bamin
24. https://techblog.woowahan.com/
25. https://github.com/channel-io
26. https://github.com/channel-io/bezier-react
27. https://github.com/channel-io/bezier-compose
28. https://github.com/channel-io/BezierSwift
29. https://velog.io/@wns450/bezier-react-%EB%94%94%EC%9E%90%EC%9D%B8-%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%B1%84%EB%84%90%ED%86%A1-%EC%98%A4%ED%94%88%EC%86%8C%EC%8A%A4-%EC%82%B4%ED%8E%B4%EB%B3%B4%EA%B8%B0
30. https://seed-design.io/
31. https://seed-design.io/docs/foundation/color/color-system
32. https://seed-design.io/docs/foundation/logo
33. https://github.com/daangn/seed-design
34. https://raw.githubusercontent.com/daangn/seed-design/main/LICENSE
35. https://medium.com/daangn/%EB%94%94%EC%9E%90%EC%9D%B8%EC%8B%9C%EC%8A%A4%ED%85%9C-%ED%8C%80%EC%9D%80-%EB%94%94%EC%9E%90%EC%9D%B8%EC%8B%9C%EC%8A%A4%ED%85%9C%EB%A7%8C-%EC%9E%98-%EB%A7%8C%EB%93%A4%EB%A9%B4-%EB%90%A0%EA%B9%8C-4f6f2478a8db
36. https://vibrant-design.com/
37. https://medium.com/class101/vibrant-design-system%EC%9D%84-%EC%86%8C%EA%B0%9C%ED%95%A9%EB%8B%88%EB%8B%A4-e66ba0ae1dc3
38. https://blog.banksalad.com/tech/banksalad-product-language-design/
39. https://blog.banksalad.com/tags/design-system/
40. https://brand.toss.im/
41. https://toss.tech/article/toss-design-system
42. https://github.com/toss/tossface
43. https://github.com/RealityRipple/emoji/blob/master/LICENSE-TOSSFACE
44. https://toss.tech/article/22205
45. https://www.figma.com/community/file/1355516515676178246/wanted-design-system
46. https://github.com/wanteddev
47. https://montage.wanted.co.kr/docs/getting-started
48. https://designcompass.org/2025/04/11/wanted-design-system-open-source/
49. https://www.krds.go.kr/
50. https://www.krds.go.kr/html/site/outline/outline_05.html
51. https://github.com/KRDS-uiux/krds-uiux
52. https://github.com/alexpate/awesome-design-systems
53. https://github.com/klaufel/awesome-design-systems
54. https://designsystemsrepo.com/design-systems/
55. https://github.com/VoltAgent/awesome-design-md
56. https://github.com/Cloud-Premises/figma-design-system-resources
57. https://github.com/bradtraversy/design-resources-for-developers
58. https://noonnu.cc/font_page/694
59. https://github.com/orioncactus/pretendard
