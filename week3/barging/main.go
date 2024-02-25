// main.go
package main

import (
	"fmt"
	"sync/atomic"
)

type Mutex struct {
	lock uint32
}

func (m *Mutex) Lock() {
	for !atomic.CompareAndSwapUint32(&m.lock, 0, 1) {
		// loop
	}
}

func (m *Mutex) Unlock() {
	atomic.StoreUint32(&m.lock, 0)
}

func (m *Mutex) TryLock() bool {
	return atomic.CompareAndSwapUint32(&m.lock, 0, 1)
}

func main() {
	fmt.Println("vim-go")
}