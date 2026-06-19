# 09. ASHRAE 180 요약

> **문서 역할**  
> 유지관리 계획 표준 요약
> **대상 독자**  
> maintenance plan 구조를 이해하려는 사람
>
> **읽는 시간**  
> 15분
> **난이도**  
> 중급
>
> **선수지식**  
> [08_District_Energy_PM_Checklist_요약.md](./08_District_Energy_PM_Checklist_요약.md)
>
> **원문 링크**  
> [ASHRAE Preview PDF](https://www.ashrae.org/File%20Library/Technical%20Resources/Bookstore/previews_2016639_pre.pdf)
>
> **로컬 자산 경로**  
> [09_ashrae_180_preview.pdf](./assets/pdf/09_ashrae_180_preview.pdf)

---

## 왜 읽어야 하는가

HeatGrid가 정말 운영용 Agent가 되려면 알람이 아니라 계획 문서를 만들 수 있어야 한다. ASHRAE 180은 그 계획 문서가 어떤 구조를 가져야 하는지 보여 준다.

## 핵심 개념

- 유지관리 계획에는 설비 inventory, 점검 항목, 일정, 상태 지표, 결과 기록이 들어간다.
- inspection은 상태를 보는 행위이고, maintenance는 실제 조치까지 포함한다.

## 중요한 번역 포인트

- condition indicator는 설비 열화를 판단하는 기준값이다.
- 유지관리 계획은 설비 목록, 절차, 일정, 기록 체계를 포함해야 한다.

## 실무 예시

같은 온도 이상이라도 condition indicator가 이미 나빠진 설비라면 단순 관찰보다 우선 출동 대상으로 올릴 수 있다.

## PreDist 연결 예시

PreDist의 반복 이상 패턴을 condition indicator 후보로 삼아, 특정 설비가 “주의” 단계인지 “즉시 조치” 단계인지 구분할 수 있다.

## HeatGrid 적용 포인트

- 작업 오더에는 설비 ID, 점검 항목, 상태 지표, 기록 형식이 함께 있어야 한다.
- 단순 경보보다 운영 계획 문서에 가까운 출력이 필요하다.

## 초심자 체크포인트

- inspection과 maintenance 차이를 설명할 수 있는가
- condition indicator가 왜 중요한지 말할 수 있는가
- HeatGrid 출력이 왜 계획 문서에 가까워야 하는지 이해했는가
