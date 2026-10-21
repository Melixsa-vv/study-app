import UpperBar from "./sections/home/UpperBar";
import QuickView from "./sections/home/QuickView";
import FooterBar from "./sections/home/FooterBar";
import Feed from "./sections/home/Feed";

import { feedData } from "../data/FeedData";

export default function Home() {
  const handleSelectItem = (item: any) => {
    console.log("Elemento seleccionado:", item);
  };

  return (
    <div
      className={`min-h-screen
       bg-white
       text-white 
       p-0`}
    >
      <UpperBar />
      <QuickView />

      <main className="w-full px-4 pt-56 pb-24 flex flex-col items-start gap-4">
        <Feed items={feedData} onSelectItem={handleSelectItem} />
      </main>

      <FooterBar />
    </div>
  );
}
