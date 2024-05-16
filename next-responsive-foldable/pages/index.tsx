import { FC, useState } from "react";
import styles from "../styles/Home.module.css";
import Items, { ItemProps } from "./Items";

interface SectionProps {
  title: string;
  items: ItemProps[];
}

const Section: FC<SectionProps> = ({ title, items }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSectionClick = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div
      className={`${styles.section} ${isExpanded ? styles.expandedSection : ""}`}
    >
      <h2 className={styles.sectionTitle} onClick={handleSectionClick}>
        {title}
      </h2>
      <Items items={items} initialItemsToShow={3} />
    </div>
  );
};

export default Section;
