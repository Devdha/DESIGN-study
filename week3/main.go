package main

import (
	"fmt"
	"sync/atomic"
	"unsafe"
)

type Mutex struct {
	isLocked  int32
	next    chan struct{}
	isWaiting int32
}

func (m *Mutex) Lock() {
	if atomic.AddInt32(&m.isWaiting, 1) == 1 {
		atomic.StoreInt32(&m.isLocked, 1)
		return
	}

	ch := make(chan struct{})
	defer close(ch)
	
	for {
		prevNext := atomic.LoadPointer((*unsafe.Pointer)(unsafe.Pointer(&m.next)))
		if atomic.CompareAndSwapPointer((*unsafe.Pointer)(unsafe.Pointer(&m.next)), prevNext, unsafe.Pointer(&ch)) {
			break
		}
	}

	for atomic.LoadInt32(&m.isLocked) != 0 { 
		//
	}
	
	atomic.StoreInt32(&m.isLocked, 1)
}

func (m *Mutex) Unlock() {
	if atomic.LoadInt32(&m.isWaiting) == 0 {
		atomic.StoreInt32(&m.isLocked, 0)
		return
	}

	if atomic.AddInt32(&m.isWaiting, -1) > 0 {
		if m.next != nil {
			close(m.next) 
			ch := make(chan struct{})
			defer close(ch)
			for {
				old := atomic.LoadPointer((*unsafe.Pointer)(unsafe.Pointer(&m.next)))
				if atomic.CompareAndSwapPointer((*unsafe.Pointer)(unsafe.Pointer(&m.next)), old, unsafe.Pointer(&ch)) {
					break
				}
			}
		}
	} else {
		atomic.StoreInt32(&m.isLocked, 0)
	}
}

func (m *Mutex) TryLock() bool {
	if atomic.LoadInt32(&m.isWaiting) == 0 && atomic.CompareAndSwapInt32(&m.isLocked, 0, 1) {
		return true
	}
	return false
}


func main() {
	m := new(Mutex)
	for i := 0; i < 100000; i++ {
		func() {
			m.Lock()
			if (i % 30) == 0 {
				fmt.Println(i)
			}
			m.Unlock()
		}()
	}
}