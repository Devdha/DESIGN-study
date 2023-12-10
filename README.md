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

### 1.2. Observer patter이란?

## 2. 구현

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
