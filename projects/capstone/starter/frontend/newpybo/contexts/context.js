import { useAuth0 } from "@auth0/auth0-react";
import { createContext, useContext, useEffect, useState } from "react";

// Auth0 context
const AuthToken = createContext();

export const useAuthToken = () => {
  return useContext(AuthToken);
};

export const AuthTokenProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();

  // get accessToken
  useEffect(() => {
    (async () => {
      if (isAuthenticated && !accessToken) {
        const token = await getAccessTokenSilently();
        setAccessToken(token);
      }
    })();
  }, [isAuthenticated]);

  return <AuthToken.Provider value={accessToken}>{children}</AuthToken.Provider>;
};
