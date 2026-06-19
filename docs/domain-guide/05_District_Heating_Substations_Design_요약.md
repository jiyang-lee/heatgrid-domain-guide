# 05. District Heating Substations Design 요약

> **문서 역할**  
> 설계와 구성 PDF 상세 요약
> **대상 독자**  
> 기계실 구성요소를 처음 배우는 사람
>
> **읽는 시간**  
> 20분
> **난이도**  
> 입문 ~ 중급
>
> **선수지식**  
> [04_해외_지역난방_구조와_운영_가이드.md](./04_해외_지역난방_구조와_운영_가이드.md)
>
> **원문 링크**  
> [PDF](https://www.energiforetagen.se/4a4e6b/globalassets/energiforetagen/det-erbjuder-vi/publikationer/f101-district-heating-substations-design-and-installation.pdf)
>
> **로컬 자산 경로**  
> [05_substation_design.pdf](./assets/pdf/05_substation_design.pdf)

---

## 왜 읽어야 하는가

이 문서는 기계실을 부품 집합이 아니라 하나의 시스템으로 보게 해 준다. HeatGrid가 설비별 센서와 고장을 연결하려면 바로 이 설계 관점이 필요하다.

## 핵심 개념

- substation은 열교환기, 펌프, 밸브, 센서, 계측기, 안전장치가 함께 움직이는 시스템이다.
- 예방정비, 상태기반 정비, 사후정비를 구분해서 설계와 운영을 연결해야 한다.

## 중요한 번역 포인트

- 설계, 배치, 운전, 유지관리 요구사항은 따로 놀지 않고 함께 고려되어야 한다.
- 열교환기, 센서, 밸브, 펌프, 필터는 하나의 연동 구조로 봐야 한다.

## 실무 예시

유량 저하가 보일 때 현장에서는 펌프만 보지 않는다. 필터 막힘, 밸브 반응, 차압 변화까지 같이 보며 시스템 전체를 의심한다.

## PreDist 연결 예시

PreDist에서 유량과 온도차가 같이 흔들리면 단일 센서 이상보다 열교환기 또는 순환계통 문제 후보를 먼저 올리는 식으로 연결할 수 있다.

## HeatGrid 적용 포인트

- Agent는 부품 단위보다 시스템 단위 이상을 설명해야 한다.
- 정비 분류를 `사후정비`, `예방정비`, `상태기반 정비`로 나눠둘 필요가 있다.

## 초심자 체크포인트

- preventive maintenance와 corrective maintenance 차이를 설명할 수 있는가
- 기계실을 단일 부품이 아니라 시스템으로 이해하고 있는가
- 센서 이상을 설비 구조와 연결해 해석할 수 있는가
