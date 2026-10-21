import { useNavigate } from "react-router";
import { GraduationCap } from "lucide-react";
import Button from "../../components/Button";
import { COLORS } from "../../constants/colors";
import { SIZES } from "../../constants/sizes";

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <div
      className={`min-h-screen w-full flex flex-col items-center justify-between p-6 ${COLORS.light_mode.bg}`}
    >
      <div className="w-full max-w-sm flex flex-col items-center justify-center my-auto gap-4">
        <div
          className={`w-20 h-20 ${COLORS.accents.highlight.bg} rounded-3xl flex items-center justify-center`}
        >
          <GraduationCap
            className={`w-10 h-10 ${COLORS.accents.highlight.text}`}
          />
        </div>

        <div className="text-center">
          <h1 className="text-xl font-bold  tracking-tight">Study Together</h1>
        </div>
      </div>

      <div
        className={`
        w-full 
        max-w-sm 
        flex flex-col items-center 
        gap-3 
        `}
      >
        <Button
          variant="accent"
          size={`
            w-full
            ${SIZES.buttons.sm.h}
            ${SIZES.buttons.md.text}
            text-base`}
          onClick={() => navigate("/register")}
        >
          Register
        </Button>

        <Button
          variant="blue"
          size={`
            w-full
            ${SIZES.buttons.sm.h}
            ${SIZES.buttons.md.text}
            text-base`}
          onClick={() => navigate("/login")}
        >
          Log In
        </Button>

        <p className="text-xs text-slate-400 text-center mt-2">
          By continuing, you agree to our{" "}
          <button
            onClick={() => console.log("Terms clicked")}
            className={`underline font-medium hover:text-slate-600 transition-colors`}
          >
            Terms & Conditions
          </button>
        </p>
      </div>
    </div>
  );
}
