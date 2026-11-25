import { StandardSchemaValidationPipe, type INestApplication } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

// Shared by main.ts and the e2e tests, so both run the same pipes and documents.
export function configureApp(app: INestApplication): INestApplication {
  app.useGlobalPipes(new StandardSchemaValidationPipe());
  const config = new DocumentBuilder().setTitle('Calculator (layered 3-tier)').setVersion('0.1.0').build();
  SwaggerModule.setup('swagger-ui', app, () => SwaggerModule.createDocument(app, config), {
    jsonDocumentUrl: 'v3/api-docs',
  });
  return app;
}
