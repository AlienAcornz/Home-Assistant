import FilterDropdown from "./FilterDropdown";
import "../css/NavBar.css";

function NavBar() {
  return (
    <div className="nav-bar">
      <div className="nav-left">
        <button>Home</button>
        <button>Chat</button>
      </div>
      <FilterDropdown />
    </div>
  );
}

export default NavBar;
