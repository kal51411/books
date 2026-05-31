import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.post('http://localhost:8000/api/v1/ask', JSON.stringify({ query: 'Can police arrest without warrant?' }), { headers: { 'Content-Type': 'application/json' } });
  check(res, { 'status is 200': (r) => r.status === 200 });
}
