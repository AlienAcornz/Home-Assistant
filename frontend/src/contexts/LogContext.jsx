import {
  createContext,
  useState,
  useContext,
  useEffect,  
  useDebugValue,
} from "react";

const LogContext = createContext();

export const useLogContext = () => useContext(LogContext);

export const LogProvider = ({ children }) => {
  const [filters, setFilters] = useState([]);

  useEffect(() => {
    const storedFilters = localStorage.getItem("filters");

    if (storedFilters) setFilters(JSON.parse(storedFilters));
  }, []);

  useEffect(() => {
    localStorage.setItem("filters", JSON.stringify(filters));
  }, [filters]);
  const addToFilters = (filter) => {
    setFilters((prev) => [...prev, filter]);
  };

  const removeFromFilters = (filter) => {
    setFilters((prev) => prev.filter((f) => f !== filter));
  };

  const value = {
    filters,
    addToFilters,
    removeFromFilters,
  };

  return (
    <LogContext.Provider value={value}>{children}</LogContext.Provider>
  );
};
