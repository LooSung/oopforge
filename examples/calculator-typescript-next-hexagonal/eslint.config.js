// OOPforge enforcement for the TypeScript Next.js hexagonal reference. The
// import zones replace the Java reference's ArchUnit ArchitectureTest.
import importPlugin from 'eslint-plugin-import';
import tseslint from 'typescript-eslint';

const CALCULATOR = './src/server/calculator';

const zones = [
  {
    target: `${CALCULATOR}/domain`,
    from: '.',
    except: [`${CALCULATOR}/domain`],
    message: 'Domain imports nothing outside domain/: no next, react, zod, ORM, adapter, or application code.',
  },
  {
    target: `${CALCULATOR}/application`,
    from: [`${CALCULATOR}/adapter`, `${CALCULATOR}/config`],
    message: 'Application depends only on domain and its own ports; adapters and config depend on it.',
  },
  {
    target: './src/app',
    from: '.',
    except: [`${CALCULATOR}/adapter/web`, './src/app'],
    message: 'Route files are one-line re-exports from adapter/web.',
  },
];

// Class state is readonly or private behind behaviour methods (no public setters).
const publicMutableState = [
  {
    selector:
      "PropertyDefinition:not([readonly=true]):not([accessibility='private']):not([accessibility='protected']):not([key.type='PrivateIdentifier'])",
    message: 'Class fields are readonly or private.',
  },
  {
    selector: "TSParameterProperty:not([readonly=true]):not([accessibility='private']):not([accessibility='protected'])",
    message: 'Public constructor properties are readonly.',
  },
  {
    selector: "MethodDefinition[kind='set']:not([accessibility='private'])",
    message: 'No public setters: expose a behaviour method instead.',
  },
];

export default tseslint.config(
  { ignores: ['.next/**', 'node_modules/**', 'next-env.d.ts'] },
  tseslint.configs.recommended,
  {
    files: ['**/*.ts'],
    plugins: { import: importPlugin },
    settings: {
      // The default node resolver does not resolve .ts imports, which silently
      // disables no-restricted-paths. Proven with a negative test (README).
      'import/resolver': { node: { extensions: ['.js', '.ts'] } },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      'import/no-restricted-paths': ['error', { zones }],
      'max-lines': ['error', { max: 300 }],
      'max-lines-per-function': ['error', { max: 20 }],
    },
  },
  {
    files: ['src/**/*.ts'],
    rules: {
      '@typescript-eslint/explicit-module-boundary-types': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      'no-restricted-syntax': ['error', ...publicMutableState],
    },
  },
  {
    // Node built-ins are not file paths, so the zone cannot see them.
    files: ['src/server/calculator/domain/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        { patterns: [{ regex: '^[^.]', message: 'Domain imports only relative domain modules.' }] },
      ],
    },
  },
);
