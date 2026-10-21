import { User, Users } from "lucide-react";
import Button from "../../../components/Button";

interface QuickViewProps {
  width?: string;
}

export default function QuickView({ width }: QuickViewProps) {
  const containerWidth = width || "w-[300px]";
  const iconButtonSize = "w-14 h-14 p-0 text-sm";
  const lastSessionSize = "w-full h-15";

  return (
    <div
      className={`
        ${containerWidth}
        fixed
        top-16
        left-0
        z-10
        w-full
        flex
        flex-col
        gap-3
      `}
    >
      <div className="w-full px-8">
        <Button size={lastSessionSize} aria-label="LastSession">
          Last Session
        </Button>
      </div>

      <div
        className="flex items-left gap-2
        flex-col px-2"
      >
        <Button
          size={iconButtonSize}
          icon={<Users className="w-5 h-5" />}
          aria-label="Amigos"
        />
        <Button
          size={iconButtonSize}
          icon={<Users className="w-5 h-5" />}
          aria-label="Amigos"
        />
      </div>
    </div>
  );
}
