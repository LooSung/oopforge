import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // `npm run check` runs ESLint with the OOPforge zones before the build.
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;
