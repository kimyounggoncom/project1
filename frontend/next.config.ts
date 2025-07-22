import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // ▼▼▼ 바로 이 부분을 추가해주세요! ▼▼▼
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  // ▲▲▲ 여기까지 입니다 ▲▲▲

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