import React from "react";
import ReactDOM from "react-dom";
import { Auth0Provider } from "@auth0/auth0-react";
import Navbar from "@/components/navbar";
import { AuthProvider } from "@/contexts/context";
import "bootstrap/dist/css/bootstrap.min.css";

function App({ Component, pageProps }) {
  return (
    <Auth0Provider
      domain="dev-hwgb8d1f3r3ztqaq.us.auth0.com"
      clientId="Rlj2w6tlzrrxI4QXFPwxBI4COkC1MYeb"
      authorizationParams={{
        redirect_uri: typeof window != "undefined" && location.origin,
        audience: "pybo",
        scope: "openid profile email",
        cacheLocation: "localStorage",
        useRefreshTokens: true,
      }}
    >
      <AuthProvider>
        <Navbar />
        <Component {...pageProps} />
      </AuthProvider>
    </Auth0Provider>
  );
}

// Disable SSR for all pages
App.getInitialProps = async ({ Component, ctx }) => {
  const pageProps = Component.getInitialProps ? await Component.getInitialProps(ctx) : {};

  return { pageProps, unstable_runtimeJS: false };
};

export default App;
