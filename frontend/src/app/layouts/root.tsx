import { Outlet } from "react-router-dom";

export default function Root() {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}
