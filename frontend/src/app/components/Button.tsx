import React from "react";
import { COLORS } from "../constants/colors";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: string;
  text?: string;
  variant?: keyof typeof COLORS.buttons;
  icon?: React.ReactNode;
}

export default function Button({
  size,
  variant = "blue",
  text,
  icon,
  children,
  ...props
}: ButtonProps) {
  const buttonSize = size || "px-6 py-6 text-base";
  const colors = COLORS.buttons[variant] || COLORS.buttons.blue;

  return (
    <button
      className={`
        ${colors.bg}
        ${colors.hover}
        text-white 
        font-bold 
        rounded-lg 
        flex 
        items-center 
        justify-center 
        gap-2 
        
        transition-all 
        duration-200 
        shadow-sm 
        cursor-pointer
        ${buttonSize}
      `}
      {...props}
    >
      {icon && text && (
        <>
          <span>{icon}</span>
          <span>{text}</span>
        </>
      )}

      {icon && !text && <span>{icon}</span>}

      {!icon && text && <span>{text}</span>}
    </button>
  );
}
