import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  env:{
    PROJECT_NAME: process.env.PROJECT_NAME,
  }
};

export default nextConfig;
