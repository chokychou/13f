import { Tag, Users, Settings, Bookmark, SquarePen, LayoutGrid } from "lucide-react";
import { tabs } from "./tab_list"

export function getMenuList(pathname) {
  return [
    {
      groupLabel: "",
      menus: [
        {
          href: "#",
          label: "Live",
          icon: LayoutGrid,
          submenus: []
        }
      ]
    },
    {
      groupLabel: "Stats",
      menus: [
        {
          href: "#",
          label: tabs._13_filings,
          icon: SquarePen,
          submenus: [
          ]
        },
      ]
    }
  ];
}
