import { useEffect } from "react";
import { Outlet, useNavigate, useLocation } from "react-router";

export default function Root() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const isAuthenticated = localStorage.getItem("is_authenticated") === "true";
    const publicPaths = ["/welcome", "/register", "/login"];
    const isPublicPath = publicPaths.includes(location.pathname);

    if (!isAuthenticated && !isPublicPath) {
      navigate("/welcome", { replace: true });
    }

    if (isAuthenticated && isPublicPath) {
      navigate("/", { replace: true });
    }
  }, [navigate, location.pathname]);

  return (
    <div className="min-h-screen w-full bg-slate-50 flex flex-col">
      <Outlet />
    </div>
  );
}
