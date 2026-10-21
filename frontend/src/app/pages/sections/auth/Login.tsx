import { useState } from "react";
import { useNavigate } from "react-router";
import AuthContainer from "../../../components/AuthContainer";
import Button from "../../../components/Button";
import { SIZES } from "../../../constants/sizes";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e: React.SyntheticEvent) => {
    e.preventDefault();
    console.log("Registering:", { email, password });
    localStorage.setItem("is_authenticated", "true");
    navigate("/", { replace: true });
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
