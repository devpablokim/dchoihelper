<!-- Language switcher -->
[English](README.md) | **한국어**

<div align="center">

# deck-factory

**말할 내용 한 줄 → 발표급 다크 에디토리얼 HTML 덱.**

[![Stars](https://img.shields.io/github/stars/kimsh-1/deck-factory?style=flat&color=6E7BF2&labelColor=08090A)](https://github.com/kimsh-1/deck-factory/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-6E7BF2?style=flat&labelColor=08090A)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-6E7BF2?style=flat&labelColor=08090A)](skills/deck-factory/SKILL.md)
[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude-6E7BF2?style=flat&labelColor=08090A)](https://claude.com/claude-code)

</div>

<div align="center">

![움직이는 deck-factory](docs/media/hero.gif)

**▶ 풀 영상 보기:**
[Hook · 30s](https://github.com/kimsh-1/deck-factory/releases/download/showcase-v1/01-hook-30s.mp4) ·
[제작기 · 40s](https://github.com/kimsh-1/deck-factory/releases/download/showcase-v1/02-making.mp4) ·
[사용법 · 30s](https://github.com/kimsh-1/deck-factory/releases/download/showcase-v1/03-usage-30s.mp4)

</div>

---

## 이게 뭔가

발표 전날 밤을 떠올려 보라. 텍스트 박스를 밀고, 회색 카드와 씨름하고, 뒷자리에서는 읽히지도 않을 글씨를 줄이고 있다. **deck-factory**는 그 노동을 디자인 시스템으로 대체한다. 무엇을 말하고 싶은지 한 문장만 주면, 발표의 앞면 — 거대 숫자, 4모서리 크롬, hairline 구조, 아마추어 박스 0개의 다크 에디토리얼 덱 — 을 지어낸다. Apple·Linear·Stripe 키노트가 실제로 보이는 그 방식으로.

지금 검증된 실물은 **프리미엄 슬라이드 12장 + 모션그래픽 영상 3편**, 전부 이 디자인 시스템으로 지었다. 아래의 생성 파이프라인은 이걸 끝에서 끝까지 자동화하는 로드맵이다.

## 빠른 시작

```bash
# 1. 플러그인 마켓플레이스 추가
/plugin marketplace add kimsh-1/deck-factory

# 2. 스킬 설치
/plugin install deck-factory@deck-factory

# 3. 한 문장으로 호출
/deck-factory "시리즈A IR 덱 12장, 우리 리텐션 곡선이 이기는 이유"
```

> 플러그인 마켓플레이스 설치가 의도된 경로다. 디자인 시스템과 스킬은 실물이며 바로 쓸 수 있고, 완전 자동화된 원커맨드 파이프라인은 연결 작업 중이다([작동 방식](#작동-방식) 참조).

## 특징

| | |
|---|---|
| **다크 에디토리얼 디자인 시스템** | near-black `#08090A` 캔버스, 라벤더블루 `#6E7BF2` + 시안 `#43C7F4` 액센트, Pretendard, 거대 숫자. |
| **`no_box` · 거대 숫자 · 4모서리 크롬** | 회색 채움 카드 없음 — 구조는 hairline과 surface 래더에서 나온다. 120px+ 스탯 숫자에 value > label > context 위계. |
| **품질 게이트 — 설계 기준** | 6개 가중 카테고리(타이포·구조·신뢰·데이터시각화·컬러·정렬)에 걸친 47개 결정론 검수, 90점 합격선, 하드페일 7종. 자동채점은 캘리브레이션 대기 중이며, 미달 덱이 조용히 `final`로 나가지 못하도록 게이트가 설계돼 있다. |
| **실제 크로미움 렌더** | 슬라이드는 HTML/CSS로 조판되고 실제 브라우저 엔진으로 렌더된다 — 보이는 그대로 export된다. |
| **8개 스타일 프리셋** | `apple` · `linear` · `notion` · `stripe` · `vercel` · `krds` · `toss-principles` · `kr-pick`. |
| **CJK 안전** | `keep-all` 줄바꿈과 한글 break 규칙 — 음절 중간에서 글자가 깨지지 않는다. |

## 갤러리

슬라이드 12장, 하나의 디자인 시스템. 이게 최고의 증명이다.

| | | |
|:-:|:-:|:-:|
| ![슬라이드 1](docs/gallery/slide-01.jpg) | ![슬라이드 2](docs/gallery/slide-02.jpg) | ![슬라이드 3](docs/gallery/slide-03.jpg) |
| ![슬라이드 4](docs/gallery/slide-04.jpg) | ![슬라이드 5](docs/gallery/slide-05.jpg) | ![슬라이드 6](docs/gallery/slide-06.jpg) |

<details>
<summary><b>12장 전체 보기</b></summary>

| | | |
|:-:|:-:|:-:|
| ![슬라이드 7](docs/gallery/slide-07.jpg) | ![슬라이드 8](docs/gallery/slide-08.jpg) | ![슬라이드 9](docs/gallery/slide-09.jpg) |
| ![슬라이드 10](docs/gallery/slide-10.jpg) | ![슬라이드 11](docs/gallery/slide-11.jpg) | ![슬라이드 12](docs/gallery/slide-12.jpg) |

</details>

## 작동 방식

![파이프라인](docs/media/pipeline.png)

디자인 시스템은 오늘 여기 있다. 아래 파이프라인은 한 문장을 완성된 덱으로 자동 변환하는 비전이다 — 각 단계가 다음 단계가 검증할 파일을 넘겨주는 6단계 체인:

1. **storyline** — 한 줄 브리프에서 출처와 claim을 수집.
2. **copy** — 액션 타이틀을 작성(마침표로 끝나는 단정문 — 명사 나열 금지).
3. **compose** — 고정된 레이아웃 어휘에서 슬라이드를 결정론적으로 조립(모델은 콘텐츠만, 코드가 좌표·색·z를 소유).
4. **grade** — 품질 게이트 실행; 합격선 미만은 `draft`로 격리되고 절대 조용히 승격되지 않는다.
5. **render** — 실제 크로미움 엔진으로 조판·페인트.
6. **export** — PNG / PDF / PPTX 산출.

storyline부터 render/export까지는 인큐베이터에 동작하는 코드로 존재하며, 엔드투엔드 자동채점과 최종 마감 패스가 남은 캘리브레이션 작업이다.

## 디자인 시스템

전체 룩은 강제되는 몇 개의 토큰으로 환원된다 — 스킬이 정본이다:

- **캔버스** — `--bg-0: #08090A`(순흑 금지, near-black), 드롭섀도 대신 깊이를 주는 surface 래더 `#101113 → #1A1B1E → #232427`.
- **액센트** — 라벤더블루 `#6E7BF2`와 시안 `#43C7F4`, 슬라이드당 액센트 1곳.
- **잉크** — `#FFFFFF` / `#A1A1A6` / `#6B6B70`, 3단 전경 위계.
- **타입** — Pretendard, display에 공격적 음수 트래킹, 슬라이드당 폰트 크기 ≤ 3종.
- **구조** — `no_box`, 알파화이트 hairline, 4모서리 크롬(브랜드칩 · 섹션 · 저자 · 페이지), 슬라이드당 지배 오브젝트 1개.

→ 전체 계약: [`skills/deck-factory/SKILL.md`](skills/deck-factory/SKILL.md)

## 레포 구조

```
deck-factory/
├── skills/deck-factory/     # 스킬 — SKILL.md + assets/styles.css
├── docs/
│   ├── media/               # hero.gif, pipeline.png
│   └── gallery/             # slide-01.jpg … slide-12.jpg
├── videos/                  # 모션그래픽 영상 3편
├── design/                  # DECK-STANDARD.md — 품질 계약(SSOT)
└── incubator/               # 파이프라인 코드: deck-grader, deck-tokens, deck-editor
```

**커스터마이징:** 프리셋을 고르거나(`/deck-factory "… preset: linear"`), 스킬의 스타일시트에서 토큰 값을 편집해 팔레트를 재조정한다. 프리셋은 구조와 시그니처 장치를 바꾸며, 색은 항상 토큰 변수를 통해 해석된다.

## 크레딧 & 라이선스

[MIT 라이선스](LICENSE)로 배포한다.

- **폰트** — [Pretendard](https://github.com/orioncactus/pretendard)(SIL Open Font License).
- **모션** — 쇼케이스 영상에 [GSAP](https://gsap.com)와 HyperFrames 사용.

---

<div align="center">

[Claude Code](https://claude.com/claude-code)로 제작 — [deck-factory 스킬](skills/deck-factory/SKILL.md) 구동.

**한 줄 넣으면, 발표할 만한 덱이 나온다.**

</div>
