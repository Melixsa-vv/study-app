import React from "react";
import { COLORS } from "../constants/colors";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: string;
  variant?: keyof typeof COLORS.buttons;
  icon?: React.ReactNode;
}

export default function Button({
  size,
  variant = "blue",
  icon,
  children,
  ...props
}: ButtonProps) {
  const buttonSize = size || "w-12 h-12";
  const colors = COLORS.buttons[variant] || COLORS.buttons.blue;

  return (
    <button
      className={`
        ${colors.bg}
        ${colors.hover}
        text-white 
        font-bold 
        rounded-xl 
        flex 
        items-center 
        justify-center 
        gap-2 
        whitespace-nowrap
        select-none
        transition-all 
        duration-200 
        shadow-sm 
        cursor-pointer
        ${buttonSize}
      `}
      {...props}
    >
      {icon && <span className="flex items-center justify-center">{icon}</span>}
      {children && <span>{children}</span>}
    </button>
  );
}
