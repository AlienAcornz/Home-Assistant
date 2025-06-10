import { useState, useEffect } from "react";
import MessageInfo from "../components/MessageInfo";
import "../css/Home.css";
import { getLogs } from "../services/api";
import { useLogContext } from "../contexts/LogContext";

function Home() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const { filters: selectedFilters } = useLogContext();

  useEffect(() => {
    const loadLogs = async () => {
      try {
        const logs = await getLogs();
        setLogs(logs);
      } catch (err) {
        console.error("Failed to fetch logs:", err);
        setError("Failed to load logs...");
      } finally {
        setLoading(false);
      }
    };

    loadLogs();

    const interval = setInterval(loadLogs, 1000);
    return () => clearInterval(interval);
  }, []);

  function checkFilter(message) {
    return selectedFilters.includes(message.tag)
  }

  return (
    <div className="home">
      <div className="message-stream">
        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Message:</th>
                <th>Timestamp</th>
                <th>Tags</th>
              </tr>
            </thead>
            <tbody>
              {[...logs].filter(checkFilter).reverse().map((message) => (
                <MessageInfo key={message.id} message={message} />
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Home;
