## 작업 시작 전 필수 확인

코드 수정 전 반드시 다음을 먼저 확인한다.

1. 최종 3주제 HTML 문서
2. docs/guide 내부 md 파일
3. README.md
4. 기존 코드 구조
5. pyproject.toml
6. .env.example

위 문서를 확인하지 않고 새 구조, 새 기술, 새 의존성을 추가하지 않는다.

## 개발 규칙

- Python 3.12 사용
- 패키지 관리는 uv 사용
- pip install 금지
- 새 패키지는 uv add로만 추가
- FastAPI router에는 비즈니스 로직 작성 금지
- service, db, config, utils로 책임 분리
- 설정값은 .env 또는 config로 분리
- print 대신 logging 사용
- 주석은 한국어로 작성
- 루트 디렉토리에 임시 파일 생성 금지
- 테스트 파일은 tests 또는 scripts에 작성