import { Home, BookOpen, PlusCircle, Settings } from "lucide-react";
import Button from "../../../components/Button";

export default function FooterBar() {
  const iconButtonSize = "w-10 h-10 p-0 text-sm";

  return (
    <footer className="fixed bottom-0 left-0 w-full py-2 px-4 bg-blue-200 z-10">
      <div className="w-full flex items-center justify-center">
        <div className="flex items-center gap-3">
          <Button
            size={iconButtonSize}
            icon={<Home className="w-5 h-5" />}
            aria-label="Home"
          />

          <Button
            size={iconButtonSize}
            icon={<BookOpen className="w-5 h-5" />}
            aria-label="Subjects"
          />

          <Button
            size={iconButtonSize}
            icon={<PlusCircle className="w-5 h-5" />}
            aria-label="Create"
          />
          <Button
            size={iconButtonSize}
            icon={<Settings className="w-5 h-5" />}
            aria-label="Settings"
          />
        </div>
      </div>
    </footer>
  );
}
