# 10. Anomaly Detection Review 요약

> **문서 역할**  
> 이상탐지/고장 연구 요약

> **대상 독자**  
> 이 분야의 연구 지형을 빠르게 보고 싶은 사람

> **읽는 시간**  
> 15분

> **난이도**  
> 중급

> **선수지식**  
> [01_PreDist_논문_정리.md](./01_PreDist_논문_정리.md)

> **원문 링크**  
> [ResearchGate 리뷰](https://www.researchgate.net/publication/370164650_Fault_and_anomaly_detection_in_district_heating_substations_A_survey_on_methodology_and_data_sets), [ML anomaly detection thesis PDF](https://www.diva-portal.org/smash/get/diva2%3A1988416/FULLTEXT01.pdf)

> **로컬 PDF 경로**  
> ResearchGate 리뷰는 로컬 보관 불가, [10_ml_anomaly_detection_thesis.pdf](./assets/pdf/10_ml_anomaly_detection_thesis.pdf)

---

## 왜 이 문서를 읽어야 하는가

PreDist 하나만 보면 데이터셋은 이해되지만, 어떤 fault와 anomaly가 중요한지 넓은 맥락이 부족할 수 있다.

## 핵심 해설

- district heating substation 분야는 일반 산업 PdM보다 상대적으로 연구가 적었다.
- 중요한 것은 catastrophic failure보다 `부분 고장`, `성능 저하`, `제어 이상`, `에너지 비효율`이다.
- anomaly detection은 `미지의 이상`을 조기 포착하는 데 유용하다.

## HeatGrid에 직접 쓰는 포인트

- HeatGrid는 완전 파손보다 `성능 저하 + 운영 리스크`를 먼저 다루는 것이 자연스럽다.
- 따라서 anomaly score는 우선순위 엔진의 핵심 입력 중 하나가 된다.

## 초심자 체크포인트

- 이 도메인에서 이상탐지가 왜 중요한지 설명할 수 있는가
- 고장 분류와 이상탐지를 어떻게 함께 쓸지 말할 수 있는가
