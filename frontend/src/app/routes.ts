import { createBrowserRouter } from "react-router";
import Root from "./layouts/root";
import Home from "./pages/sections/home";
import Welcome from "./pages/sections/Welcome";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: Home },
      { path: "welcome", Component: Welcome },
    ],
  },
]);