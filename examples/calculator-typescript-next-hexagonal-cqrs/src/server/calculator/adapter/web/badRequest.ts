export function badRequest(request: Request, message: string): Response {
  const path = new URL(request.url).pathname;
  return Response.json({ status: 400, error: 'Bad Request', message, path }, { status: 400 });
}
