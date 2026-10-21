import { User, Bell, Users, Flame } from "lucide-react";
import Button from "../../../components/Button";

export default function UpperBar() {
  const iconButtonSize = "w-10 h-10 p-0 text-sm";

  return (
    <header className="fixed bg-white top-0 left-0 w-full py-2 px-4  z-10 ">
      <div className="w-full h-18px flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Button
            size={iconButtonSize}
            icon={<Flame className="w-5 h-5" />}
            aria-label="Streak"
          />
        </div>

        <div className="flex items-center gap-3">
          <Button
            size={iconButtonSize}
            icon={<Users className="w-5 h-5" />}
            aria-label="Friends"
          />

          <Button
            size={iconButtonSize}
            icon={<Bell className="w-5 h-5" />}
            aria-label="Notifications"
          />

          <Button
            size={iconButtonSize}
            icon={<User className="w-5 h-5" />}
            aria-label="Perfil"
          />
        </div>
      </div>
    </header>
  );
}
