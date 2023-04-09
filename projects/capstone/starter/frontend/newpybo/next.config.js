/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  trailingSlash: true,
  output: "export",
  env: {
    API_URL: "https://shkim-api.ver.team",
  }
}

module.exports = nextConfig
