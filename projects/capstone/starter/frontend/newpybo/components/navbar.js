import React, { useEffect, useState } from "react";
import {useAuthContext} from "@/contexts/context";

export default function Navbar() {
  const { authStatus, loginWithRedirect, logout, user } = useAuthContext();

  // fix Hydration Error
  const [loginText, setLoginText] = useState();

  // fix Hydration Error
  useEffect(() => {
    if (authStatus) {
      setLoginText(`${user && user.name ? user.name : ""} 로그아웃`);
    } else {
      setLoginText("로그인");
    }
  }, [authStatus]);

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light border-bottom">
      <div className="container">
        <a className="navbar-brand" href="/">
          Pybo
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          {authStatus ? (
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <button
                  className="nav-link btn"
                  onClick={() =>
                    logout({
                      logoutParams: {
                        returnTo: typeof window != "undefined" && location.origin,
                      },
                    })
                  }
                >
                  {loginText}
                </button>
              </li>
            </ul>
          ) : (
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <button className="nav-link btn" onClick={() => loginWithRedirect()}>
                  {loginText}
                </button>
              </li>
            </ul>
          )}
        </div>
      </div>
    </nav>
  );
}
