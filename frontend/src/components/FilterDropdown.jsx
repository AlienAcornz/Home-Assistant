import { useState, useEffect, useRef } from "react";

function FilterDropdown() {
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
    <div ref={filterRef}>
      {filterPaneState ? (
        <div>
          <button type="button" onClick={onFilterClick}>
            Filter ▲
          </button>

          <div>
            <label>
              <input type="checkbox" />
              Option A
            </label>
            <br />
            <label>
              <input type="checkbox" />
              Option B
            </label>
            <br />
            <label>
              <input type="checkbox" />
              Option C
            </label>
          </div>
        </div>
      ) : (
        <div>
          <button type="button" onClick={onFilterClick}>
            Filter ▼
          </button>
        </div>
      )}
    </div>
  );
}

export default FilterDropdown;
