// Route handlers are plain functions of a Request, so tests call them directly
// instead of starting a server (the counterpart of Spring's MockMvc).
export function calculationRequest(body: string, headers: Record<string, string> = {}): Request {
  return new Request('http://localhost/calculations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body,
  });
}
