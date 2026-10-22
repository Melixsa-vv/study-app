import { useState } from "react";
import { useNavigate } from "react-router";
import AuthContainer from "../../../components/AuthContainer";
import Button from "../../../components/Button";
import { SIZES } from "../../../constants/sizes";

const API_URL = import.meta.env.VITE_API_URL;

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.SyntheticEvent) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      // 2. Llamada real a tu endpoint de FastAPI
      const response = await fetch(`${API_URL}/auth/login/access-token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Wrong Credentials");
      }

      const data = await response.json();

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("is_authenticated", "true");

      navigate("/", { replace: true });
    } catch (err) {
      console.error("Login Error:", err);
    }
  };
  const INPUT_CLASSES =
    "w-full p-3 bg-white border border-slate-200 rounded-xl text-sm outline-none focus:border-pink-400 transition-colors";
  const INPUT_TEXT = "text-xs font-semibold text-slate-600";
  return (
    <AuthContainer
      title="Create Account"
      subtitle="Join Study Together"
      onBack={() => navigate("/welcome")}
    >
      <form onSubmit={handleLogin} className="flex flex-col gap-4 w-full">
        <div className="flex flex-col gap-1">
          <label className={`${INPUT_TEXT}`}>Email</label>
          <input
            type="email"
            required
            placeholder="name@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`${INPUT_CLASSES}`}
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className={`${INPUT_TEXT}`}>Password</label>
          <input
            type="password"
            required
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`${INPUT_CLASSES}`}
          />
        </div>

        <Button
          size={`
            w-full
            ${SIZES.buttons.sm.h}
            ${SIZES.buttons.md.text}
            `}
          variant="accent"
          type="submit"
        >
          Sign Up
        </Button>
      </form>
    </AuthContainer>
  );
}
