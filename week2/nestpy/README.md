# Week 2.

## 1. 문제 정의

### 1.1. 요구사항

- 1.1.1. 기능

  - main.py를 실행시켰을 때 우리의 예상대로 동작가능한 서버가 뜨면 성공입니다.
  - cats 폴더는 건드리지 않습니다. (건드려야 할 경우 저에게 문의해주세요.)
  - python의 http.server를 활용합니다.
  - @Injectable이 없는 모듈은 provider가 될 수 없습니다.
  - CatsService는 다른 모듈에서도 사용될 수 있게 구현되어야 합니다.
  - CatsController.**init** 의 argument 타입의 이름과 동일한 provider가 module에서 등록되지 않은 경우 nestjs와 같은 방식으로 에러가 나야 합니다.
  - CatsController에서 Body, Query, Param 와 같은 argument나 path는 전부 nestjs와 동일한 방식으로 동작합니다.

- 1.1.2. 사용 패턴

  - 팩토리 패턴: NestFactory
  - 싱글톤 패턴: NestApplication
  - 커맨드 패턴: Http input retrieval
    - 커맨드 패턴은 아무리 봐도 쓸만한 곳이 없어서 우선 간단한 곳에서 구현, invoker가 없어서 조금 어색하긴 하나, 목적을 채우고 있다고 생각
  - 데코레이터 패턴: 전반적인 Decorators
  - 전략 패턴: Get / Post

    - 전략 패턴도 약간 애매하긴 하나, 로직의 차이가 생길 수 있을 만한 Get / Post에 적용.
    - 현재는 동일한 로직이 많아서 사실 나누는 게 의미가 없으나, 확장성, 독립성 측면에서 Strategy 패턴 적용

  - DI
  - IoC
  - DIP

- 1.1.3. 필요 데코레이터 및 클래스
  - @Injectable
  - @Controller
  - @Module
  - @Get
  - @Post
  - NestFactory
  - Body, Param, Query

## 2. 설계

### 2.1. Module -> Controller -> Provider 구현

1. Module, Factory는 singleton
2. Controller, Provider은 not singleton

### 2.2. 요구사항 충족

- main.py를 실행시켰을 때 우리의 예상대로 동작가능한 서버가 뜨면 성공입니다.
  - 아래 요구사항 충족 및 서버 실행(완료)
- python의 http.server를 활용합니다.
  - main.py에서 app을 가져오고, app 내에서 모듈 세팅 및 http.server을 사용하여 서버가 뜨도록 구현(완료)
- @Injectable이 없는 모듈은 provider가 될 수 없습니다.(완료)
  - Injectable이 붙은 클래스를 마킹하여, 사용하도록 구현(완료)
  - 해당 클래스의 metadata를 수정하여, 해당 클래스가 provider로 등록되도록 구현(완료)
- CatsService는 다른 모듈에서도 사용될 수 있게 구현되어야 합니다.(완료)
- CatsController.**init** 의 argument 타입의 이름과 동일한 provider가 module에서 등록되지 않은 경우 nestjs와 같은 방식으로 에러가 나야 합니다.(완료)
  - CatsController에서 init의 argument를 순회하며, 해당 argument의 타입이 provider로 등록되어 있는지 확인(완료)
- CatsController에서 Body, Query, Param 와 같은 argument나 path는 전부 nestjs와 동일한 방식으로 동작합니다.(완료)
