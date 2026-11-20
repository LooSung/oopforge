import { expect, it } from 'vitest';
import { GET } from '../../../../../src/server/calculator/adapter/web/apiDocsController';
import { CORRELATION_HEADER } from '../../../../../src/server/calculator/adapter/web/correlationAuditFilter';

// TypeScript addition: the Java hexagonal reference ships no springdoc, so this
// pins the generated contract to the one HTTP route and leaves the action out.
it('documentsTheCalculationRouteOnly', async () => {
  const response = await GET(new Request('http://localhost/v3/api-docs'));
  const document = await response.json();

  expect(response.status).toBe(200);
  expect(response.headers.has(CORRELATION_HEADER)).toBe(true);
  expect(Object.keys(document.paths)).toEqual(['/calculations']);
  expect(Object.keys(document.paths['/calculations'])).toEqual(['post']);
  expect(Object.keys(document.paths['/calculations'].post.responses))
    .toEqual(['201', '400', '409', '422', '500']);
  expect(Object.keys(document.components.schemas).sort())
    .toEqual(['ApiError', 'CalculateRequest', 'CalculationResponse']);
});
