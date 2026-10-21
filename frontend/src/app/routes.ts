import { createBrowserRouter } from "react-router";
import Root from "./layouts/root";
import Home from "./pages/sections/home";
import Welcome from "./pages/sections/Welcome";
import Register from "./pages/sections/auth/Register";
import Login from "./pages/sections/auth/Login";


export const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: Home },
      { path: "welcome", Component: Welcome },
      { path: "register", Component: Register},
      { path: "login", Component: Login},
    ],
  },
]);