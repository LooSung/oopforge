// OOPforge enforcement for the typescript-next-layered stack. The import zones
// replace the Java reference's ArchUnit ArchitectureTest.
import { defineConfig } from 'eslint/config';
import importPlugin from 'eslint-plugin-import';
import tseslint from 'typescript-eslint';

const CALCULATOR = './src/server/calculator';

const layerZones = [
  {
    target: `${CALCULATOR}/domain`,
    from: './',
    except: [`${CALCULATOR}/domain`],
    message: '[domain-isolation] domain/ imports nothing outside domain/: no framework, library, or other layer.',
  },
  {
    target: [`${CALCULATOR}/controller`, './src/app'],
    from: `${CALCULATOR}/repository`,
    message: '[controller-no-repository] Controllers and route files go through the service, never a repository.',
  },
  {
    target: `${CALCULATOR}/service`,
    from: `${CALCULATOR}/controller`,
    message: '[service-no-controller] The service layer never imports the controller layer.',
  },
  {
    target: `${CALCULATOR}/repository`,
    from: [`${CALCULATOR}/service`, `${CALCULATOR}/controller`],
    message: '[repository-downward-only] The repository never imports the service or controller layer.',
  },
];

const FRAMEWORK_IMPORTS = [
  'next', 'next/*', 'react', 'react/*', 'react-dom', 'react-dom/*', 'server-only', 'zod', 'zod/*',
  'prisma', '@prisma/*', 'drizzle-orm', 'drizzle-orm/*', 'typeorm', 'mongoose', 'sequelize', 'node:*',
];

export default defineConfig(
  { ignores: ['.next/**', 'node_modules/**', 'next-env.d.ts'] },
  tseslint.configs.recommended,
  {
    files: ['src/**/*.ts', 'tests/**/*.ts'],
    plugins: { import: importPlugin },
    settings: {
      // The default node resolver does not resolve .ts imports, which silently
      // disables no-restricted-paths. Proven with a negative test.
      'import/resolver': { node: { extensions: ['.js', '.ts'] } },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      'max-lines': ['error', { max: 300 }],
      'max-lines-per-function': ['error', { max: 20 }],
      'import/no-restricted-paths': ['error', { zones: layerZones }],
    },
  },
  {
    files: ['src/**/*.ts'],
    rules: {
      '@typescript-eslint/explicit-module-boundary-types': 'error',
      '@typescript-eslint/parameter-properties': [
        'error',
        { allow: ['readonly', 'private readonly', 'protected readonly', 'public readonly'] },
      ],
    },
  },
  {
    files: ['src/server/calculator/domain/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        { patterns: [{ group: FRAMEWORK_IMPORTS, message: '[domain-framework-free] The domain stays runtime- and framework-agnostic.' }] },
      ],
      'no-restricted-syntax': [
        'error',
        { selector: 'PropertyDefinition[readonly!=true]', message: '[domain-readonly] Domain state is readonly.' },
        {
          selector: 'MethodDefinition[kind="constructor"]:not([accessibility="private"])',
          message: '[domain-factory] Domain classes keep a private constructor behind a static factory.',
        },
      ],
    },
  },
);
