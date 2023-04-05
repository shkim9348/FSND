import { useAuth0 } from "@auth0/auth0-react";
import { createContext, useContext, useEffect, useState } from "react";

export const getCsrfToken = async () => {
  return await fetch(`${process.env.API_URL}/csrftoken`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    // cookie sharing
    // cf. axios cookiejar
    credentials: "include",
  })
    .then((res) => res.text())
    .then((data) => data);
};

const AuthContext = createContext();

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("AuthContext error");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const { isAuthenticated, isLoading, user, loginWithRedirect, logout, getAccessTokenSilently } =
    useAuth0();

  // auth status
  const savedAuthStatus =
    typeof window != "undefined" && (localStorage.getItem("isAuthenticated") || false);

  // user
  const savedUser =
    typeof window != "undefined" && JSON.parse(localStorage.getItem("user") || "{}");

  if (!isLoading) {
    typeof window != "undefined" && localStorage.setItem("isAuthenticated", isAuthenticated);
    typeof window != "undefined" && localStorage.setItem("user", JSON.stringify(user) || "{}");
  }

  // get accessToken
  useEffect(() => {
    (async () => {
      if (isAuthenticated && !accessToken) {
        const token = await getAccessTokenSilently();
        setAccessToken(token);
      }
    })();
  }, [isAuthenticated]);

  const context = {
    authStatus: isLoading ? savedAuthStatus : isAuthenticated,
    user: isLoading ? savedUser : user,
    loginWithRedirect: loginWithRedirect,
    logout: logout,
    accessToken: accessToken || "",
  };
  return <AuthContext.Provider value={context}>{children}</AuthContext.Provider>;
};
