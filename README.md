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

1. 초기엔 Observer pattern에 집중함

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

2. 비동기 동작 처리

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

3. 비동기 비효율성

- 위 비동기 처리에서 listener의 순서대로 실행되도록 함, 이렇게 되면 비동기 함수 -> 동기 -> 비동기 or not 이러한 형태로 전개되는데, 이는 비효율적이고 비동기 함수의 이점이 많이 사라짐
- Promise.all() 처럼 처리하면 비교적 효율적일 듯이라는 생각이 듬. python에서 똑같은 역할을 하는 asyncio.gather 발견 후 적용

### 2.1. Click detection

### 2.2. Define Emitter class

### 2.3. Implement click listeners

# Week 2.

# Week 3.

# Week 4.

# Week 5.

# Week 6.

# Week 7.

# Week 8.
