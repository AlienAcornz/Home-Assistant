import { useState, useEffect, useRef } from "react";
import "../css/FilterDropdown.css";

function FilterDropdown({ logs }) {
  const [filterPaneState, setFilterPaneState] = useState(false);
  const filterRef = useRef(null);

  function onFilterClick(e) {
    e.preventDefault();
    setFilterPaneState((prev) => !prev);
  }

  useEffect(() => {
    function handleClickOutside(event) {
      if (filterRef.current && !filterRef.current.contains(event.target)) {
        setFilterPaneState(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="filter-dropdown" ref={filterRef}>
      <button type="button" onClick={onFilterClick}>
        Filter {filterPaneState ? "▲" : "▼"}
      </button>
      {filterPaneState && (
        <div className="dropdown-panel">
          <label><input type="checkbox" /> Option A</label><br />
          <label><input type="checkbox" /> Option B</label><br />
          <label><input type="checkbox" /> Option C</label>
        </div>
      )}
    </div>
  );
}

export default FilterDropdown;
