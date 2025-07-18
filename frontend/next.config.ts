import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  output: 'standalone',
  experimental: {
    turbo: false,
  },
  swcMinify: false,
  compiler: {
    removeConsole: false,
  },
};

export default nextConfig;
