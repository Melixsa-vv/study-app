import { useState } from "react";
import { useNavigate } from "react-router";
import AuthContainer from "../../../components/AuthContainer";
import Button from "../../../components/Button";
import { SIZES } from "../../../constants/sizes";

const API_URL = import.meta.env.VITE_API_URL;

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user_name, setUserName] = useState("");

  const handleRegister = async (e: React.SyntheticEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          user_name: user_name,
          email: email,
          password: password,
        }),
      });

      if (!response.ok) {
        throw new Error("Wrong Credentials");
      }
      const loginFormData = new URLSearchParams();
      loginFormData.append("username", email);
      loginFormData.append("password", password);

      const loginResponse = await fetch(`${API_URL}/auth/login/access-token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: loginFormData,
      });

      if (!loginResponse.ok) {
        throw new Error("Registration succeeded, but auto-login failed");
      }

      const loginData = await loginResponse.json();

      localStorage.setItem("access_token", loginData.access_token);
      localStorage.setItem("is_authenticated", "true");

      console.log("All Good!");

      navigate("/", { replace: true });
    } catch (err) {
      console.error("Registration Error: ", err);
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
      <form onSubmit={handleRegister} className="flex flex-col gap-4 w-full">
        <div className="flex flex-col gap-1">
          <label className={`${INPUT_TEXT}`}>Full Name</label>
          <input
            type="text"
            required
            placeholder="Your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={`${INPUT_CLASSES}`}
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className={`${INPUT_TEXT}`}>User Name</label>
          <input
            type="text"
            required
            placeholder="Your user name"
            value={user_name}
            onChange={(e) => setUserName(e.target.value)}
            className={`${INPUT_CLASSES}`}
          />
        </div>

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
