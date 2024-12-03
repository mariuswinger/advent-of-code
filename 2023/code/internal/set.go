package internal

type Set struct {
	values map[int64]struct{}
}

func (s *Set) Length() int64 {
	return int64(len(s.values))
}

func (s *Set) Has(i int64) bool {
	_, ok := s.values[i]
	return ok
}

func (s *Set) Add(i int64) {
	s.values[i] = struct{}{}
}

func NewSet() *Set {
	s := &Set{}
	s.values = map[int64]struct{}{}
	return s
}

func FromSlice(l []int64) *Set {
	s := NewSet()
	for _, v := range l {
		s.Add(v)
	}
	return s
}

func (s *Set) Intersect(s2 *Set) *Set {
	res := NewSet()
	for v := range s.values {
		if s2.Has(v) == false {
			continue
		}
		res.Add(v)
	}
	return res
}
