import { useEffect } from "react";
import { Outlet, useNavigate, useLocation } from "react-router";

export default function Root() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const isAuthenticated = localStorage.getItem("is_authenticated") === "true";

    if (!isAuthenticated && location.pathname !== "/welcome") {
      navigate("/welcome", { replace: true });
    }

    if (isAuthenticated && location.pathname === "/welcome") {
      navigate("/", { replace: true });
    }
  }, [navigate, location.pathname]);

  return (
    <div className="min-h-screen w-full bg-slate-50 flex flex-col">
      <Outlet />
    </div>
  );
}
