import { useState, useEffect } from "react";
import MessageInfo from "../components/MessageInfo";

function Home() {
    const [logs, setLogs] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const temp_logs = [
            {message: "Assistant: Hello!", time: "18:56", tag: "chat", id: 0},
            {message: "Timer created for 300s", time: "19:14", tag: "tools", id: 1},
            {message: "User: Hi!", time: "19:42", tag: "chat", id: 2}
        ]
        setLogs(temp_logs);
    }, [])

    return (
        <div className="home">
            <div className="message-stream">
                <table>
                    <tr>
                        <th>Message:</th>
                        <th>Timestamp</th>
                        <th>Tags</th>
                    </tr>
                    {logs.map((message) => (
                    <MessageInfo message={message} key={message.id}/>
                ))}
                </table>
            </div>
        </div>        
    )
}

export default Home;