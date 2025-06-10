import { useState, useEffect, useRef } from "react";
import "../css/FilterDropdown.css";
import { getFilters } from "../services/api";
import { useLogContext } from "../contexts/LogContext";

function FilterDropdown({ logs }) {
  // State for controlling the visibility of the dropdown panel
  const [filterPaneState, setFilterPaneState] = useState(false);
  // Ref to detect clicks outside the dropdown to close it
  const filterRef = useRef(null);

  // State to store the filters fetched from the API (e.g., 'Warning', 'Error', 'Info')
  // Renamed from 'filters' to 'availableFilters' for clarity to distinguish from context filters
  const [availableFilters, setAvailableFilters] = useState([]);
  // State for error handling during API calls
  const [error, setError] = useState(null);
  // State for loading indicator during API calls
  const [loading, setLoading] = useState(true);

  // Destructure selectedFilters and functions to modify them from LogContext
  const { filters: selectedFilters, addToFilters, removeFromFilters } = useLogContext();

  // State for the "All" checkbox within the dropdown.
  // This state will be derived from whether all individual filters are selected in the context.
  const [isAllCheckboxChecked, setIsAllCheckboxChecked] = useState(false);
  // State to manage the indeterminate visual state of the "All" checkbox
  const [isAllCheckboxIndeterminate, setIsAllCheckboxIndeterminate] = useState(false);
  // Ref for the "All" checkbox input element to set its indeterminate property directly
  const allCheckboxRef = useRef(null);


  // Effect to fetch filters from the API on component mount and set up an interval for updates.
  useEffect(() => {
    const loadFilters = async () => {
      try {
        const fetchedFilters = await getFilters();
        setAvailableFilters(fetchedFilters);
      } catch (err) {
        console.error("Failed to fetch filters:", err);
        setError("Failed to load filters...");
      } finally {
        setLoading(false);
      }
    };

    loadFilters(); // Initial load

    // Set up an interval to refresh filters every second
    const interval = setInterval(loadFilters, 1000);
    // Cleanup function to clear the interval when the component unmounts
    return () => clearInterval(interval);
  }, []); // Empty dependency array means this effect runs once on mount

  // Effect to update the state of the "All" checkbox (checked/unchecked/indeterminate)
  // based on the selected individual filters.
  useEffect(() => {
    // Only proceed if there are available filters to compare against and they are loaded
    if (!loading && !error && availableFilters.length > 0) {
      const allSelected = availableFilters.every(filter =>
        selectedFilters.includes(filter)
      );
      const noneSelected = availableFilters.every(filter =>
        !selectedFilters.includes(filter)
      );

      // If all filters are selected, 'All' checkbox should be checked.
      // If no filters are selected, 'All' checkbox should be unchecked.
      // Otherwise, it's in an indeterminate state.
      setIsAllCheckboxChecked(allSelected);
      setIsAllCheckboxIndeterminate(!allSelected && !noneSelected);
    } else {
      // If no available filters or still loading/error, 'All' checkbox should be unchecked and not indeterminate.
      setIsAllCheckboxChecked(false);
      setIsAllCheckboxIndeterminate(false);
    }
  }, [selectedFilters, availableFilters, loading, error]); // Re-run when these dependencies change

  // Effect to set the 'indeterminate' property on the actual DOM element of the "All" checkbox.
  // This property cannot be set directly via JSX props.
  useEffect(() => {
    if (allCheckboxRef.current) {
      allCheckboxRef.current.indeterminate = isAllCheckboxIndeterminate;
    }
  }, [isAllCheckboxIndeterminate]); // Re-run when the indeterminate state changes

  // Handler for the main "Filter" button click to toggle dropdown visibility
  function onFilterClick(e) {
    e.preventDefault(); // Prevent default button behavior (e.g., form submission)
    setFilterPaneState((prev) => !prev); // Toggle the dropdown panel's visibility
  }

  // Effect to handle clicks outside the dropdown to close it
  useEffect(() => {
    function handleClickOutside(event) {
      // If the dropdown ref exists and the click is outside the dropdown element
      if (filterRef.current && !filterRef.current.contains(event.target)) {
        setFilterPaneState(false); // Close the dropdown
      }
    }

    // Add event listener for mousedown on the document
    document.addEventListener("mousedown", handleClickOutside);
    // Cleanup function to remove the event listener when the component unmounts
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []); // Empty dependency array means this effect runs once on mount

  // Handler for the "All" checkbox change
  const handleAllCheckboxChange = (e) => {
    const checked = e.target.checked;
    // When "All" is clicked, we explicitly check/uncheck all available filters.
    // The `isAllCheckboxChecked` state will be updated by the useEffect above
    // based on the changes propagated through selectedFilters.

    if (checked) {
      // If "All" is checked, add all available filters to the context
      availableFilters.forEach(filter => {
        // Only add if the filter is not already present in selectedFilters to avoid unnecessary updates
        if (!selectedFilters.includes(filter)) {
          addToFilters(filter);
        }
      });
    } else {
      // If "All" is unchecked, remove all available filters from the context
      availableFilters.forEach(filter => {
        // Only remove if the filter is currently present in selectedFilters
        if (selectedFilters.includes(filter)) {
          removeFromFilters(filter);
        }
      });
    }
    // No need to setIsAllCheckboxChecked here directly, as it's derived from selectedFilters
  };

  // Handler for individual filter checkbox changes
  const handleIndividualCheckboxChange = (e, filter) => {
    const checked = e.target.checked;
    // Added logging to help debug why individual checkboxes might not be unchecking.
    console.log(`[FilterDropdown] Checkbox for "${filter}" changed to: ${checked}`); 
    if (checked) {
      addToFilters(filter); // Add the filter to context if checked
    } else {
      removeFromFilters(filter); // Remove the filter from context if unchecked
    }
  };

  return (
    <div className="filter-dropdown" ref={filterRef}>
      <button type="button" onClick={onFilterClick}>
        Filter {filterPaneState ? "▲" : "▼"} {/* Toggle arrow based on state */}
      </button>

      {filterPaneState && ( // Render dropdown panel only if filterPaneState is true
        <div className="dropdown-panel">
          <label>
            <input
              type="checkbox"
              ref={allCheckboxRef} // Assign ref to the "All" checkbox
              checked={isAllCheckboxChecked} // This checkbox is controlled by local state
              onChange={handleAllCheckboxChange} // Handle changes for the "All" checkbox
            />
            All
          </label>
          <br />

          {loading && <div>Loading filters...</div>}
          {error && <div style={{ color: "red" }}>{error}</div>}
          {/* Display message if no filters are available after loading */}
          {!loading && !error && availableFilters.length === 0 && (
            <div>No filters available.</div>
          )}

          {/* Render individual filter checkboxes if not loading and no error */}
          {!loading && !error && availableFilters.length > 0 && (
            [...availableFilters] // Create a shallow copy to sort without modifying original array
              .sort((a, b) => a.localeCompare(b)) // Sort filters alphabetically
              .map((filter) => (
                <div key={filter}> {/* Use filter string as key, assuming they are unique */}
                  <label>
                    <input
                      type="checkbox"
                      // This checkbox is controlled by checking if the filter is in the context's selectedFilters.
                      // This setup is designed to allow the user to check and uncheck individual filters.
                      checked={selectedFilters.includes(filter)}
                      // Handle changes for individual filter checkboxes
                      onChange={(e) => handleIndividualCheckboxChange(e, filter)}
                    />
                    {filter}
                  </label>
                </div>
              ))
          )}
        </div>
      )}
    </div>
  );
}

export default FilterDropdown;
