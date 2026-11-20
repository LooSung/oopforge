import { expect, it } from 'vitest';

import { GET } from '../../src/app/v3/api-docs/route';

it('openApiDocsAvailable', async () => {
  const response = GET();
  const document = await response.json();

  expect(response.status).toBe(200);
  expect(document.openapi).toBeDefined();
  expect(document.paths['/api/v1/calculations']).toBeDefined();
});
