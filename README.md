Title Format: "# Week {i}. {name}"

# Week 1. Observer: Event Emitter

## 1. 개념정리

### 1.1. Emitter란?

- 브라우저 자바스크립트에는 i/o 등 이벤트를 처리하기 위해 `events` 모듈이 존재함
- nodejs에서는 `events` 모듈이 없기 때문에 이를 유사하게 사용할 수 있는 `EventEmitter`가 존재

  ```typescript
  const EventEmitter = require("node:events");
  const eventEmitter = new EventEmitter();

  eventEmitter.on("start", () => {
    console.log("started");
  });
  // When we run
  eventEmitter.emit("start");
  ```

### 1.2. Observer pattern이란?

- 상태 변화를 알리기 위해 여러가지 방식이 있는데, 관찰자가 계속 방문하거나 상태의 주체가 상태를 계속해서 모두에게 알리는 방식은 비효율적임
- 이를 해결하기 위해 주체가 관찰자들에게 상태 변화를 알리기 위해 사용하는 방식
- 주체는 관찰자들을 등록하고, 관찰자들은 subscribe하는 방식. 상태 변화가 생기면 관찰자들을 순회하며 상태 변화 알림

## 2. 구현

### 2.1. 초기엔 Observer pattern에 집중함

- subscribing 하는 Emitter 클래스 구현
- 요구사항 중, decorator가 필요하다는 것을 인지

  - 일반적인 function decorator와 다른 decorator factory 사용
  - 함수 파라미터는 그대로 사용하면서 response인 데코레이더로 래핑하는 것을 확인

    ```python
    def on(self, event, filter):
        def decorator(func):
            self.__add(event, func, False, filter)

        return decorator
    ```

- 그 외 listener(event) 관리 메소드는 추가/제거 하는 방식으로 구현 완료
- 문제점: Emitter만 클래스화 하고 다른 건 다 딕셔너리에 넣어버림 / 코드는 짧아졌지만, 이렇게 코드짜면 인지도 힘들고 유지보수도 힘들 듯

### 2.2. 비동기 동작 처리

- 동기적인 동작을 완료할 때 쯤 아래 에러 발생
  ```
  RuntimeWarning: coroutine 'on_click_right' was never awaited
  [task(kwargs) for task in syncTasks]
  RuntimeWarning: Enable tracemalloc to get the object allocation traceback
  ```
- 비동기 동작을 위해 asyncio 모듈 사용
- 하지만, 비동기 함수 사용 시 await 또는 asyncio.run()을 통해 실패 케이스 핸들링 등 작업이 필요
- 그런 작업 없이 동기 함수처럼 호출하여 위 에러 발생
- 이를 해결하기 위해, listener 중 async 함수인 아이들을 별도로 실행

### 2.3. 비동기 비효율성

- 위 비동기 처리에서 listener의 순서대로 실행되도록 함, 이렇게 되면 비동기 함수 -> 동기 -> 비동기 or not 이러한 형태로 전개되는데, 이는 비효율적이고 비동기 함수의 이점이 많이 사라짐
- Promise.all() 처럼 처리하면 비교적 효율적일 듯이라는 생각이 듬. python에서 똑같은 역할을 하는 asyncio.gather 발견 후 적용

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

# Week 3.

# Week 4.

# Week 5.

# Week 6.

# Week 7.

# Week 8.
