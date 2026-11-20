// OOPforge enforcement for the typescript-next-hexagonal stack with the CQRS
// overlay. The import zones replace the Java reference's ArchUnit ArchitectureTest.
import { defineConfig } from 'eslint/config';
import importPlugin from 'eslint-plugin-import';
import tseslint from 'typescript-eslint';

const CALCULATOR = './src/server/calculator';

const hexagonalCqrsZones = [
  {
    target: `${CALCULATOR}/domain`,
    from: './',
    except: [`${CALCULATOR}/domain`],
    message: '[domain-isolation] domain/ imports nothing outside domain/: no framework, library, or other layer.',
  },
  {
    target: `${CALCULATOR}/application`,
    from: [`${CALCULATOR}/adapter`, `${CALCULATOR}/config`],
    message: '[application-no-adapter] The application core never imports an adapter or the wiring.',
  },
  {
    target: `${CALCULATOR}/application/command`,
    from: `${CALCULATOR}/application/query`,
    message: '[command-no-query] The command side never imports the query side.',
  },
  {
    target: `${CALCULATOR}/application/query`,
    from: `${CALCULATOR}/application/command`,
    message: '[query-no-command] The query side never imports the command side.',
  },
];

const FRAMEWORK_IMPORTS = [
  'next', 'next/*', 'react', 'react/*', 'react-dom', 'react-dom/*', 'server-only', 'zod', 'zod/*',
  'prisma', '@prisma/*', 'drizzle-orm', 'drizzle-orm/*', 'typeorm', 'mongoose', 'sequelize', 'node:*',
];

const MUTATING_CALL = '/^(save|delete|update|insert|persist|store|remove)$/';
const READ_SHAPED_TYPE = '/(Response|Summary|Dto|DTO|View|ReadModel)$/';

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
      'import/no-restricted-paths': ['error', { zones: hexagonalCqrsZones }],
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
  {
    files: ['src/**/*QueryService.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: `CallExpression[callee.property.name=${MUTATING_CALL}], CallExpression[callee.name=${MUTATING_CALL}]`,
          message: '[query-no-side-effects] The query side only reads.',
        },
      ],
    },
  },
  {
    files: ['src/**/*CommandService.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: `:function > TSTypeAnnotation TSTypeReference[typeName.name=${READ_SHAPED_TYPE}]`,
          message: '[command-returns-id] The command side returns an id or void, never a read-shaped type.',
        },
      ],
    },
  },
);
